# Alogrand Tutorials

Repo with examples illustrating the use of the Algorand JavaScript SDK (https://github.com/algorand/js-algorand-sdk).

Examples include:

- connecting to a network
- creating accounts
- sending transactions
- querying balances

# Assumptions

Familiarity with the Algorand network and tools e.g. sandbox (which creates a default unencrypted wallet with 3 funded accounts)

- `$ ./sandbox up`

- `$ ./sandbox goal account list`

- `$ ./sandbox goal wallet list`

`node.js` and `npm` are installed properly in your development environment

- `$ node -v`

- `$ npm -v`

# Steps (if not cloning repo)

Prepare a new directory and initialise a Node environment.

`$ npm init`

Install Algorand JavaScript SDK (this updates package.json)

`$ npm install algosdk -s`

Create a `.env` file for your environment variables

`$ touch .env`

Populate your `.env` file with the following contents (make a note to update the variables named PLEASE_REPLACE_ME)

```
NODE_ENV=development
PORT=3000
BLOCKCHAINENV=TESTNET
DEV_ALGOD_API_KEY=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
DEV_ALGOD_SERVER=http://localhost
DEV_ALGOD_PORT=4001
DEV_ALGOINDEXER_PORT=8980
TESTNET_ALGOD_API_KEY=PLEASE_REPLACE_ME
TESTNET_ALGOD_SERVER=https://testnet-algorand.api.purestake.io/ps2
TESTNET_ALGOINDEXER_SERVER=https://testnet-algorand.api.purestake.io/idx2
TESTNET_ALGOD_PORT=
ACCOUNT1_ADDRESS=PLEASE_REPLACE_ME
ACCOUNT1_MNEMONIC=PLEASE_REPLACE_ME
ACCOUNT2_ADDRESS=PLEASE_REPLACE_ME
ACCOUNT2_MNEMONIC=PLEASE_REPLACE_ME
ACCOUNT3_ADDRESS=PLEASE_REPLACE_ME
ACCOUNT3_MNEMONIC=PLEASE_REPLACE_ME
```

Create a new file, and then copy and paste contents from https://github.com/jajukajulz/algo-tutorial/blob/master/algo_account_create.js

`$ touch algo_account_create.js`

# Steps (if cloning repo)

Clone repo

`$ git clone https://github.com/jajukajulz/algo-tutorial.git`

Change directory and install node dependencies

`$ cd algo-tutorial && npm install`

Setup`.env` file for your environment variables (as noted in previous section)

Run script to create 3 new accounts via (i.e. via SDK). Once complete, make a note of the 3 account mnemonics and save somewhere safe.

`$ node algo_account_create.js`

Fund the 1st of the 3 newly created account using one of the default funded sandbox accounts

`$ ./sandbox goal clerk send -a 12345678 -f <REPLACE_SOURCE_ADDRESS_FROM_SANDBOX> -t <REPLACE_DESTINATION_ADDRESS_CREATED_BY_SDK>`

Run script to check balance of the 3 new accounts (i.e. via SDK). Before running, 1st update the 3 account mnemonics manually.

`$ node algo_account_balance.js`

Run script to send funds from the 1st of the 3 new accounts to the 2nd account. Before running, 1st update the 3 account mnemonics manually.

`$ node algo_account_send.js`

For example of sdk included client side in a browser (i.e. simple website with no server),
`algo-tutorial/webapp/test.html` in your browser. This assumes that you have algosdk installed via npm because
it includes the `../node_modules/algosdk/dist/browser/algosdk.min.js` in the `test.html` file.

## PureStake

The PureStake API service makes it easy to quickly get up-and-running on the Algorand network. The service builds upon PureStake's existing infrastructure platform to provide developers with easy-to-use access to native Algorand REST APIs. You will need to create an account with PureStake in order to get an API key that allows you to use their service to access the Algorand Network (TestNet or MainNet). See https://www.purestake.com/technology/algorand-api/ and https://purestake.github.io/algosigner-dapp-example/

```
const algodServer = 'https://testnet-algorand.api.purestake.io/ps2'
const indexerServer = 'https://testnet-algorand.api.purestake.io/idx2'
const token = { 'X-API-Key': 'YOUR API KEY HERE' }
const port = '';

algodClient = new algosdk.Algodv2(token, algodServer, port);
indexerClient = new algosdk.Indexer(token, indexerServer, port);

algodClient.healthCheck().do()
.then(d => {
  ...
})
.catch(e => {
  console.error(e);
});
```

## Reference articles

- https://github.com/algorand/js-algorand-sdk/tree/develop/examples
- https://developer.algorand.org/tutorials/create-account-testnet-javascript/
- https://developer.algorand.org/tutorials/asa-javascript/
- https://developer.algorand.org/articles/getting-started-assets/
- https://developer.algorand.org/docs/features/asa/
- https://kctheservant.medium.com/demonstration-of-algorand-with-javascript-sdk-34ba5bfb7eb4
- https://blockdaemon.com/docs/protocol-documentation/algorand/creating-an-algorand-wallet/
