from utils.cryptographic import hash_function


class MerkelNode:
    def __init__(self, left, right, hash):
        self.left: MerkelNode = left
        self.right: MerkelNode = right
        self.hash = hash


class MerkleTree:
    def __init__(self, hashes): #list of hashes for transactions
        self.build_tree(hashes)

    def build_tree(self, hashes):
        leaves: [MerkelNode] = [MerkelNode(None, None, hash) for hash in hashes]
        if len(leaves) % 2 == 1:
            leaves.append(MerkelNode(None, None, leaves[-1].hash)) #need an extra Node to make it even

        self.root = self.build_tree_helper(leaves)

    def build_tree_helper(self, Nodes):
        if len(Nodes) % 2 == 1:
            Nodes.append(MerkelNode(None, None, Nodes[-1].hash)) #need an extra Node to make it even

        half = len(Nodes) // 2

        if len(Nodes) == 2:
            return MerkelNode(Nodes[0], Nodes[1], hash_function(Nodes[0].hash + Nodes[1].hash))

        left = self.build_tree_helper(Nodes[:half])
        right = self.build_tree_helper(Nodes[half:])
        return MerkelNode(left, right, hash_function(left.hash + right.hash))

    def get_root(self):
        return self.root.hash
