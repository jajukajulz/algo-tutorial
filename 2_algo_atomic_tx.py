# Description - Interact with Algorand blockchain using the Python SDK py-algorand-sdk
# Before running, make sure you have installed py-algorand-sdk i.e. pip3 install py-algorand-sdk
# Usage - $ python 2_algo_atomic_tx.py

import json

from typing import Dict, Any
from base64 import b64decode

from algosdk import account, mnemonic
from algosdk import transaction
from algosdk.v2client import algod

# generate 3 random accounts, each with a fresh private key and associated account address
account_1_private_key, account_1_address = account.generate_account()
account_2_private_key, account_2_address = account.generate_account()
account_3_private_key, account_3_address = account.generate_account()

print(f"Account 1 Base64 encoded private key: {account_1_private_key}")
print(f"Account 1 Address: {account_1_address}")

print(f"Account 2 Base64 encoded private key: {account_2_private_key}")
print(f"Account 2 Address: {account_2_address}")

print(f"Account 3 Base64 encoded private key: {account_3_private_key}")
print(f"Account 3 Address: {account_3_address}")

user_input = input(
    "Now go to Algorand testnet dispenser (https://bank.testnet.algorand.network) and fund account 1 and 2, then return and press enter. "
)

# Create a new algod client, configured to connect to your local sandbox or a node e.g. https://algonode.io/
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""

algod_client = algod.AlgodClient(algod_token, algod_address)

# grab suggested params from algod using client
# includes things like suggested fee and first/last valid rounds
suggested_params = algod_client.suggested_params()

account_1_info: Dict[str, Any] = algod_client.account_info(account_1_address)
print(f"Account 1 balance: {account_1_info.get('amount')} microAlgos")

account_2_info: Dict[str, Any] = algod_client.account_info(account_2_address)
print(f"Account 2 balance: {account_2_info.get('amount')} microAlgos")

account_3_info: Dict[str, Any] = algod_client.account_info(account_3_address)
print(f"Account 3 balance: {account_3_info.get('amount')} microAlgos")


# example: ATOMIC_CREATE_TXNS
# payment from account 1 to account 2
txn_1 = transaction.PaymentTxn(
    account_1_address, suggested_params, account_2_address, 100000
)

# payment from account 2 to account 1
txn_2 = transaction.PaymentTxn(
    account_2_address, suggested_params, account_1_address, 200000
)
# example: ATOMIC_CREATE_TXNS


# example: ATOMIC_GROUP_TXNS
# Assign group id to the transactions (order matters!)
transaction.assign_group_id([txn_1, txn_2])
# Or, equivalently
# get group id and assign it to transactions
# gid = transaction.calculate_group_id([txn_1, txn_2])
# txn_1.group = gid
# txn_2.group = gid
# example: ATOMIC_GROUP_TXNS

# example: ATOMIC_GROUP_SIGN
# sign transactions
stxn_1 = txn_1.sign(account_1_private_key)
stxn_2 = txn_2.sign(account_2_private_key)
# example: ATOMIC_GROUP_SIGN

# example: ATOMIC_GROUP_ASSEMBLE
# combine the signed transactions into a single list
signed_group = [stxn_1, stxn_2]
# example: ATOMIC_GROUP_ASSEMBLE

# example: ATOMIC_GROUP_SEND

# Only the first transaction id is returned
tx_id = algod_client.send_transactions(signed_group)

# wait for confirmation
result: Dict[str, Any] = transaction.wait_for_confirmation(algod_client, tx_id, 4)
print(f"txID: {tx_id} confirmed in round: {result.get('confirmed-round', 0)}")
# example: ATOMIC_GROUP_SEND
