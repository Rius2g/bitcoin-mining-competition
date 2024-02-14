# backbone/consensus.py
from utils.cryptographic import double_hash
from abstractions.block import Block
from backbone.merkle import MerkleTree
import datetime

from abstractions.transaction import Transaction
from utils.cryptographic import load_private, verify_signature, load_public
import rsa
import base64
from server.__init__ import SELF, DIFFICULTY


def POW(Prev_block: Block, Txs: list[Transaction]) -> Block:
    # before taking hashes we check transactions and verify them and remove invalid transactions
    start = datetime.datetime.now().timestamp()
    Txs = sorted(Txs, key=lambda tx: tx.time)
    # valid_txs = Transaction_approval(Db, Txs)
    hashes = [tx.hash for tx in Txs]
    Nonce = 1
    MerkTree = MerkleTree(hashes)
    time = str(datetime.datetime.now().timestamp())
    merk_root = MerkTree.get_root()
    block_header = Prev_block.hash + time + merk_root

    while True:
        hash = double_hash(block_header + str(Nonce))
        if hash.startswith(DIFFICULTY * "0"):
            return build_block(Prev_block, Nonce, hash, Txs, merk_root, time, start)
        Nonce += 1


def GetPrivateKey():
    file = open("../vis/users/hmm112_pvk.pem", "r")
    return file.read()


def build_block(Prev_block: Block, Nonce, Hash, Txs, MerkRoot, timestamp, start):
    sign = base64.b64encode(
        rsa.sign(Hash.encode(), load_private(GetPrivateKey()), "SHA-1")
    ).decode()
    return {
        # "previous_block": Prev_block.hash,
        "nonce": Nonce,
        "time": timestamp,
        "creation_time": str(datetime.datetime.now().timestamp() - start),
        "hash": Hash,
        "transactions": [t.to_dict() for t in Txs],
        "merkle_root": MerkRoot,
        "height": Prev_block.height + 1,
        "signature": str(sign),
        "prev": Prev_block.hash,
        "main_chain": True,
        "confirmed": True,
        "next": [],
        "mined_by": SELF,
    }
