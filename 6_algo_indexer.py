# Description - Interact with Algorand blockchain using the Python SDK py-algorand-sdk
# Before running, make sure you have installed py-algorand-sdk i.e. pip3 install py-algorand-sdk
# Usage - $ python 6_algo_indexer.py

from algosdk.v2client import indexer
import json
import datetime

try:
    my_address = "REPLACE_ME"
    txid = "REPLACE_ME"

    # Create a new indexer client, configured to connect to a node e.g. https://testnet-algorand.api.purestake.io/idx2
    # or https://testnet-idx.algonode.cloud
    indexer_address = "https://testnet-idx.algonode.cloud"
    indexer_token = ""
    headers = ""
    indexer_client = indexer.IndexerClient(indexer_token, indexer_address, headers)

    # Read the transaction by ID
    try:
        txn1 = indexer_client.transaction(txid)
        if txn1 is not None:
            print("Transaction information tx1: {}".format(json.dumps(txn1, indent=4)))
        else:
            print("Transaction not found")
        # indexer search by address search_transactions_by_address
    except Exception as err:
        print(err)


    # Read the transactions by address
    try:
        txn_list = indexer_client.search_transactions_by_address(my_address)
        # txn_list["transactions"], txn_list["current-round"], txn_list["next-token"]

        if txn_list is not None:
            print(f'Number of transactions found: {len(txn_list["transactions"])}')

            for txn in txn_list["transactions"]:
                print("Transaction information tx: {}".format(json.dumps(txn, indent=4)))
        else:
            print("Transaction not found")
    except Exception as err:
        print(err)

except Exception as e:
    print(e)
