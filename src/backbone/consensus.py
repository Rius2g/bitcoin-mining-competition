# backbone/consensus.py
from utils.cryptographic import double_hash
from abstractions.block import Block
from backbone.merkle import MerkleTree
import datetime

from abstractions.transaction import Transaction
from utils.cryptographic import load_private, verify_signature
import rsa
import base64
from server.__init__ import SELF, DIFFICULTY

def Transaction_approval(Db, Txs: list[Transaction]):
    # spent_outputs = set()

    valid_txs = []

    for tx in Txs:
        # if not verify_signature(tx.hash, tx.prev_owner_sig, tx.receiver_pub):
        #     continue

        valid = False
        for user in Db:
            if user.address == tx.source_address:
                if user.balance < tx.amount:
                    break
            else:
                user.balance -= tx.amount
                valid = True
                break 

        if valid: #will only approve transactions where the source address has enough balance and the signature is verified
            for user in Db:
                if user.address == tx.destination_address:
                    user.balance += tx.amount
                    tx.is_verified = True
                    valid_txs.append(tx)
                    break

    return valid_txs

def POW(Db, Prev_block: Block, Txs: list[Transaction]) -> Block:
    # before taking hashes we check transactions and verify them and remove invalid transactions
    Txs = sorted(Txs, key=lambda tx: tx.time)
    valid_txs = Transaction_approval(Db, Txs)

            
    
    hashes = [tx.hash for tx in valid_txs]
    Nonce = 1
    MerkTree = MerkleTree(hashes)
    time = str(datetime.datetime.now().timestamp())
    merk_root = MerkTree.get_root()
    block_header = merk_root + Prev_block.hash + time


    while True:
        hash = double_hash(block_header + str(Nonce))
        if hash.startswith(DIFFICULTY * "0"):
            return build_block(Prev_block, Nonce, hash, valid_txs, merk_root, time)
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
        "creation_time": str(datetime.datetime.now().timestamp()),
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
