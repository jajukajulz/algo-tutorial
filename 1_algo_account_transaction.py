# Description - Interact with Algorand blockchain using the Python SDK py-algorand-sdk
# Before running, make sure you have installed py-algorand-sdk i.e. pip3 install py-algorand-sdk
# Usage - $ python 1_algo_account_transaction.py

# from utils import get_accounts, get_algod_client
import json

from typing import Dict, Any
from base64 import b64decode

from algosdk import account, mnemonic
from algosdk import transaction
from algosdk.v2client import algod


MY_PERA_ADDRESS = "GRZANBMEE3JDUGNIMR5ZGLRHJ3N3OQFJAAHNFLQZI4GJMBZYEYWKNTT3GQ"

# example: ACCOUNT_RECOVER_MNEMONIC
sender_mnemonic = "cost piano sample enough south bar diet garden nasty mystery mesh sadness convince bacon best patch surround protect drum actress entire vacuum begin abandon hair"
sender_pk = mnemonic.to_private_key(sender_mnemonic)
print(f"Base64 encoded private key: {sender_pk}")
sender_addr = account.address_from_private_key(sender_pk)
print(f"Address: {sender_addr}")
# example: ACCOUNT_RECOVER_MNEMONIC


# Create a new algod client, configured to connect to your local sandbox or a node e.g. https://algonode.io/
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""

algod_client = algod.AlgodClient(algod_token, algod_address)

account_info: Dict[str, Any] = algod_client.account_info(sender_addr)
print(f"Account balance: {account_info.get('amount')} microAlgos")

# example: TRANSACTION_PAYMENT_CREATE
# grab suggested params from algod using client
# includes things like suggested fee and first/last valid rounds
params = algod_client.suggested_params()
unsigned_txn = transaction.PaymentTxn(
    sender=sender_addr,
    sp=params,
    receiver=MY_PERA_ADDRESS,
    amt=1000000,
    note=b"Hello World",
)
# example: TRANSACTION_PAYMENT_CREATE

# example: TRANSACTION_PAYMENT_SIGN
# sign the transaction
signed_txn = unsigned_txn.sign(sender_pk)
# example: TRANSACTION_PAYMENT_SIGN

# example: TRANSACTION_PAYMENT_SUBMIT
# submit the transaction and get back a transaction id
txid = algod_client.send_transaction(signed_txn)
print("Successfully submitted transaction with txID: {}".format(txid))

# wait for confirmation
txn_result = transaction.wait_for_confirmation(algod_client, txid, 4)

print(f"Transaction information: {json.dumps(txn_result, indent=4)}")
print(f"Decoded note: {b64decode(txn_result['txn']['txn']['note'])}")
# example: TRANSACTION_PAYMENT_SUBMIT
