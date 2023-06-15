# Description - Interact with Algorand blockchain using the Python SDK py-algorand-sdk
# Before running, make sure you have installed py-algorand-sdk i.e. pip3 install py-algorand-sdk
# Usage - $ python 4_algo_rekey.py

import json, time

from typing import Dict, Any
from base64 import b64decode

from algosdk import account, transaction, mnemonic
from algosdk.v2client import algod

# setup algod client
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""

algod_client = algod.AlgodClient(algod_token, algod_address)
sp = algod_client.suggested_params()

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
    "Now go to Algorand testnet dispenser (https://bank.testnet.algorand.network) and fund account 1 then return and press enter. "
)

# example: ACCOUNT_REKEY
# Any kind of transaction can contain a rekey
rekey_txn = transaction.PaymentTxn(
    account_1_address, sp, account_1_address, 0, rekey_to=account_2_address
)
signed_rekey = rekey_txn.sign(account_1_private_key)
txid = algod_client.send_transaction(signed_rekey)
result = transaction.wait_for_confirmation(algod_client, txid, 4)
print(f"rekey transaction confirmed in round {result['confirmed-round']}")

user_input = input(
    "Now we should get an error if we try to submit a transaction from account 1 \
    and signed with account_1s private key. Press enter to continue... "
)

# Now we should get an error if we try to submit a transaction
# signed with account_1s private key
expect_err_txn = transaction.PaymentTxn(account_1_address, sp, account_1_address, 0)
signed_expect_err_txn = expect_err_txn.sign(account_1_private_key)
try:
    txid = algod_client.send_transaction(signed_expect_err_txn)
except Exception as e:
    print("Expected error: ", e)

user_input = input(
    "Now we should NOT get an error if we try to submit a transaction from account 1 \
    and sign with account_2s private key. Press enter to continue... "
)

# But its fine if we sign it with the account we rekeyed to
signed_expect_err_txn = expect_err_txn.sign(account_2_private_key)
txid = algod_client.send_transaction(signed_expect_err_txn)
result = transaction.wait_for_confirmation(algod_client, txid, 4)
print(f"transaction confirmed in round {result['confirmed-round']}")

user_input = input(
    "Now we rekey account 1 back to using its own private key i.e. account 1 private key.\
          Press enter to continue... "
)

# rekey account1 back to itself so we can actually use it later
rekey_txn = transaction.PaymentTxn(
    account_1_address, sp, account_1_address, 0, rekey_to=account_1_address
)
signed_rekey = rekey_txn.sign(account_2_private_key)
txid = algod_client.send_transaction(signed_rekey)
result = transaction.wait_for_confirmation(algod_client, txid, 4)
print(f"rekey transaction confirmed in round {result['confirmed-round']}")
# example: ACCOUNT_REKEY
