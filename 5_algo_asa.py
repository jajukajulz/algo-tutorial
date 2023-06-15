# Description - Interact with Algorand blockchain using the Python SDK py-algorand-sdk
# Before running, make sure you have installed py-algorand-sdk i.e. pip3 install py-algorand-sdk
# Usage - $ python 5_algo_asa.py

import json

from typing import Dict, Any
from base64 import b64decode

from algosdk import account, mnemonic
from algosdk import transaction
from algosdk.v2client import algod


MY_PERA_ADDRESS = "REPLACE_ME"

# example: ACCOUNT_RECOVER_MNEMONIC
account_1_mnemonic = "REPLACE_ME"
account_1_private_key = mnemonic.to_private_key(account_1_mnemonic)
print(f"Base64 encoded private key: {account_1_private_key}")
account_1_address = account.address_from_private_key(account_1_private_key)

print(f"Account 1 Base64 encoded private key: {account_1_private_key}")
print(f"Account 1 Address: {account_1_address}")

account_2_mnemonic = "REPLACE_ME"
account_2_private_key = mnemonic.to_private_key(account_2_mnemonic)
print(f"Base64 encoded private key: {account_2_private_key}")
account_2_address = account.address_from_private_key(account_2_private_key)

print(f"Account 2 Base64 encoded private key: {account_2_private_key}")
print(f"Account 2 Address: {account_2_address}")

account_3_mnemonic = "REPLACE_ME"
account_3_private_key = mnemonic.to_private_key(account_3_mnemonic)
print(f"Base64 encoded private key: {account_3_private_key}")
account_3_address = account.address_from_private_key(account_3_private_key)

print(f"Account 3 Base64 encoded private key: {account_3_private_key}")
print(f"Account 3 Address: {account_3_address}")
# example: ACCOUNT_RECOVER_MNEMONIC

user_input = input(
    "Now go to Algorand testnet dispenser (https://bank.testnet.algorand.network) and fund account 3, then return and press enter. "
)

# Create a new algod client, configured to connect to your local sandbox or a node e.g. https://algonode.io/
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""

algod_client = algod.AlgodClient(algod_token, algod_address)
params = algod_client.suggested_params()

# example: CREATE ASSET
# grab suggested params from algod using client
# includes things like suggested fee and first/last valid rounds

# Account 1 creates an asset called Ariary Digital (i.e. Madagascar) and
# sets Account 2 as the manager, reserve, freeze, and clawback address.
# Asset Creation transaction
unsigned_txn = transaction.AssetConfigTxn(
    sender=account_1_address,
    sp=params,
    total=1000,
    default_frozen=False,
    unit_name="ArD",
    asset_name="Ariary Digital",
    manager=account_2_address,
    reserve=account_2_address,
    freeze=account_2_address,
    clawback=account_2_address,
    url="https://path/to/my/asset/details",
    decimals=0,
)

# example: ASSET_CREATE

# example: ASSET_CREATE_SIGN
# sign the transaction with private key of creator
signed_txn = unsigned_txn.sign(account_1_private_key)
# example: ASSET_CREATE_SIGN

# example: ASSET_CREATE_SUBMIT
# submit the transaction and get back a transaction id

# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    asset_id = confirmed_txn["asset-index"]
    confirmed_round = confirmed_txn["confirmed-round"]

    print("TXID: ", txid)
    print("Asset ID: {}".format(asset_id))
    print("Result confirmed in round: {}".format(confirmed_round))
    print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))
except Exception as err:
    print(err)
