import hashlib

class MerkleNode:
    '''A node in the Merkle Tree. Each node has a data, hash, left child, and right child.'''
    def __init__(self, data):
        self.data = data
        self.hash = hashlib.sha256(data.encode()).hexdigest()
        self.left = None
        self.right = None

class MerkleTree:
    '''A Merkle Tree is a binary tree where each non-leaf node is the hash of its children.'''
    def __init__(self, transactions):
        self.root = self.build_tree(transactions)

    def build_tree(self, transactions):
        '''Builds the Merkle Tree from the list of transactions.'''
        if len(transactions) == 0:
            return None
        elif len(transactions) == 1:
            return MerkleNode(transactions[0])

        mid = len(transactions) // 2
        left_subtree = self.build_tree(transactions[:mid])
        right_subtree = self.build_tree(transactions[mid:])
        
        root = MerkleNode(left_subtree.hash + right_subtree.hash)
        root.left = left_subtree
        root.right = right_subtree

        return root

    def get_root(self):
        return self.root.hash if self.root else None

    def pretty_print(self, node, prefix="", is_left=True):
        '''Pretty prints the Merkle Tree.'''
        if node is not None:
            self.pretty_print(node.right, prefix + ("│   " if is_left else "    "), False)
            print(prefix + ("└── " if is_left else "┌── ") + node.hash)
            self.pretty_print(node.left, prefix + ("    " if is_left else "│   "), True)

    def get_proof(self, transaction):
        '''Returns the hash of the transaction and the Merkle Path to it.'''
        if self.root is None:
            return None, []

        return self._get_proof_helper(self.root, transaction)

    def _get_proof_helper(self, node, transaction):
        if node is None:
            return None, []

        if node.data == transaction:
            return node.hash, []

        left_hash, left_proof = self._get_proof_helper(node.left, transaction)
        if left_hash is not None:
            left_proof.append(node.right.hash)
            return left_hash, left_proof

        right_hash, right_proof = self._get_proof_helper(node.right, transaction)
        if right_hash is not None:
            right_proof.append(node.left.hash)
            return right_hash, right_proof

        return None, []

def validate_proof(merkle_root_hash, transaction_hash, merkle_path):
    '''Validates the Merkle Path of a transaction.'''
    if not merkle_path:
        return transaction_hash == merkle_root_hash

    sibling_hash = merkle_path[0]
    computed_hash_1 = hashlib.sha256((transaction_hash + sibling_hash).encode()).hexdigest()
    computed_hash_2 = hashlib.sha256((sibling_hash + transaction_hash).encode()).hexdigest()

    left_path = validate_proof(merkle_root_hash, computed_hash_2, merkle_path[1:])
    right_path = validate_proof(merkle_root_hash, computed_hash_1, merkle_path[1:])

    return left_path or right_path

if __name__ == "__main__":

    transactions = [f"transaction{i}" for i in range(1, 20)]

    merkle_tree = MerkleTree(transactions)

    print("Merkle Root:", merkle_tree.get_root())
    print("\nMerkle Tree:")
    merkle_tree.pretty_print(merkle_tree.root)

    transaction_to_verify = 'transaction19'
    transaction_hash, merkle_path = merkle_tree.get_proof(transaction_to_verify)
    print("\nTransaction Hash:", transaction_hash)
    print("Merkle Path Length:", len(merkle_path), "\n","Merkle Path:", merkle_path)

    is_valid = validate_proof(merkle_tree.get_root(), transaction_hash, merkle_path)
    print("Is Valid:", is_valid)
