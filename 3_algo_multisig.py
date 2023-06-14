# Description - Interact with Algorand blockchain using the Python SDK py-algorand-sdk
# Before running, make sure you have installed py-algorand-sdk i.e. pip3 install py-algorand-sdk
# Usage - $ python 3_algo_multisig.py

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


# example: MULTISIG_CREATE
version = 1  # multisig version
threshold = 2  # how many signatures are necessary
# create a Multisig given the set of participants and threshold
msig = transaction.Multisig(
    version,
    threshold,
    [account_1_address, account_2_address, account_3_address],
)
print("Multisig Address: ", msig.address())
# example: MULTISIG_CREATE

sp = algod_client.suggested_params()
ptxn = transaction.PaymentTxn(account_1_address, sp, msig.address(), int(1e5)).sign(
    account_1_private_key
)
txid = algod_client.send_transaction(ptxn)
transaction.wait_for_confirmation(algod_client, txid, 4)
# dont check response, assume it worked

# example: MULTISIG_SIGN
msig_pay = transaction.PaymentTxn(
    msig.address(),
    sp,
    account_1_address,
    0,
    close_remainder_to=account_1_address,
)
msig_txn = transaction.MultisigTransaction(msig_pay, msig)
msig_txn.sign(account_2_private_key)
msig_txn.sign(account_3_private_key)
txid = algod_client.send_transaction(msig_txn)
result = transaction.wait_for_confirmation(algod_client, txid, 4)
print(f"Payment made from msig account confirmed in round {result['confirmed-round']}")
# example: MULTISIG_SIGN
