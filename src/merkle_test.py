from backbone.merkle import MerkleTree


def test():
    hashes = ["a", "b", "c", "d", "e"]
    tree = MerkleTree(hashes)
    tree.print_tree()


if __name__ == "__main__":
    test()
