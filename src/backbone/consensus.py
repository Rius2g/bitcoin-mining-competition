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
    # Sort transactions by time
    start = datetime.datetime.now().timestamp()
    Txs = sorted(Txs, key=lambda tx: tx.time)
    # Create a list of transaction hashes
    hashes = [tx.hash for tx in Txs]

    # Initialize nonce
    Nonce = 1

    # Create a Merkle Tree
    MerkTree = MerkleTree(hashes)

    # Get current time
    time = str(datetime.datetime.now().timestamp())

    # Get the Merkle root
    merk_root = MerkTree.get_root()

    # Construct the block header
    block_header = Prev_block.hash + time + merk_root

    # Perform Proof of Work
    while True:
        hash = double_hash(block_header + str(Nonce))

        # Check if the hash meets the required difficulty
        if hash.startswith(DIFFICULTY * "0"):
            # If so, build the block
            return build_block(Prev_block, Nonce, hash, Txs, merk_root, time, start)

        # Increment the nonce
        Nonce += 1


def GetPrivateKey():
    # Open the private key file and return its content
    file = open("../vis/users/hmm112_pvk.pem", "r")
    return file.read()


def build_block(Prev_block: Block, Nonce, Hash, Txs, MerkRoot, timestamp, start):
    # Sign the block hash
    sign = base64.b64encode(
        rsa.sign(Hash.encode(), load_private(GetPrivateKey()), "SHA-1")
    ).decode()

    # Construct the block object
    return {
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
