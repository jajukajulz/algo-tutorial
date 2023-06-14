# Description - Interact with Algorand blockchain using the Python SDK py-algorand-sdk
# Before running, make sure you have installed py-algorand-sdk i.e. pip3 install py-algorand-sdk
# Usage - $ python 6_algo_indexer.py

from algosdk.v2client import indexer
import json
import datetime

try:
    my_address = "REPLACE_ME"
    txid = "REPLACE_ME"
    asset_id = "REPLACE_ME"

    # Create a new indexer client, configured to connect to a node e.g. https://testnet-algorand.api.purestake.io/idx2
    # or https://testnet-idx.algonode.cloud
    indexer_address = "https://testnet-idx.algonode.cloud"
    indexer_token = ""
    headers = ""
    indexer_client = indexer.IndexerClient(indexer_token, indexer_address, headers)

    user_input = input("Press enter to proceed to indexer search for transactions by ID example...")

    # example: INDEXER_SEARCH_TRANSACTIONS_BY_ID
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
    # example: INDEXER_SEARCH_TRANSACTIONS_BY_ID

    user_input = input("Press enter to proceed to indexer search for transactions on address example...")

    # example: INDEXER_SEARCH_TRANSACTIONS_FOR_ADDRESS
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
    # example: INDEXER_SEARCH_TRANSACTIONS_FOR_ADDRESS

    user_input = input("Press enter to proceed to indexer asset lookup example...")

    # example: INDEXER_LOOKUP_ASSET
    # lookup a single asset, by passing include_all, we specify that we want to see deleted assets as well
    response = indexer_client.asset_info(asset_id, include_all=True)
    print(f"Asset Info: {json.dumps(response, indent=2, )}")
    # example: INDEXER_LOOKUP_ASSET

    user_input = input("Press enter to proceed to indexer transaction search filtered by minimum amount example...")

    # example: INDEXER_SEARCH_MIN_AMOUNT
    response = indexer_client.search_transactions(
        min_amount=10, min_round=1000, max_round=1500, address=my_address
    )
    print(f"Transaction results: {json.dumps(response, indent=2)}")
    # example: INDEXER_SEARCH_MIN_AMOUNT

    user_input = input("Press enter to proceed to indexer pagination example...")

    # example: INDEXER_PAGINATE_RESULTS

    nexttoken = ""
    has_results = True
    page = 0

    # loop using next_page to paginate until there are
    # no more transactions in the response
    while has_results:
        response = indexer_client.search_transactions(
            min_amount=10, min_round=1000, max_round=1500, next_page=nexttoken, address=my_address
        )

        has_results = len(response["transactions"]) > 0

        if has_results:
            nexttoken = response["next-token"]
            print(f"Tranastion on page {page}: " + json.dumps(response, indent=2))

        page += 1
    # example: INDEXER_PAGINATE_RESULTS

    user_input = input("Press enter to proceed to indexer prefix search...")

    # example: INDEXER_PREFIX_SEARCH
    note_prefix = "showing prefix".encode()
    response = indexer_client.search_transactions(note_prefix=note_prefix)
    print(f"result: {json.dumps(response, indent=2)}")
    # example: INDEXER_PREFIX_SEARCH

except Exception as e:
    print(e)
