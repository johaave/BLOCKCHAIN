from blockchain import Blockchain
from block import Block
from transaction import Transaction, create_transaction
from wallet import Wallet
from node import Node
from crypto_utils import generate_rsa_keys, sign_transaction
from wallet_gui import WalletGUI
from cryptography.hazmat.primitives import serialization

#Coordina el proceso completo, incluyendo la creación de transacciones, la minería de bloques, 
#y la sincronización de la blockchain.

def main():
    # Generar un par de claves RSA para la billetera
    private_key, public_key = generate_rsa_keys()
    address = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).hex()

    # Crear una instancia de la cadena de bloques
    blockchain = Blockchain()

    # Crear una instancia de la billetera con una tasa de cambio configurable
    exchange_rate = 3800  # Tasa de cambio: 1 moneda local = 3800 Pesos Colombianos
    wallet = Wallet(address, private_key, balance=1000, exchange_rate=exchange_rate)

    # Crear una instancia del nodo
    node = Node("localhost", 5000)
    
    # Sincronizar la cadena de bloques con otros nodos
    node.sync_blockchain()

    # Iniciar la interfaz de usuario
    wallet_gui = WalletGUI(wallet)
    wallet_gui.start()

if __name__ == "__main__":
    main()
