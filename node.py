import json
import requests
from blockchain import Blockchain

#implementa un nodo en una red de blockchain.
#Un nodo es una entidad que participa en la red de blockchain, 
#mantiene una copia de la cadena de bloques y se comunica con otros nodos para sincronizarse y transmitir información.

class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = set()
        self.blockchain = Blockchain()

    def add_peer(self, host, port):
        """
        Añade un nuevo nodo a la lista de pares.

        Args:
            host: Dirección del nodo.
            port: Puerto del nodo.
        """
        self.peers.add((host, port))

    def sync_blockchain(self):
        """
        Sincroniza la cadena de bloques con los nodos pares.
        """
        longest_chain = None
        current_length = len(self.blockchain.chain)

        for peer in self.peers:
            response = requests.get(f"http://{peer[0]}:{peer[1]}/chain")
            if response.status_code == 200:
                data = response.json()
                chain = data["chain"]
                length = data["length"]

                if length > current_length and self.blockchain.is_valid_chain(chain):
                    current_length = length
                    longest_chain = chain

        if longest_chain:
            self.blockchain.chain = longest_chain
            print("La cadena de bloques se ha sincronizado con la cadena más larga.")
        else:
            print("La cadena actual es la más larga. No se requiere sincronización.")

    def broadcast_block(self, block):
        """
        Transmite un bloque a todos los nodos pares.

        Args:
            block: Bloque a transmitir.
        """
        for peer in self.peers:
            url = f"http://{peer[0]}:{peer[1]}/add_block"
            headers = {"Content-Type": "application/json"}
            data = {
                "block": block.__dict__
            }
            requests.post(url, headers=headers, data=json.dumps(data))

    def start(self):
        """
        Inicia el nodo y realiza la sincronización inicial de la cadena de bloques.
        """
        self.sync_blockchain()
        print("Nodo iniciado. Cadena de bloques sincronizada.")
