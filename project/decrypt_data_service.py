from typing import Optional

from cryptography.fernet import Fernet
from pydantic import BaseModel


class DecryptDataResponse(BaseModel):
    """
    This model represents the response after decrypting the data, containing the original plaintext data.
    """

    decrypted_data: str


def decrypt_data(
    encrypted_data: str, decryption_key: Optional[str] = None
) -> DecryptDataResponse:
    """
    Decrypts previously encrypted data.

    Args:
        encrypted_data (str): The encrypted data string that needs to be decrypted.
        decryption_key (Optional[str]): The key used for the decryption process. This might be optional if the system
                                        uses a standard key or method that does not require explicit input.

    Returns:
        DecryptDataResponse: This model represents the response after decrypting the data, containing the original plaintext data.
    """
    standard_key = b"aGv7HmL8BsNo3tpxZ4YjW_EPdS3fiIuOQbqBmyn8h1E="
    key_to_use = decryption_key.encode() if decryption_key else standard_key
    fernet = Fernet(key_to_use)
    decrypted_data_bytes = fernet.decrypt(encrypted_data.encode())
    decrypted_data_str = decrypted_data_bytes.decode("utf-8")
    return DecryptDataResponse(decrypted_data=decrypted_data_str)
