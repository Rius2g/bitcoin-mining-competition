from utils.cryptographic import hash_function


class MerkelNode:
    def __init__(self, left, right, hash):
        # Initialize MerkelNode with left and right children nodes and its hash value
        self.left: MerkelNode = left
        self.right: MerkelNode = right
        self.hash = hash

    def __str__(self):
        # Return a string representation of MerkelNode
        return f"Node: {self.hash}, left: {self.left.hash if self.left != None else None}, right: {self.right.hash if self.left != None else None}\n"


class MerkleTree:
    def __init__(self, hashes):  # list of hashes for transactions
        # Initialize MerkleTree with root node as None and build the tree
        self.root = None
        self.build_tree(hashes)

    def build_tree(self, hashes):
        # Build the Merkle tree from the list of transaction hashes
        leaves = [
            MerkelNode(None, None, hash_function(hash_val)) for hash_val in hashes
        ]

        self.root = self._build_tree(leaves)

    def _build_tree(self, nodes):
        # Recursively build the Merkle tree from the list of nodes

        # Base case: If there's only one node, return it
        if len(nodes) == 1:
            return nodes[0]

        # Continue building the tree until there's only one root node
        while len(nodes) > 1:
            # If the number of nodes is odd, duplicate the last node
            if len(nodes) % 2 != 0:
                nodes.append(nodes[-1])

            new_level = []
            # Iterate over nodes in pairs to create parent nodes
            for i in range(0, len(nodes) - 1, 2):
                left = nodes[i]
                right = nodes[i + 1] if i + 1 < len(nodes) else None

                # Create a new node with the combined hash of its children
                new_node = MerkelNode(
                    left,
                    right,
                    hash_function(left.hash + (right.hash if right else left.hash)),
                )
                new_level.append(new_node)

            # Update nodes to the new level of parent nodes
            nodes = new_level

        # Return the root node of the Merkle tree
        return nodes[0]

    def print_tree(self):
        # Print the Merkle tree (for debugging purposes)
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
        # Return the root hash of the Merkle tree
        return self.root.hash
