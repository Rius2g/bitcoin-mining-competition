# backbone/consensus.py
from utils.cryptographic import double_hash
from block import Block


def POW(merkelRoot, prev_hash, timestamp, DIFFICULTY):
    Nonece = 0
    block_header = merkelRoot + prev_hash + timestamp

    while True:
        hash = double_hash(block_header + Nonece)
        if hash.startswith(DIFFICULTY * "0"):
            # return build_block()
            return True
        Nonece += 1

# def build_block():
#     return Block() #send in params


