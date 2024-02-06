from utils.cryptographic import hash_function


class MerkelNode:
    def __init__(self, left, right, hash):
        self.left: MerkelNode = left
        self.right: MerkelNode = right
        self.hash = hash

    def __str__(self):
        return f"Node: {self.hash}, left: {self.left.hash if self.left != None else None}, right: {self.right.hash if self.left != None else None}\n"


class MerkleTree:
    def __init__(self, hashes):  # list of hashes for transactions
        self.build_tree(hashes)

    def build_tree(self, hashes):
        leaves: [MerkelNode] = [MerkelNode(None, None, hash) for hash in hashes]

        self.root = self.create_root(leaves)

    def create_root(self, Nodes):
        if len(Nodes) % 2 == 1:
            Nodes.append(
                MerkelNode(None, None, Nodes[-1].hash)
            )  # need an extra Node to make it even

        half = len(Nodes) // 2

        if len(Nodes) == 2:
            return MerkelNode(
                Nodes[0], Nodes[1], hash_function(Nodes[0].hash + Nodes[1].hash)
            )

        left = self.create_root(Nodes[:half])
        right = self.create_root(Nodes[half:])
        return MerkelNode(left, right, hash_function(left.hash + right.hash))

    def print_tree(self):
        print("root")
        print(self.root)
        print("l1")
        print(self.root.left)
        print(self.root.right)
        print("l2")
        print(self.root.left.left)
        print(self.root.left.right)
        print(self.root.right.left)
        print(self.root.right.right)
        print("l3")
        print(self.root.left.left.left)
        print(self.root.left.left.right)
        print(self.root.left.right.left)
        print(self.root.left.right.right)
        print(self.root.right.left.left)
        print(self.root.right.left.right)
        print(self.root.right.right.left)
        print(self.root.right.right.right)

    def get_root(self):
        return self.root.hash
