# Description - Interact with Algorand blockchain using the Python SDK py-algorand-sdk
# Before running, make sure you have installed py-algorand-sdk i.e. pip3 install py-algorand-sdk
# Usage - $ python 4_algo_rekey.py

import json, time

from typing import Dict, Any
from base64 import b64decode

from algosdk import account, transaction
from algosdk.v2client import algod

# setup algod client
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""

algod_client = algod.AlgodClient(algod_token, algod_address)

# generate 3 random accounts, each with a fresh private key and associated account address
account_1_private_key, account_1_address = account.generate_account()
account_2_private_key, account_2_address = account.generate_account()
account_3_private_key, account_3_address = account.generate_account()

# time.sleep(int(10))

print(f"Account 1 Base64 encoded private key: {account_1_private_key}")
print(f"Account 1 Address: {account_1_address}")

print(f"Account 2 Base64 encoded private key: {account_2_private_key}")
print(f"Account 2 Address: {account_2_address}")

print(f"Account 3 Base64 encoded private key: {account_3_private_key}")
print(f"Account 3 Address: {account_3_address}")

user_input = input(
    "Now go to Algorand testnet dispenser (https://bank.testnet.algorand.network) and fund account 1 then return and press enter. "
)

sp = algod_client.suggested_params()
ptxn = transaction.PaymentTxn(account_1_address, sp, msig.address(), int(1e5)).sign(
    account_1_private_key
)
txid = algod_client.send_transaction(ptxn)
transaction.wait_for_confirmation(algod_client, txid, 4)
# dont check response, assume it worked


# example: ACCOUNT_REKEY
# Any kind of transaction can contain a rekey
rekey_txn = transaction.PaymentTxn(
    account_1_address, sp, account_1_address, 0, rekey_to=account_2_address
)
signed_rekey = rekey_txn.sign(account_1_private_key)
txid = algod_client.send_transaction(signed_rekey)
result = transaction.wait_for_confirmation(algod_client, txid, 4)
print(f"rekey transaction confirmed in round {result['confirmed-round']}")

# Now we should get an error if we try to submit a transaction
# signed with account_1s private key
expect_err_txn = transaction.PaymentTxn(account_1_address, sp, account_1_address, 0)
signed_expect_err_txn = expect_err_txn.sign(account_1_private_key)
try:
    txid = algod_client.send_transaction(signed_expect_err_txn)
except Exception as e:
    print("Expected error: ", e)

# But its fine if we sign it with the account we rekeyed to
signed_expect_err_txn = expect_err_txn.sign(account_2_private_key)
txid = algod_client.send_transaction(signed_expect_err_txn)
result = transaction.wait_for_confirmation(algod_client, txid, 4)
print(f"transaction confirmed in round {result['confirmed-round']}")

# rekey account1 back to itself so we can actually use it later
rekey_txn = transaction.PaymentTxn(
    account_1_address, sp, account_1_address, 0, rekey_to=account_1_address
)
signed_rekey = rekey_txn.sign(account_2_private_key)
txid = algod_client.send_transaction(signed_rekey)
result = transaction.wait_for_confirmation(algod_client, txid, 4)
print(f"rekey transaction confirmed in round {result['confirmed-round']}")
# example: ACCOUNT_REKEY
