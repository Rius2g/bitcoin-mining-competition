"""
Enrico Tedeschi @ UiT - Norges Arktiske Universitet, Faculty of Computer Science.
enrico.tedeschi@uit.no

INF 3203 - Advanced Distributed Systems

Assignment 1 - Blockchain Mining Competition

Usage:
        -h                  : display usage information
        -i [b, u]           : display information for blocks or users   
        -t                  : request N transactions                    
        -m                  : mine a block                              #TODO
        -v b                : visualize blockchain, saved to vis/blockchain/blockchain.pdf
        -d                  : request DIFFICULTY level
"""
__author__ = "Enrico Tedeschi"
__copyright__ = "Copyright (C) 2023 Enrico Tedeschi"
__license__ = "GNU General Public License."
__version__ = "v1.0"

import sys
import getopt
import random
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from utils.flask_utils import flask_call
from abstractions.block import Blockchain
from server import (
    BLOCK_PROPOSAL,
    REQUEST_DIFFICULTY,
    GET_BLOCKCHAIN,
    ADDRESS,
    PORT,
    GET_USERS,
    REQUEST_TXS,
    DIFFICULTY,
)
from utils.view import (
    visualize_blockchain,
    visualize_blockchain_terminal,
)
from backbone.consensus import POW
from abstractions.transaction import Transaction


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:tmdv:")
        # print(f'opts : {opts}\nargs : {args}')
        valid_args = False
        for opt, arg in opts:
            if opt == "-h":  # usage
                print(__doc__)
                valid_args = True
                break
            if opt == "-m":  # mine block
                _, blockchain, code = flask_call("GET", GET_BLOCKCHAIN)
                _, txs, code = flask_call("GET", REQUEST_TXS)
                transactions = []
                for tx in txs:
                    transactions.append(Transaction.load_json(json.dumps(tx)))
                if blockchain:
                    b_chain = Blockchain.load_json(json.dumps(blockchain))
                    count = 1
                    prev_block = b_chain.block_list[len(b_chain.block_list)-count]
                    while prev_block.confirmed != True & prev_block.main_chain != True: #iterate over list to find confirmed and main chain
                        count += 1
                        prev_block = b_chain.block_list[len(b_chain.block_list) - count]
                proposed_block = POW(prev_block, transactions)
                # print(proposed_block)
                response, _, _ = flask_call("POST", BLOCK_PROPOSAL, proposed_block)
                print(response)
                valid_args = True
            if opt == "-i":
                if arg == "b":
                    _, blockchain, code = flask_call("GET", GET_BLOCKCHAIN)
                    if blockchain:
                        print(_)
                    valid_args = True
                elif arg == "u":
                    _, users, code = flask_call("GET", GET_USERS)
                    if users:
                        print(_)
                    valid_args = True
                else:
                    valid_args = False
            if opt == "-t":
                _, txs, code = flask_call("GET", REQUEST_TXS)
                if txs:
                    print(_)
                valid_args = True
            if opt == "-v":
                if arg == "b":
                    _, blockchain, code = flask_call("GET", GET_BLOCKCHAIN)
                    if blockchain:
                        b_chain = Blockchain.load_json(json.dumps(blockchain))
                        # saves the blockchain as pdf in "vis/blockchain/blockchain.pdf"
                        visualize_blockchain(b_chain.block_list, n_blocks=40)
                        visualize_blockchain_terminal(b_chain.block_list, n_blocks=40)
                    valid_args = True
            if opt == "-d":
                response, table, code = flask_call("GET", REQUEST_DIFFICULTY)
                print(table)
                valid_args = True
        if valid_args is False:
            print(__doc__)
    except getopt.GetoptError:
        print(__doc__)
        sys.exit(2)
    except ValueError as e:
        print(e)
        print(__doc__)
        sys.exit(2)  # exit due to misuse of shell/bash --> check documentation
    except KeyboardInterrupt as e:
        print(e)


def connect_to_server():
    """

    :return:
    """
    url = "https://" + ADDRESS + ":" + PORT + "/"
    response = requests.get(url, verify=False)
    return response


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    main(sys.argv[1:])
