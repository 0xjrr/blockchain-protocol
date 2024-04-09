from transaction import Transaction 
from block import Block

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # Create the first block with a placeholder transaction
        return Block(transactions=[Transaction(inputs="0", outputs="Genesis Block", signature="")], previous_hash="0")
    
    def add_block(self, block):
        # Add a new block if valid (validation logic to be implemented)
        self.chain.append(block)
