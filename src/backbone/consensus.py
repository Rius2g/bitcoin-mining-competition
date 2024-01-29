# backbone/consensus.py
from utils.cryptographic import double_hash


def POW(merkelRoot, prev_hash, timestamp, DIFFICULTY):
    Count = 0
    Nonce = str(Count)
    block_header = str(merkelRoot) + str(prev_hash) + str(timestamp)

    while True:
        hash = double_hash(block_header + Nonce)
        if hash.startswith(DIFFICULTY * "0"):
            # return build_block()
            return True
        Count += 1
        Nonce = str(Count)


# def build_block():
#     return Block() #send in params
