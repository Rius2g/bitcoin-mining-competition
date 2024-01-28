# backbone/consensus.py
from utils.cryptographic import hash_function
from merkle import MerkleTree
from block import Block


def POW(txs, prev_hash, timestamp, DIFFICULTY):
    Nonece = 0
    Tree = MerkleTree(txs)
    block_header = Tree.root.hash + prev_hash + timestamp

    while True:
        hash = hash_function(block_header + Nonece)
        double_hash = hash_function(hash)
        if double_hash.startswith(DIFFICULTY * "0"):
            return build_block()
        Nonece += 1

def build_block():
    return Block() #send in params
    
    pass


