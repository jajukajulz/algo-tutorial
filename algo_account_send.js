// Script 3 - send algos from one account to another using the algosdk
// Usage - $node algo_account_send.js

const algosdk = require('algosdk');
// In order to do an ASA tutorial, we will need to generate 3 accounts
// once created, copy off the values which we will paste into the tutorial code
// once created successfully, you will need to add funds to all three
// The Algorand TestNet Dispenser is located here: https://bank.testnet.algorand.network/

//------Update account mnemonics------\\

var account1_mnemonic = 'PLEASE REPLACE ME';
var account2_mnemonic = 'PLEASE REPLACE ME';
var account3_mnemonic = 'PLEASE REPLACE ME';
console.log("Account Mnemonic 1 from user = " + account1_mnemonic);
console.log("Account Mnemonic 2 from user = " + account2_mnemonic);
console.log("Account Mnemonic 3 from user = " + account3_mnemonic);

//------/Update account mnemonics------\\

//------Recover algorand accounts from mnemonic/secret phrase------\\

console.log("Now attempting to recover accounts using user supplied secret phrases...");

var recoveredAccount1 = algosdk.mnemonicToSecretKey(account1_mnemonic);
var isValid = algosdk.isValidAddress(recoveredAccount1.addr);
console.log("Account recovered: " + isValid);
var account1 = recoveredAccount1.addr;
console.log("Account 1 = " + account1);

var recoveredAccount2 = algosdk.mnemonicToSecretKey(account2_mnemonic);
var isValid = algosdk.isValidAddress(recoveredAccount2.addr);
console.log("Account recovered: " + isValid);
var account2 = recoveredAccount2.addr;
console.log("Account 2 = " + account2);

var recoveredAccount3 = algosdk.mnemonicToSecretKey(account3_mnemonic);
var isValid = algosdk.isValidAddress(recoveredAccount3.addr);
console.log("Account recovered: " + isValid);
var account3 = recoveredAccount3.addr;
console.log("Account 3 = " + account3);

console.log("");

//------/Recover algorand accounts from mnemonic/secret phrase------\\

//------Setup algod connection------\\

console.log("Now setting up algod connection...");

// configure  algod client connection parameters i.e. connection to algo network (this can either be to sandbox or via a 3rd party service)

// this token is not the same as a digital asset, rather it is API Key (token): which is defined as an object. The token is used to
// identify the source of a connection / give you permission to access an algorand node. In the sandbox, the default token is aaa...
// Example use of token is when querying KMD for list of wallets, the first will work but the second has invalid key and fails
// $curl localhost:4002/v1/wallets -H "X-KMD-API-Token: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
// $curl localhost:4002/v1/wallets -H "X-KMD-API-Token: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaB"
// This is especially useful if you are connecting to the Algorand TestNet/BetaNet/MainNet via a 3rd party service i.e. a 3rd party node
// e.g. https://developer.purestake.io/ (in the Ethereum space, this would be infura.io)
const token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const server = "http://localhost"; //for TestNet use PureStake "https://testnet-algorand.api.purestake.io/ps2" or AlgoExplorer "https://api.testnet.algoexplorer.io",
const port = 4001;

// Instantiate the algod wrapper
let algodclient = new algosdk.Algodv2(token, server, port);

//------/Setup aldod connection------\\

//------Check algod status------\\

console.log("Now checking algod status...");

(async () => {
    // call the status method from the algod client to check the details of your connection.
    let status = (await algodclient.status().do());
    console.log("Algorand network status: %o", status);
})().catch(e => {
    console.log(e);
});

//------/Check algod status------\\

//------Send algos from one account to another and check balance------\\

console.log("Now sending algos from one account 1 to account 2... Assumes account 1 has funds!");
//If you use the async keyword before a function definition, you can then use await within the function.
// When you await a promise, the function is paused in a non-blocking way until the promise settles.
(async() => {
    let params = await algodclient.getTransactionParams().do();
    let txn = {
        "from": recoveredAccount1.addr,
        "to": recoveredAccount2.addr,
        "fee": 1,
        "amount": 1000000, // 2 algos
        "firstRound": params.firstRound,
        "lastRound": params.lastRound,
        "genesisID": params.genesisID,
        "genesisHash": params.genesisHash,
        "note": new Uint8Array(0)
    }
    let signedTxn = algosdk.signTransaction(txn, recoveredAccount1.sk);
    let sendTx = await algodclient.sendRawTransaction(signedTxn.blob).do();

    console.log("Transaction: " + sendTx.txId);

    console.log("Now checking balances...");
    // get information on accounts e.g. balances
    let account_info = (await algodclient.accountInformation(recoveredAccount1.addr).do());
    let acct_string = JSON.stringify(account_info);
    console.log("Account 1 Info: " + acct_string);
    console.log("Balance of account 1: " + JSON.stringify(account_info.amount));

    account_info = (await algodclient.accountInformation(recoveredAccount2.addr).do());
    acct_string = JSON.stringify(account_info);
    console.log("Account 2 Info: " + acct_string);
    console.log("Balance of account 2: " + JSON.stringify(account_info.amount));

    account_info = (await algodclient.accountInformation(recoveredAccount3.addr).do());
    acct_string = JSON.stringify(account_info);
    console.log("Account 3 Info: " + acct_string);
    console.log("Balance of account 3: " + JSON.stringify(account_info.amount));

})().catch( e => {
    console.log(e)
})
//------/Send algos from one account to another and check balance------\\
