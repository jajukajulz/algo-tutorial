# Alogrand Tutorials
Repo with examples illustrating the use of the Algorand JavaScript SDK (https://github.com/algorand/js-algorand-sdk).

Examples include:
- connecting to a network
- creating accounts
- sending transactions 
- querying balances

# Assumptions
Familiarity with the Algorand network and tools e.g. sandbox (which creates a default unencrypted wallet with 3 funded accounts)

- `./sandbox up`

- `./sandbox goal account list`

- `./sandbox goal wallet list`


`node.js` and `npm` are installed properly in your development environment

- `node -v`

- `npm -v`

# Steps (if not cloning repo)
Prepare a new directory and initialise a Node environment.

`npm init`

Install Algorand JavaScript SDK (this updates package.json)

`npm install algosdk -s`

Create a new file

`touch algo_account_create.js`

Paste contents from https://github.com/jajukajulz/algo-tutorial/blob/master/algo_account_create.js

# Steps (if cloning repo)

Clone repo
`git clone https://github.com/jajukajulz/algo-tutorial.git`

Run script to create 3 new accounts via (i.e. via SDK). Once complete, make a note of the 3 account mnemonics and save somewhere safe.

`node algo_account_create.js`

Fund the 1st of the 3 newly created account using one of the default funded sandbox accounts

`./sandbox goal clerk send -a 12345678 -f <REPLACE_SOURCE_ADDRESS_FROM_SANDBOX> -t <REPLACE_DESTINATION_ADDRESS_CREATED_BY_SDK>`

Run script to check balance of the 3 new accounts (i.e. via SDK). Before running, 1st update the 3 account mnemonics manually.

`node algo_account_balance.js`

Run script to send funds from the 1st of the 3 new accounts to the 2nd account. Before running, 1st update the 3 account mnemonics manually.

`node algo_account_send.js`


## Reference articles
- https://github.com/algorand/js-algorand-sdk/tree/develop/examples
- https://developer.algorand.org/tutorials/create-account-testnet-javascript/
- https://developer.algorand.org/tutorials/asa-javascript/
- https://developer.algorand.org/articles/getting-started-assets/
- https://developer.algorand.org/docs/features/asa/
- https://kctheservant.medium.com/demonstration-of-algorand-with-javascript-sdk-34ba5bfb7eb4
- https://blockdaemon.com/docs/protocol-documentation/algorand/creating-an-algorand-wallet/