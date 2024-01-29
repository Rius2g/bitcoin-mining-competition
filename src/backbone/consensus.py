# backbone/consensus.py
from utils.cryptographic import double_hash
from abstractions.block import Block
import datetime


def POW(Prev_block:Block, Txs, DIFFICULTY) -> Block:
    #how to check if main chain or not?
    Count = 0
    Nonce = str(Count)
    block_header = str(Prev_block.merkle_root) + str(Prev_block.hash) + str(Prev_block.time)

    while True:
        hash = double_hash(block_header + Nonce)
        if hash.startswith(DIFFICULTY * "0"):
            return build_block(Prev_block, Nonce, datetime.datetime.now(), hash, Txs)
        Count += 1
        Nonce = str(Count)


def build_block(Prev_block:Block, Nonce, Time, Hash, Txs):
    return Block(Hash, Nonce, Time, Time, 
                 height=Prev_block.height+1, previous_block=Prev_block, transactions=Txs)
