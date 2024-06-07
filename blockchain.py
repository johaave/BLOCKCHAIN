from block import Block
# Maneja la adición de transacciones y bloques, y asegura la validez de los bloques añadidos.
class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

    def create_block(self, previous_hash):
        block = Block(previous_hash, self.pending_transactions)
        self.pending_transactions = []
        return block

    def add_block(self, block):
        if self.is_valid_block(block):
            self.chain.append(block)
            print("Bloque añadido a la cadena.")
        else:
            print("El bloque no es válido y no se puede añadir a la cadena.")

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def is_valid_block(self, block):
        if not block:
            return False

        if not self.chain:
            return block.previous_hash == "0" * 64

        previous_block = self.chain[-1]
        if block.previous_hash != previous_block.block_hash:
            return False

        if not self.is_valid_proof_of_work(block):
            return False

        return True

    def is_valid_proof_of_work(self, block):
        block_hash = block.calculate_block_hash()
        difficulty = 4  
        return block_hash.startswith('0' * difficulty)

    def is_valid_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.previous_hash != previous_block.block_hash:
                return False

            if not self.is_valid_proof_of_work(current_block):
                return False

        return True
