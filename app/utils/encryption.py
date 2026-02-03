from cryptography.fernet import Fernet
from flask import current_app

def get_fernet():
    return Fernet(current_app.config["FERNET_KEY"])

def encrypt_data(plain_text: str) -> str:
    """
    Encrypts plaintext before DB storage
    """
    fernet = get_fernet()
    return fernet.encrypt(plain_text.encode()).decode()

def decrypt_data(cipher_text: str) -> str:
    """
    Decrypts data before sending to client
    """
    fernet = get_fernet()
    return fernet.decrypt(cipher_text.encode()).decode()
