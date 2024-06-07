import hashlib
import time

class Block:
    def __init__(self, previous_hash, transactions, nonce=0):
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = nonce
        self.merkle_root = self.calculate_merkle_root()
        self.timestamp = int(time.time())
        self.block_hash = None

    def calculate_merkle_root(self):
        transaction_hashes = [hashlib.sha256(str(tx).encode()).hexdigest() for tx in self.transactions]

        while len(transaction_hashes) > 1:
            if len(transaction_hashes) % 2 != 0:
                transaction_hashes.append(transaction_hashes[-1])

            new_level = []
            for i in range(0, len(transaction_hashes), 2):
                combined_hash = transaction_hashes[i] + transaction_hashes[i + 1]
                new_level.append(hashlib.sha256(combined_hash.encode()).hexdigest())

            transaction_hashes = new_level

        return transaction_hashes[0]

    def calculate_block_hash(self):
        block_data = (
            str(self.previous_hash) +
            str(self.timestamp) +
            str(self.transactions) +
            str(self.nonce)
        )
        block_hash = hashlib.sha256(block_data.encode()).hexdigest()
        return block_hash

    def proof_of_work(self, difficulty):
        target = '0' * difficulty
        nonce = 0
        while True:
            self.nonce = nonce
            block_hash = self.calculate_block_hash()
            if block_hash.startswith(target):
                self.block_hash = block_hash
                return self
            nonce += 1

    def __str__(self):
        return f"Previous Hash: {self.previous_hash}\nTransactions: {len(self.transactions)}\nNonce: {self.nonce}\nMerkle Root: {self.merkle_root}\nBlock Hash: {self.block_hash}"
