# backbone/consensus.py
from utils.cryptographic import double_hash
from abstractions.block import Block
from backbone.merkle import MerkleTree
import datetime
from abstractions.transaction import Transaction
from utils.cryptographic import load_private
import rsa
import base64
from server.__init__ import SELF, DIFFICULTY


def POW(Prev_block: Block, Txs: list[Transaction]) -> Block:
    hashes = [tx.hash for tx in Txs]
    Nonce = 1
    MerkTree = MerkleTree(hashes)
    time = str(datetime.datetime.now().timestamp())
    merk_root = MerkTree.get_root()
    block_header = merk_root + Prev_block.hash + time


    while True:
        hash = double_hash(block_header + str(Nonce))
        if hash.startswith(DIFFICULTY * "0"):
            return build_block(Prev_block, Nonce, hash, Txs, merk_root, time)
        Nonce += 1


def GetPrivateKey():
    file = open("../vis/users/hmm112_pvk.pem", "r")
    return file.read()


def build_block(Prev_block: Block, Nonce, Hash, Txs, MerkRoot, timestamp):
    sign = base64.b64encode(rsa.sign(Hash.encode(), load_private(GetPrivateKey()), "SHA-1")).decode()

    return {
        "previous_block": Prev_block.hash,
        "nonce": Nonce,
        "time": timestamp,
        "creation_time": timestamp,
        "hash": Hash,
        "transactions": [t.to_dict() for t in Txs],
        "merkle_root": MerkRoot,
        "height": Prev_block.height + 1,
        "signature": str(sign),
        "prev": Prev_block.hash,
        "main_chain": True,
        "confirmed": True,
        "next": [],
        "mined_by": SELF
    }
