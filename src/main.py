"""
Enrico Tedeschi @ UiT - Norges Arktiske Universitet, Faculty of Computer Science.
enrico.tedeschi@uit.no

INF 3203 - Advanced Distributed Systems

Assignment 1 - Blockchain Mining Competition

Usage:
        -h                  : display usage information
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
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from consensus import POW

from utils.flask_utils import flask_call
from abstractions.block import Blockchain
from server import BLOCK_PROPOSAL, REQUEST_DIFFICULTY, GET_BLOCKCHAIN, ADDRESS, PORT, GET_USERS, REQUEST_TXS
from utils.view import visualize_blockchain, visualize_blockchain_terminal, create_visualization_table

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
                difficulty, table, code = flask_call('GET', REQUEST_DIFFICULTY)
                _, txs, code = flask_call('GET', REQUEST_TXS)
                _, blockchain, code = flask_call('GET', GET_BLOCKCHAIN)
                if blockchain:
                    b_chain = Blockchain.load_json(json.dumps(blockchain))
                    prev_hash = b_chain.get_last_block().hash #???
                    timestamp = b_chain.get_last_block().timestamp #???
                proposed_block = POW(txs, prev_hash, timestamp, difficulty)
                response, _, _ = flask_call('POST', BLOCK_PROPOSAL, proposed_block)
                print(response)
                valid_args = True
            if opt == "-i":
                if arg == "b":
                    _, blockchain, code = flask_call('GET', GET_BLOCKCHAIN)
                    if blockchain:
                        b_chain = Blockchain.load_json(json.dumps(blockchain))
                        # table = create_visualization_table(b_chain.block_list)
                        print(b_chain) #might need to use some views stuff to visualize better
                    valid_args = True
                elif arg == "u":
                    _, users, code = flask_call('GET', GET_USERS)
                    if users:
                        field_names = ["username", "address", "balance (BTC)", "mined blocks", "confirmed blocks", "reward (BTC)"]
                        table = create_visualization_table(field_names, users, "Users INFO")
                        print(users) #might need to use some views stuff to visualize better
                    valid_args = True
                else:
                    valid_args = False
            if opt == "-t":
                _, txs, code = flask_call('GET', REQUEST_TXS)
                if txs:
                    # table = create_visualization_table(txs)
                    print(txs) #might need to use some views stuff to visualize better
                valid_args = True
            if opt == "-v":
                if arg == "b":
                    _, blockchain, code = flask_call('GET', GET_BLOCKCHAIN)
                    if blockchain:
                        b_chain = Blockchain.load_json(json.dumps(blockchain))
                        # saves the blockchain as pdf in "vis/blockchain/blockchain.pdf"
                        visualize_blockchain(b_chain.block_list, n_blocks=40)
                        visualize_blockchain_terminal(b_chain.block_list, n_blocks=40)
                    valid_args = True
            if opt == "-d":
                response, table, code = flask_call('GET', REQUEST_DIFFICULTY)
                print(response)
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
    url = 'https://' + ADDRESS + ':' + PORT + '/'
    response = requests.get(url, verify=False)
    return response

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    main(sys.argv[1:])