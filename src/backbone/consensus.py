# backbone/consensus.py
from utils.cryptographic import double_hash
from abstractions.block import Block
from backbone.merkle import MerkleTree
import datetime
from abstractions.transaction import Transaction
from utils.cryptographic import load_signature, load_private
import rsa
import json


def POW(Prev_block: Block, Txs: list[Transaction], DIFFICULTY) -> Block:
    hashes = []
    for tx in Txs:
        hashes.append(tx.hash)
    Count = 1
    Nonce = str(Count)
    MerkTree = MerkleTree(hashes)

    block_header = str(MerkTree.root) + str(Prev_block.hash) + str(Prev_block.time)

    while True:
        hash = double_hash(block_header + Nonce)
        if hash.startswith(DIFFICULTY * "0"):
            return build_block(Prev_block, Nonce, hash, Txs, MerkTree.get_root())
        Count += 1
        Nonce = str(Count)


def GetPrivateKey():
    file = open("../vis/users/hmm112_pvk.pem", "r")
    return file.read()


def build_block(Prev_block: Block, Nonce, Hash, Txs, MerkRoot):
    Transaction_list = []
    for tx in Txs:
        Transaction_list.append(tx.to_dict())
    time = datetime.datetime.now().timestamp()
    sign = rsa.sign(Hash.encode(), load_private(GetPrivateKey()), "SHA-1")
    return {
        "previous_block": Prev_block.hash,
        "nonce": Nonce,
        "time": time,
        "creation_time": time,
        "hash": Hash,
        "transactions": Transaction_list,
        "merkle_root": MerkRoot,
        "height": Prev_block.height + 1,
        "signature": sign.decode("utf-8"),
    }
