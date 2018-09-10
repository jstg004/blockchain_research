# Casper API notes

* an infrastructure to store data on any blockchain platform (that is capable of
  implementing smart contracts)
* allows for the capabilities of cloud storage in a decentralized data storage
  compatible with any blockchain platform

## overview

### smart contracts

* smart contracts are used to make interaction between clients/providers easier
* smart contracts regulate storage network and supervise work or providers

### P2P architecture

* all network participants connect to each other - relying on large nodes\
  * allows for some DDoS protection
* no geographic limits
  * users are able to receive their data from the nearest provider
* several copies of the data are stored be different providers

### Lightning Network private channel

* operations with data can be made through a private cryptographic channel
  between client and provider

### SDK

* integrating the Casper API into any application
* developers can access their data within the Casper API infrastructure

## Casper API services

### data storage

* decentralized data storage that allows for
  * uploading and downloading
  * editing and deleting
  * access permission management
  * file random read function
  * unencrypted data modification without replacing the data
  * ability to mount virtual storage as an external drive

### backup copy storage

* cheaper storage in data is rarely accessed
* ability to store files in partner data centers

### CDN

* ability for fast load times for websites
* increased stability under high loads
* choice between provider networks in target regions

## CST token emission

* Casper token (CST) currency unit
* used in every transaction without the Casper APU on any blockchain

### franchise-like storage volume registration system

* when a CST holder decides to become a provider they purchase a storage valume
  quota
  * this is registered in a smart contract
  * rate of 25.6GB for 1 CST
    * designed in order to ensure the payback period of N months
      * attracts providers ready for long-term cooperation
* purchasing a quota:
  * potential provider invokes the register (```tokenCount```) function of the
    smart contract
    * entering the desired amount of tokens as the argument
    * the indicated amount of tokens is locked and not allowed to be used
  * token holder is eligible to modify the amount of locked tokens at any time
    * to do this - invoke the register (```tokenCount```) function
      * enter the new number of tokens (even 0)
* request for data storage
  * invoke the getPeers (```sizeToStore```) function of the smart contract
    * providers are selected depending on available storage volume within
      respective quotas

### independent  medium of exchange

* independent from any given crytocurrency on the blockchain integrated
* user pays for data storage services
* CDN services/providers are rewarded for supplying the data services
* Casper API operations are based on a blockchain with its own monetary unit
  * launched on several blockchain platforms using smart contracts
    * provider will receive storage requests from users of several blockchain
      platforms at the same time
* to provide transparency rewards are credited to the provider's account in CST
  * issued on the Ethereum platform
  * can be shifted to other platforms keeping the same total amount of tokens

### token price support

* price of CST is backed by the profitability of services rendered by the
  provider for the storage volume registered for 1 CST as well as by CST
  token turnover
* during the ICO a limited amount of tokens are issued
  * quota of 25.6GB oer 1 CST
  * Casper API can register a limited storage volume with all the tokens
* when the network registers storage volume exceeding a certain limit of the max
  volume
  * while a certain min limit of the registered storage volume is already in use
  * the quota for 1 CST will begin to increase
* quota is raised to keep a certain share of the total storage volume always
  available to be filled with user data
* as the usage of the Casper API grows, CST tokens will be backed by increasing
  amounts of real assets

### selling tokens on exchanges and token leasing

* the Casper API smart contract is based on teh ERC20 standard
  * ability to put CST tokens on ab exchange
  * freely buy/sell - trade/lease
* free circulation of CST tokens on exchanges can lead to increases in the price
  of the token
  * leads to the possibility of obstacles in purchasing CST tokens
  * leasing tokens could become financially attractive if market prices are high
  * token holders can rent the tokens
  * profitable and transparent for token holder and lessee

### token emission

* token purchase during Pre-ICO:
  * CST tokens for Pre-ICO with non-ERC20 contract were issued 12/19/2017
  * once the ICO goes live these tokens can be swapped for CST tokens of the
    operational smart contract that complies with the ERC20 standard
* tokens purchased during ICO:
  * CST tokens were issued during the ICO using a separate ERC20-compliant smart
    contract
    * able to swap tokens purchased during Pre-ICO for the ICO tokens via the
      ```exchange()``` function of the smart contract
* after ICO is terminated:
  * purchased tokens can be swapped for CST tokens of the operational smart
    contract

### token release schedule

* all tokens purchased during the Pre-ICO, pre-sale, and crowd-sale are locked
  temporarily
  * they release in this order:
    1. September 2018 - 20%
    2. November 2018 - 20% - Casper API alpha-version release
    3. January 2019 - 20%
    4. March 2019 - 20% - Casper API beta-version release
    5. May 1019 - project launch
* the Casper API smart contract will have an ```exchange()``` function
  * this function allows you to swap Pre-ICO and ICO tokens for the operational
    smart contract tokens

## pricing policy

* users pay monthly for GB storage as well as downloads per GB
* providers are rewarded for storing a certain certain number of GB per month
  * also rewarded for providing data for downloads in GB
  * payment is performed in CST according rate determined in the smart contract
    and the account provider's scoring
* user pays for data storage services in CST
  * according to current USD/CST rate
  * amount of CST tokens vary depending on exchange rate
* the smart contract selects storage providers automatically
  * when a file is successfully placed into storage, the smart contract starts
    charging user for storage on a monthly basis
    * charges are deducted from the user's prepayment
      * user submits prepayment via the client application in BTC, ETH, or USD
        * it is then converted to CST
    * if user deletes the file from the service, remaining prepayment is
      returned to the user

### providers economics

* provider uses equipment for which cost structure can be calculated
  * amortization costs
  * energy costs
  * internet and rent expenses
* providers offer disk space to store data
  * an incoming and outgoing internet connection
  * not rewarded for incoming connections, user uploads for free
  * user pays for monthly file storage and each download

