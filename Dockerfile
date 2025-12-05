# ---------- Stage 1: builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install Python dependencies into /install
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# ---------- Stage 2: runtime ----------
FROM python:3.11-slim

ENV TZ=UTC
WORKDIR /app

# Install system deps: cron + tzdata + curl
RUN apt-get update && apt-get install -y \
    cron tzdata curl \
 && rm -rf /var/lib/apt/lists/*

# Copy Python deps from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . /app

# Create mount points and install cron job
RUN mkdir -p /data /cron && chmod 755 /data /cron
COPY cron/cronfile /etc/cron.d/app-cron
RUN chmod 0644 /etc/cron.d/app-cron && crontab /etc/cron.d/app-cron

# Start cron and FastAPI app
CMD service cron start && uvicorn app:app --host 0.0.0.0 --port 8080