import base64
import os
from typing import Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from pydantic import BaseModel


class EncryptDataResponse(BaseModel):
    """
    The response model returning the result of the encryption process.
    """

    encrypted_data: str


def encrypt_data(
    data: str, encryption_schema: Optional[str] = None
) -> EncryptDataResponse:
    """
    Encrypts the provided data using AES-GCM for strong encryption and authentication.
    If no schema is specified, this function will use a default secure configuration.

    Args:
        data (str): The data to be encrypted. Accepts a string or base64 encoded binary data.
        encryption_schema (Optional[str]): The name of the encryption schema to use.
            Supports 'PBKDF2HMAC' or 'Scrypt' for key derivation. Defaults to None.

    Returns:
        EncryptDataResponse: A model including the encrypted data as a base64 encoded string.

    Example:
        encrypt_data('Hello, World!')
        > EncryptDataResponse(encrypted_data='encrypted_base64_string')
    """
    salt = os.urandom(16)
    backend = default_backend()
    if encryption_schema == "PBKDF2HMAC":
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
            backend=backend,
        )
    elif encryption_schema == "Scrypt":
        kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=backend)
    else:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
            backend=backend,
        )
    key = kdf.derive(data.encode())
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    encrypted_data = aesgcm.encrypt(nonce, data.encode(), None)
    encrypted_blob = nonce + encrypted_data
    encrypted_data_base64 = base64.b64encode(encrypted_blob).decode("utf-8")
    return EncryptDataResponse(encrypted_data=encrypted_data_base64)
