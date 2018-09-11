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

## finances and business

### CST

* provides the opportunity to perform in-system transactions
* designed to allow greater system flexibility in real time
  * provides grounds for future growth and development of the system
* all CST tokens are issues during the ICO
* may be divided up to 0.00000001 CST

### CST token use cases

* CST may be purchased, exchanged, sold, leased, or rented out
* token holder may register in the system as a provider
* providers can become a participant in the system by putting storage volumes
  into the Casper API network
  * 25.6GB of storage volume for each CST token
  * rewarded in CST
  * providers need to meet technical requirements
    * server uptime and connection speed
* any CST token holder is eligible to fully dispose the tokens
* any Casper API use may lease their tokens or rent out to any Casper API user
  * if leased, the lessee acquires te right to use the token
    * just like any other user/provider
    * lease in ensured by the smart contract
    * lease price is based on market conditions
* decentralized applications (DAapps)
  * act as users of the service
  * have separate fixed USD rates for data storage and transmission (GB/month)
* the Casper API will provide payment processing and user access to network
* the Casper API will withhold a certain part of incoming payments to ensure
  the network and the software run normally
  * the rest is converted to CST according to current exchange rate and sent to
    the smart contract
    * these tokens serve as a reward for the providers
    * distributed among providers according to pricing and individual
      contribution to the system
* the system allows for providers to be rewarded in fiat currency
  * have ability to put tokens back into circulation again
* growing number of investors encourages token purchasing performed by Casper API
  * contributes to token exchange rate increase
* Casper API reservers 8% of the tokens and part of the funds raised during ICO
  * this reserve ensures stability of the inner financial system
  * helps the company provide a fully functioning service at the early stages
    * if providers are not active enough
  * allows for more stable CST/USD exchange rate

### ICO - main terms and conditions

* IDO is condicted on the Ethereum platform through a smart contract
* CST token emission or mining is impossible after the ned of the ICO
* if the system fails to reach the soft cap during the ICO
  * raised funds will be returned to investors
  * funds raised during Pre-ICO are non-refundable

### providers compensation formula

* if all the technical requirements for equipment and uptime are met:

  ``` none
  ([monthly rate for 1GB of storage] * [actual storage volume utilized] + 
   [rate for 1GB transferred] * [actual data transmitted]) * 0.85/4
  ```

### CST value projection and CST holder privileges

* long-term CST growth driver will be the volume of data within the system
  * number of TB the users will purchase through the Casper API

* the Fisher equation:
  * MV = PQ where:
    * M = money supply
    * V = velocity of circulation
    * P = price level in the economy
    * Q = the output produced by the economy
  * applying this equation to the Casper API economics assumes that PQ is the
    volume of money transfers in the system that rely on CST
  * money supply in this model:

    ``` none
    amount of CST in circulation * market exchange rate of CST/USD
    ```

* basic equation for CST/USD exchange rate projection:

  ``` none
  CST exchange rate =
      USD transaction volume per year / CST in circulation /
      CST velocity of circulation
  ```

* making a projection for each of 3 above figures:
  1. USD transaction volume per year:
     * provider storage and transfer serices are paid for in CST
     * transaction volume is the target market volume for Casper API included in
       in the financial model multiplied by the rates set in the system for
       services
     * Casper API allows users to pay for services in both CST or fiat money
     * if user pays in fiat money - Casper API transfers CST for the provider
       from the reserve fund or purchases CST on exchanges (if needed)
       * if services are paid for with fiat currency - Casper API deducts a fee
       * CST is purchased for the amount of money left over after the fee is
         deducted
  2. amount of CST in circulation
     * not the total supply of CST on te market
     * represents the CST in transactions within the system
       * the CST that users buy to pay providers for the services
       * the CST that providers sell to receive their revenue in fiat money
     * relative categories for CST holders
       * investors:
         * purchased CST during the ICO (Pre-ICO or after on exchanges)
         * hold tokens for long periods of time (1 - 5 years)
         * this volume of CST is virtually out of the market
       * providers:
         * reserve CST in the system to provide their resources
         * receive CST from users as rewards for their services provided
         * may dispose of CST received for the following purposes:
           * reserve further - increasing resources on offer in the system
           * sell and take the revenue in fiat currencies - transactor
           * keep the tokens to sell later at a higher price - trader
           * keep the tokens and rent them out to other providers
         * transactors within the system
           * transactors are CST buys and sells linked to the system function
             * users buying CST to pay for services
             * providers selling the CST they earned
         * Reserve Fund of the system
           * serves as market maker
           * this fund keeps a stable number of CST
           * CST are sold during price hikes to be bought back later and restore
             the previous amount of CST ni this fund
         * traders
           * those who buy CST for speculative reasons
           * seek profit from price difference
     * to determine the volume of CST in circulation:
       * deduct the amount of tokens held by investors from the total amount on
         the market
       * deduct the CST stored in the Reserve Fund of the system
         * in short-term - a fraction of this CST can be used for market-making
         * in long-term - amount of CST in the Fund must be stable
     * after deducting CST held by investors and the fund - a share of CST is
       distributed among providers and traders with remainder of CST circulating
       in transactions
     * the amount of CST reserved by providers is determined by:
       * storage volume in the system
       * CST capacity - total capacity provider can put up after reserving 1 CST
     * financial model includes a potential provider (data center) profit for
       1TB of storage
       * based on current CST capacity and CST exchange rate projections - the
         payback period for providers per 1 CST is estimated
       * the Casper API determines the CST capacity based on the resulting
         payback period so that CST payback period stays within the target
         boundaries
       * with the resulting CST capacity and the data storage capacity utilized
         in the system - the amount of CST that providers must reserve to
         service a required storage volume is derived
         * this CST is taken out of circulation
       * a share of the remaining CST is bought and sold by traders
  3. CST velocity of circulation
     * turnover ratio of CST characterizes the number of times on CST can be
       used in 1 year
     * as data volumes increase - providers will be keeping their CST and
       reserving them in the system
     * CST value is dependent on the amount of CST reserved by providers
     * CST capacity is determined by Casper API  based on the current CST market
       value
     * the Casper API cannot change CST capacity on the fly
       * CST capacity update is set to 1 month
     * CST capacity change is by design one of market-making instruments along
       with CST sales by the Reserve Fund of the system

### market-making logic

* the Casper API project implies the creation of a Reserve Fund that consists
  of a certain amount of CST and USD
  * this is considered one of the items of expenditure present in the project's
    financial model

#### Fund's objectives

* utilized for market-making and marketing
1. market-making
   * implies certain actions taken by the Casper API that directly or indirectly
     affect the market value of CST
   * Casper API market interventions follow strict logic and will be predicable
     * ensures providers capacities are in use by 70% on average
     * ensures a CST payback period of no longer than 12 months for providers
       by changing CST capacity according to current CST price on exchanges
   * conducting market-making
     1. monthly CST capacity correction is calculated  according to current CST
        price on exchanges and the projected CST payback periord for providers
        * if there is an increase in the CST payback period as result of an
          increase in CST price - the Casper API increases CST capacity
          * reduces the CST payback period (for providers) to its target
            boundaries
     2. Fund interventions in the market
        * CST capacity change cannot occur more often than once a month
          * some imbalances may be observed on the market
          * inflow of new users can drive the value of CST up
            * can make payback period longer for providers who sell CST at a
              higher price
          * during the rise in demand providers may begin leaving the system
            * this increases the load on the remaining providers - destabilizes
              the entire system
          * Casper API uses its own CST to sell on exchanges during times of
            price hikes until CST capacity can be changed
        * if CST price drops within a month - Casper API will buy CST on
          exchanges using Fund's fiat money
          * once CST capacity changes - providers will either have a surplus or
            a deficit of CST
            * this leads to CST price correction
          * Casper API buys enough CST for cheap in the amount required to
            restore the initial amount of tokens in the Fund
            * sells back during reverse interventions
2. marketing
   * the Fund's resources can be used to conduct marketing activities
   * the Fund's CST can be allocated towards select DApps in the for of grants
     * projects can later begin using the Casper API platform and strengthen
       the company's (DApps?) position on the market

#### Fund resources

* amount of the Fund's resources allocated towards marketing also depend on the
  sum raised during ICO and the number of CST sold
* amount of fiat at the Fund's disposal depends on the sum raised during the ICO
* amount of CST in the Reserve Fund depends on the amount of CST sold during ICO