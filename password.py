from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def derive_key(password: str) -> bytes:
    '''
    Deriva una clave a partir de una contraseña utilizando PBKDF2-HMAC con SHA-256.
    Parámetros:
    - password: Contraseña de entrada para derivar la clave.
    Resultado:
    - Una cadena de bytes que representa la clave derivada, codificada en base64.
    Precondiciones:
    - Ninguna.
    Postcondiciones:
    - La clave derivada se obtiene utilizando el algoritmo PBKDF2-HMAC con SHA-256.
    - La clave se codifica en base64 antes de ser devuelta.
    '''
    salt = b'\xd3\x96\xf7\xa1\x93vO\x02P4\xf6\xd6ka\x80\x84'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    return base64.urlsafe_b64encode(kdf.derive(bytes(password, 'utf-8')))
