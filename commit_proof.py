from pathlib import Path
import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def sign_message(message: str, private_key) -> bytes:
    message_bytes = message.encode("utf-8")
    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature

def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext

def load_private_key(path: str):
    pem = Path(path).read_bytes()
    return serialization.load_pem_private_key(pem, password=None)

def load_public_key(path: str):
    pem = Path(path).read_bytes()
    return serialization.load_pem_public_key(pem)

if __name__ == "__main__":
    commit_hash = "849505e0a1413636bb1486cb380f1ccb0f1b750e"

    student_priv = load_private_key("student_private.pem")
    instructor_pub = load_public_key("instructor_public.pem")

    signature = sign_message(commit_hash, student_priv)
    encrypted_sig = encrypt_with_public_key(signature, instructor_pub)

    encrypted_sig_b64 = base64.b64encode(encrypted_sig).decode("utf-8")

    print("Commit Hash:", commit_hash)
    print("Encrypted Signature (base64):", encrypted_sig_b64)
