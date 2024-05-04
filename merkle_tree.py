import hashlib

class MerkleNode:
    def __init__(self, data):
        self.data = data
        self.hash = hashlib.sha256(data.encode()).hexdigest()
        self.left = None
        self.right = None

def build_tree(transactions):
    if len(transactions) == 0:
        return None
    elif len(transactions) == 1:
        return MerkleNode(transactions[0])

    mid = len(transactions) // 2
    left_subtree = build_tree(transactions[:mid])
    right_subtree = build_tree(transactions[mid:])
    
    root = MerkleNode(left_subtree.hash + right_subtree.hash)
    root.left = left_subtree
    root.right = right_subtree

    return root

def get_root(tree):
    return tree.hash if tree else None

def pretty_print(node, prefix="", is_left=True):
    if node is not None:
        pretty_print(node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + node.hash)
        pretty_print(node.left, prefix + ("    " if is_left else "│   "), True)

def get_proof(tree, transaction):
    if tree is None:
        return None, []

    if tree.data == transaction:
        return tree.hash, []

    left_hash, left_proof = get_proof(tree.left, transaction)
    if left_hash is not None:
        left_proof.append(tree.right.hash)
        return left_hash, left_proof

    right_hash, right_proof = get_proof(tree.right, transaction)
    if right_hash is not None:
        right_proof.append(tree.left.hash)
        return right_hash, right_proof

    return None, []

def validate_proof(merkle_root_hash, transaction_hash, merkle_path):
    # Base case: if the Merkle path is empty, return whether the computed hash matches the Merkle root hash
    if not merkle_path:
        return transaction_hash == merkle_root_hash

    # Get the current sibling hash
    sibling_hash = merkle_path[0]

    # Try both possibilities for concatenation order
    computed_hash_1 = hashlib.sha256((transaction_hash + sibling_hash).encode()).hexdigest()
    computed_hash_2 = hashlib.sha256((sibling_hash + transaction_hash).encode()).hexdigest()

    # Recursively validate the rest of the Merkle path
    left_path = validate_proof(merkle_root_hash, computed_hash_2, merkle_path[1:])
    right_path = validate_proof(merkle_root_hash, computed_hash_1, merkle_path[1:])

    if left_path:
        return True
    elif right_path:
        return True
    else:
        # If neither computed hash matches the Merkle root hash, the proof is invalid
        return False

if __name__ == "__main__":
    transactions = [
        "transaction1",
        "transaction2",
        "transaction3",
        "transaction4",
        "transaction5",
        "transaction6",
        "transaction7",
        "transaction8",
        "transaction9",
        "transaction10",
        "transaction11",
        "transaction12",
        "transaction13",
        "transaction14",
        "transaction15",
        "transaction16",
        "transaction17",
        "transaction18",
        "transaction19",
        "transaction20"
    ]
    merkle_tree = build_tree(transactions)
    print("Merkle Root:", get_root(merkle_tree))
    print("\nMerkle Tree:")
    pretty_print(merkle_tree)

    transaction_to_verify = 'transaction19'
    transaction_hash, merkle_path = get_proof(merkle_tree, transaction_to_verify)
    print("\nTransaction Hash:", transaction_hash)
    print("Merkle Path Length:", len(merkle_path), "\n","Merkle Path:", merkle_path)

    is_valid = validate_proof(get_root(merkle_tree), transaction_hash, merkle_path)
    print("Is Valid:", is_valid)
