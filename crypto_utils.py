from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

def generate_rsa_keys():
    """
    Genera un par de claves RSA (clave privada y clave pública).

    Returns:
        Tupla con la clave privada y la clave pública generadas.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

def sign_transaction(transaction, private_key):
    """
    Firma una transacción utilizando la clave privada RSA.

    Args:
        transaction: Transacción a firmar.
        private_key: Clave privada RSA para firmar la transacción.

    Returns:
        Firma digital de la transacción.
    """
    transaction_data = str(transaction).encode()
    signature = private_key.sign(
        transaction_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_transaction(transaction, signature, public_key):
    """
    Verifica la firma digital de una transacción utilizando la clave pública RSA.

    Args:
        transaction: Transacción a verificar.
        signature: Firma digital de la transacción.
        public_key: Clave pública RSA para verificar la firma.

    Returns:
        True si la firma es válida, False en caso contrario.
    """
    transaction_data = str(transaction).encode()
    try:
        public_key.verify(
            signature,
            transaction_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
