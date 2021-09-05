// Script 1 - create algorand accounts using the algosdk
// Usage - $node algo_account_create.js

const algosdk = require('algosdk');
// In order to do an ASA tutorial, we will need to generate 3 accounts
// once created, copy off the values which we will paste into the tutorial code
// once created successfully, you will need to add funds to all three
// The Algorand TestNet Dispenser is located here: https://bank.testnet.algorand.network/

//------Setup algorand accounts------\\

console.log("Now creating accounts...");

var acct = null;

acct = algosdk.generateAccount();
// const { sk: account1SecretKey, addr: account1Address } = algosdk.generateAccount();
var account1 = acct.addr;
console.log("Account 1 = " + account1);
// convert the Account 1 secret key to a 25-word mnemonic i.e. human-readable secret phrase
var account1_mnemonic = algosdk.secretKeyToMnemonic(acct.sk);
console.log("Account Mnemonic 1 = "+ account1_mnemonic);
console.log("Account created. Note the address and mnemonic (store mnemonic somewhere safe!)");

acct = algosdk.generateAccount();
var account2 = acct.addr;
console.log("Account 2 = " + account2);
var account2_mnemonic = algosdk.secretKeyToMnemonic(acct.sk);
console.log("Account Mnemonic 2 = " +account2_mnemonic);
console.log("Account created. Note the address and mnemonic (store mnemonic somewhere safe!)");

acct = algosdk.generateAccount();
var account3 = acct.addr;
console.log("Account 3 = " + account3);
var account3_mnemonic = algosdk.secretKeyToMnemonic(acct.sk);
console.log("Account Mnemonic 3 = " +account3_mnemonic);
var recoveredAccount3 = algosdk.mnemonicToSecretKey(account3_mnemonic);
var isValid = algosdk.isValidAddress(recoveredAccount3.addr);
console.log("Is this a valid address: " + isValid);
console.log("Account created. Note the address and mnemonic (store mnemonic somewhere safe!)");
console.log("");
console.log("Add funds to all of these accounts using the TestNet Dispenser at https://bank.testnet.algorand.network/ (if accounts are created on testnet)");
console.log("Alternatively, add funds to all of these accounts using goal (i.e. ./sandbox goal clerk send -a 12345678)  using one of the default accounts created from the unencrypted wallet");
console.log("");
console.log("Copy these 3 lines of code. They will be used in the tutorials that follow (algo_account_balance.js and algo_account_send.js");
console.log("");
console.log("var account1_mnemonic = \"" + account1_mnemonic + "\"");
console.log("var account2_mnemonic = \"" + account2_mnemonic + "\"");
console.log("var account3_mnemonic = \"" + account3_mnemonic + "\"");

//------/Setup algorand accounts------\\

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

//------Query account objects on the network------\\

console.log("Now checking balances...");

// get information on accounts e.g. balances
(async () => {
    let account_info = (await algodclient.accountInformation(account1).do());
    let acct_string = JSON.stringify(account_info);
    console.log("Account 1 Info: " + acct_string);
    console.log("Balance of account 1: " + JSON.stringify(account_info.amount));

    account_info = (await algodclient.accountInformation(account2).do());
    acct_string = JSON.stringify(account_info);
    console.log("Account 2 Info: " + acct_string);
    console.log("Balance of account 2: " + JSON.stringify(account_info.amount));

    account_info = (await algodclient.accountInformation(account3).do());
    acct_string = JSON.stringify(account_info);
    console.log("Account 3 Info: " + acct_string);
    console.log("Balance of account 3: " + JSON.stringify(account_info.amount));

})().catch(e => {
    console.log(e);
});

//------/Query account objects on the network------\\
