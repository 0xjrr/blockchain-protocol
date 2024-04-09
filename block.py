import time

class Block:
    def __init__(self, transactions, previous_hash):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0  # Placeholder for mining process
        self.timestamp = time.time()

    def hash_block(self):
        # A simplified hash function
        return hash(str(self.transactions) + str(self.timestamp) + str(self.nonce))
