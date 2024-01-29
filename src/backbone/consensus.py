# backbone/consensus.py
from utils.cryptographic import double_hash
from abstractions.block import Block
from backbone.merkle import MerkleTree
import datetime
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
            return build_block(Prev_block, Nonce, hash, Txs, MerkTree.get_root())
        Count += 1
        Nonce = str(Count)


def build_block(Prev_block:Block, Nonce, Hash, Txs, MerkRoot):
    Transaction_list = []
    for tx in Txs:
        Transaction_list.append(tx.to_dict())
    time = datetime.datetime.now().timestamp()
    return {
        "prev_block": Prev_block.hash,
        "nonce": Nonce,
        "time": time,
        "hash": Hash,
        "transactions": Transaction_list,
        "merkle_root": MerkRoot,
        "height": Prev_block.height + 1
    }
