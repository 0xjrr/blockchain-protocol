import hashlib
import time

class Block:
    '''Block class for the blockchain.'''
    def __init__(self, block_id, previous_hash, transactions, timestamp):
        self.block_id = block_id
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = 0

    def compute_hash(self):
        '''Returns the hash of the block.'''
        return hashlib.sha256((str(self.block_id) + self.previous_hash + str(self.transactions) + str(self.timestamp) + str(self.nonce)).encode()).hexdigest()

    def __str__(self):
        return f"\nBlock ID: {self.block_id}\nPrevious Hash: {self.previous_hash}\nTransactions: {self.transactions}\nTimestamp: {self.timestamp}\nNonce: {self.nonce}"


class Blockchain:
    '''Blockchain class.'''
    def __init__(self):
        '''Initializes the blockchain. Creates the genesis block.'''
        self.chain = []
        self.difficulty = 4  # Initial difficulty level
        self.target_time_interval = 15  # Target time interval between blocks in seconds
        self.block_count_since_adjustment = 0
        self.total_time_since_adjustment = 0
        # Create genesis block (initial block)
        genesis_block = Block(0, "0", "Genesis", time.time())
        self.add_block(genesis_block)

    def add_block(self, new_block):
        '''Adds a new block to the blockchain.'''
        if len(self.chain) > 0:
            new_block.previous_hash = self.chain[-1].compute_hash()

        # Mine the block with adjusted difficulty
        new_block, time_taken = self.mine_block(new_block)

        self.chain.append(new_block)
        print("Block mined successfully.")
        print("Time taken:", time_taken, "seconds")

        self.block_count_since_adjustment += 1
        self.total_time_since_adjustment += time_taken

        # Adjust difficulty every multiple of 10 blocks
        if self.block_count_since_adjustment % 10 == 0:
            self.adjust_difficulty()

    def mine_block(self, block):
        '''Mines the block with proof of work.'''
        start_time = time.time()
        target = "0" * self.difficulty

        while block.compute_hash()[:self.difficulty] != target:
            block.nonce += 1

        end_time = time.time()
        time_taken = end_time - start_time

        return block, time_taken

    def adjust_difficulty(self):
        '''Adjusts the difficulty level based on the time taken to mine the blocks.'''
        average_time = self.total_time_since_adjustment / self.block_count_since_adjustment

        print("Average time taken to mine a block:", average_time, "seconds")

        # A buffer of 5 seconds is added to the target time interval to prevent frequent difficulty adjustments
        if average_time < self.target_time_interval - 5: # Decrease difficulty by 1 if average time is less than target time interval - 5 seconds
            self.difficulty += 1
        elif average_time > self.target_time_interval + 5 and self.difficulty > 1: # Increase difficulty by 1 if average time is more than target time interval + 5 seconds
            self.difficulty -= 1

        print("Difficulty adjusted to:", self.difficulty)

        # Reset counters
        self.block_count_since_adjustment = 0
        self.total_time_since_adjustment = 0


if __name__ == "__main__":
    # Example usage
    blockchain = Blockchain()

    for i in range(1, 100):
        print("\n---------Adding block #", i, "---------")
        new_block = Block(i, "", "Transaction data " + str(i), time.time())
        blockchain.add_block(new_block)
        print("Block #", i, " added to the blockchain", blockchain.chain[-1])