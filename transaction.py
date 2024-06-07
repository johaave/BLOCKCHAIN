from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature
from crypto_utils import sign_transaction, verify_transaction

class Transaction:
    _id_counter = 1  # Contador estático para los IDs de transacción

    def __init__(self, amount, sender_id, recipient_id, signature=None):
        """
        Inicializa una nueva transacción.

        :param transaction_id: ID único de la transacción.
        :param amount: Monto de la transacción.
        :param sender_id: ID del emisor de la transacción.
        :param recipient_id: ID del receptor de la transacción.
        :param signature: Firma digital de la transacción.
        """
        self.transaction_id =  Transaction._id_counter
        Transaction._id_counter += 1
        self.amount = amount
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.signature = signature

    def __str__(self):
        """
        Retorna una representación en cadena de la transacción.
        """
        return f"Transaction ID: {self.transaction_id}\nAmount: {self.amount}\nSender ID: {self.sender_id}\nRecipient ID: {self.recipient_id}\nSignature: {self.signature}"

def create_transaction(amount, sender_id, recipient_id, private_key):
    """
    Crea una nueva transacción y la firma digitalmente.

    Args:
        transaction_id: ID de la transacción.
        amount: Cantidad a transferir.
        sender_id: ID del remitente.
        recipient_id: ID del destinatario.
        private_key: Clave privada del remitente para firmar la transacción.

    Returns:
        Objeto Transaction firmado.
    """
    transaction = Transaction(amount, sender_id, recipient_id, None)
    signature = sign_transaction(transaction, private_key)
    transaction.signature = signature
    return transaction

def validate_transaction(transaction, public_key):
    """
    Valida una transacción verificando su firma digital y otros criterios.

    Args:
        transaction: Transacción a validar.
        public_key: Clave pública del remitente para verificar la firma.

    Returns:
        True si la transacción es válida, False en caso contrario.
    """
    if not verify_transaction(transaction, transaction.signature, public_key):
        print("Error: Firma digital inválida.")
        return False

    if transaction.amount <= 0:
        print("Error: La cantidad debe ser mayor que cero.")
        return False

    if transaction.sender_id == transaction.recipient_id:
        print("Error: El remitente y el destinatario no pueden ser iguales.")
        return False

    # Aquí puedes agregar más validaciones según tus requisitos

    return True
