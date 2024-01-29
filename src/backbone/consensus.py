# backbone/consensus.py
from utils.cryptographic import double_hash
from abstractions.block import Block
import datetime
from backbone.merkle import MerkleTree


def POW(Prev_block:Block, Txs, DIFFICULTY) -> Block:
    #how to check if main chain or not?
    Count = 0
    Nonce = str(Count)
    MerkTree = MerkleTree(Txs)
    block_header = str(MerkTree.root) + str(Prev_block.hash) + str(Prev_block.time)

    while True:
        hash = double_hash(block_header + Nonce)
        if hash.startswith(DIFFICULTY * "0"):
            return build_block(Prev_block, Nonce, datetime.datetime.now(), hash, Txs, MerkTree.root, )
        Count += 1
        Nonce = str(Count)


def build_block(Prev_block:Block, Nonce, Time, Hash, Txs, MerkRoot):
    #     def __init__(
    #     self,
    #     hash,
    #     nonce,
    #     time,
    #     creation_time, #missing
    #     height,
    #     previous_block=None,
    #     transactions=None,
    #     main_chain=True, #missing
    #     confirmed=False, #missing
    #     merkle_root=None,
    #     next=[], #missing
    #     mined_by=None,
    #     signature=None, #missing
    # ):

    return Block(Hash, Nonce, Time, Time, 
                 height=Prev_block.height+1, previous_block=Prev_block, 
                 transactions=Txs, MerkRoot=MerkRoot, mined_by="hmm112") #need to add signature
