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
        self.root = None
        self.build_tree(hashes)

    def build_tree(self, hashes):
        leaves = [
            MerkelNode(None, None, hash_function(hash_val)) for hash_val in hashes
        ]

        self.root = self._build_tree(leaves)

    def _build_tree(self, nodes):
        if len(nodes) == 1:
            return nodes[0]

        while len(nodes) > 1:
            if len(nodes) % 2 != 0:
                nodes.append(nodes[-1])

            new_level = []
            for i in range(0, len(nodes) - 1, 2):
                left = nodes[i]
                right = nodes[i + 1] if i + 1 < len(nodes) else None

                new_node = MerkelNode(
                    left,
                    right,
                    hash_function(left.hash + (right.hash if right else left.hash)),
                )
                new_level.append(new_node)
            nodes = new_level

        return nodes[0]

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
