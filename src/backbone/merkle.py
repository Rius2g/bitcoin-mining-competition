from utils.cryptographic import hash_function

# TODO: Make Merkle tree structure

class MerkelNode:
    def __init__(self, left, right, hash):
        self.left: MerkelNode = left
        self.right: MerkelNode = right
        self.hash = hash

class MerkleTree:
    def __init__(self, txs):
        self.data = None
        self.leaf_nodes = None
        self.build_tree(txs)
        self.root = None

    def build_tree(self, hashes):
        #fill up the hashes list if < 4 hashes
        leaves: [MerkelNode] = [MerkelNode(None, None, _) for _ in range(len(hashes))]
        if len(hashes) % 2 == 1:
            hashes.append(hashes[-1])
        self.root = self.build_tree_helper(leaves)

    def build_tree_helper(self, Nodes):
        if len(Nodes) % 2 == 1:
            Nodes.append(Nodes[-1])
            half = len(Nodes) // 2
        if len(Nodes) == 2:
            return MerkelNode(Nodes[0], Nodes[1], hash_function(Nodes[0].hash + Nodes[1].hash))
        
        left = self.build_tree_helper(Nodes[:half])
        right = self.build_tree_helper(Nodes[half:])
        return MerkelNode(left, right, hash_function(left.hash + right.hash))
    

    def get_root(self):
        return self.root.hash
