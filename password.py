from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


# https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet
def derive_key(password: str) -> bytes:
    salt = b'\xd3\x96\xf7\xa1\x93vO\x02P4\xf6\xd6ka\x80\x84'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    return base64.urlsafe_b64encode(kdf.derive(bytes(password, 'utf-8')))
