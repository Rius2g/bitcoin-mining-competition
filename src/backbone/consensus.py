# backbone/consensus.py
from utils.cryptographic import double_hash
from abstractions.block import Block
import datetime
from backbone.merkle import MerkleTree
from utils.cryptographic import load_private, load_public, save_key, save_signature, verify_signature, load_signature
from abstractions.transaction import Transaction


def POW(Prev_block:Block, Txs: list[Transaction], DIFFICULTY) -> Block:
    hashes = []
    for tx in Txs:
        hashes.append(
            tx.hash)
    Count = 0
    Nonce = str(Count)
    MerkTree = MerkleTree(hashes)

    block_header = str(MerkTree.root) + str(Prev_block.hash) + str(Prev_block.time)

    while True:
        hash = double_hash(block_header + Nonce)
        if hash.startswith(DIFFICULTY * "0"):
            return build_block(Prev_block, Nonce, datetime.datetime.now(), hash, Txs, MerkTree.root)
        Count += 1
        Nonce = str(Count)


def build_block(Prev_block:Block, Nonce, Time, Hash, Txs, MerkRoot):
    return Block(hash=Hash, nonce=Nonce, time=Time, creation_time=Time, 
                 height=Prev_block.height+1, 
                 transactions=Txs, merkle_root=MerkRoot) 
