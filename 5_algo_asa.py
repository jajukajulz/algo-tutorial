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

# grab suggested params from algod using client includes things like suggested fee and first/last valid rounds
suggested_params = algod_client.suggested_params()

# example: CREATE ASSET
# Account 1 creates an asset called Ariary Digital (i.e. Madagascar) and sets Account 2 as the manager, reserve, freeze, and clawback address.

# manager - The manager account is the only account that can authorize transactions to re-configure or destroy an asset.

# reserve - non-minted assets will reside in this account instead of the default creator account. Assets transferred from this account are "minted" units of the asset.

# freeze - The freeze account is allowed to freeze or unfreeze the asset holdings for a specific account. When an account is frozen it cannot send or receive the frozen asset. In traditional finance, freezing assets may be performed to restrict liquidation of company stock, to investigate suspected criminal activity or to deny-list certain accounts. If the DefaultFrozen state is set to True, you can use the unfreeze action to authorize certain accounts to trade the asset (such as after passing KYC/AML checks).

# clawback - i.e. revoking an asset for an account removes a specific number of the asset from the revoke target account. The clawback address represents an account that is allowed to transfer assets from and to any asset holder (assuming they have opted-in). Use this if you need the option to revoke assets from an account (like if they breach certain contractual obligations tied to holding the asset). In traditional finance, this sort of transaction is referred to as a clawback.

# Asset Creation transaction
unsigned_txn = transaction.AssetConfigTxn(
    sender=account_1_address,
    sp=suggested_params,
    total=1000,
    default_frozen=False,
    unit_name="ArD",
    asset_name="Ariary Digital",
    manager=account_2_address,
    reserve=account_2_address,  # non-minted assets will reside in this account instead of the default creator account. Assets transferred from this account are "minted" units of the asset.
    freeze=account_2_address,  # account authorised to sign a transaction to freeze an asset
    clawback=account_2_address,  # account authorised to sign a clawback transaction
    url="https://path/to/my/asset/details",
    decimals=0,
)
# example: ASSET_CREATE

# example: ASSET_CREATE_SIGN
# sign the transaction with private key of creator
signed_txn = unsigned_txn.sign(account_1_private_key)
# example: ASSET_CREATE_SIGN

# example: ASSET_CREATE_SUBMIT
# submit the transaction to the network and get back a transaction id
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
# example: ASSET_CREATE_SUBMIT

# example: RETRIEVE_ASSET_INFORMATION
# Retrieve the asset info of the newly created asset
asset_info = algod_client.asset_info(asset_id)
asset_params: Dict[str, Any] = asset_info["params"]
print(f"Asset Name: {asset_params['name']}")
print(f"Asset params: {list(asset_params.keys())}")
# example: RETRIEVE_ASSET_INFORMATION

# example: OPT-IN_TO_ASSET
user_input = input("Now Opt-in to the newly created asset and press enter. ")
# Create opt-in transaction
# asset transfer from me to me for asset id we want to opt-in to with amt==0
suggested_params = algod_client.suggested_params()
optin_txn = transaction.AssetOptInTxn(
    sender=account_3_address, sp=suggested_params, index=asset_id
)
signed_optin_txn = optin_txn.sign(account_3_private_key)
txid = algod_client.send_transaction(signed_optin_txn)
print(f"Sent opt in transaction with txid: {txid}")

# Wait for the transaction to be confirmed
results = transaction.wait_for_confirmation(algod_client, txid, 4)
print(f"Result confirmed in round: {results['confirmed-round']}")
# example: OPT-IN_TO_ASSET

# example: TRANSFER_ASSET
suggested_params = algod_client.suggested_params()
# Create transfer transaction
xfer_txn = transaction.AssetTransferTxn(
    sender=account_2_address,  # this should be from the reserve account
    sp=suggested_params,
    receiver=account_3_address,
    amt=1,
    index=asset_id,
)
signed_xfer_txn = xfer_txn.sign(account_2_private_key)
txid = algod_client.send_transaction(signed_xfer_txn)
print(f"Sent transfer transaction with txid: {txid}")

results = transaction.wait_for_confirmation(algod_client, txid, 4)
print(f"Result confirmed in round: {results['confirmed-round']}")
# example: TRANSFER_ASSET

# example: FREEZE_ASSET
# example: FREEZE_ASSET

# example: CLAWBACK_ASSET
# example: CLAWBACK_ASSET

# example: OPT_OUT_ASSET
# example: OPT_OUT_ASSET

# example: DESTROY_ASSET
# example: DESTROY_ASSET

# example: MODIFY_ASSET
# example: MODIFY_ASSET
