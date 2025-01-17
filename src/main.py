"""
Enrico Tedeschi @ UiT - Norges Arktiske Universitet, Faculty of Computer Science.
enrico.tedeschi@uit.no

INF 3203 - Advanced Distributed Systems

Assignment 1 - Blockchain Mining Competition

Usage:
        -h                  : display usage information
        -i [b, u]           : display information for blocks or users   
        -t                  : request N transactions                    
        -m                  : mine a block                              
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
from abstractions.user import User
from server import (
    BLOCK_PROPOSAL,
    REQUEST_DIFFICULTY,
    GET_BLOCKCHAIN,
    ADDRESS,
    PORT,
    GET_USERS,
    REQUEST_TXS,
    GET_DATABASE,
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

        valid_args = False
        for opt, arg in opts:
            if opt == "-h":  # usage
                print(__doc__)
                valid_args = True
                break
            if opt == "-m":  # Check if the option is to mine a block
                # Retrieve the blockchain from the server
                _, blockchain, code = flask_call("GET", GET_BLOCKCHAIN)
                if blockchain:
                    # Load the blockchain from JSON format
                    b_chain = Blockchain.load_json(json.dumps(blockchain))

                # Retrieve transactions from the server
                _, txs, code = flask_call("GET", REQUEST_TXS)
                # Load transactions from JSON format
                transactions = [Transaction.load_json(json.dumps(tx)) for tx in txs]

                # Create a proposed block using Proof of Work (PoW)
                block = b_chain.block_list[0]
                for b in b_chain.block_list:
                    if b.height > block.height:
                        block = b

                proposed_block = POW(block, transactions)
                # Send the proposed block to the server
                response, _, _ = flask_call("POST", BLOCK_PROPOSAL, proposed_block)
                # Print the server's response
                print(response)

                # Set flag to indicate valid arguments
                valid_args = True

            if opt == "-i":
                if arg == "b":
                    msg, blockchain, code = flask_call("GET", GET_BLOCKCHAIN)
                    if blockchain:
                        print(msg)
                    valid_args = True
                elif arg == "u":
                    msg, users, code = flask_call("GET", GET_USERS)
                    if users:
                        print(msg)
                    valid_args = True
                else:
                    valid_args = False
            if opt == "-t":
                msg, txs, code = flask_call("GET", REQUEST_TXS)
                if txs:
                    print(msg)
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
