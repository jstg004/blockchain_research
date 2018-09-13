# notes from: _Blind Signatures for Untraceable Payments_

* by David Chaum ~ 1998

## basic idea

### the paper analog explanation/concept of a blind signature

* a blind signature can be implemented with carbon paper lined envelopes
* a signature is written on the outside of this type of envelope
  * this causes a carbon copy of that signature to be imprinted on a slip of
    paper inside that envelope

#### hold an election by secret ballot in different locations at the same time

* an elector must be able to verify that their vote has been counted
1. each elector places a ballot slip with their vote written on it in a
   carbon lined envelope
   * only authorized electors receive signed ballot slips
2. the carbon lined envelop is placed in an outer envelope addressed to the
   trustee
   * the return address written on the outer envelop is the elector's
   * this nested carbon lined envelope is then mailed to the trustee
3. the trustee receives the envelope with the elector's return address on the
   outer envelope - they remove the inner carbon lined envelope
   * then signs the outside of the carbon lined envelope containing the vote
   * not opened - vote not counted yet - elector vote is just verified
   * the trustee uses a special signature which is only valid for this specific
    election
4. the signed carbon lined envelope is then sent back in a new outer envelope
   addressed to the elector listed as the return address on the original
   envelope
5. elector receives a signed envelope - the elector removes the outer
   envelope
   * then checks the signature on the carbon lined envelope
   * the signed ballot slip form the carbon lined envelope is removed
6. the ballot is then mailed to the trustee on the day of the election in a
   new outer envelope (without a return address)
7. the trustee receives the ballots and can be made public - anyone can count
   them and check the signatures
* the trustee never saw the ballot slips while signing them
  * they cannot know anything about the correspondence between the ballot
    containing envelopes signed and the ballots made public
* trustee cannot determine how anyone voted

## functions

* blind signatures include the features of true 2 key digital signature systems
  combined with commutative style public key systems
* the blind signature cryptostystem is comprised of the following functions:
  1. a signing function _**s'**_ known only to the signer
     * the corresponding publically known invere _**s**_
     * _**s(s'(x)) = x**_
     * _**s**_ gives no clue about _**s'**_
  2. a community function _**c**_ and its inverse _**c'**_
     * both of these are known only to the provider
     * _**c'(s'(c(x))) = s'(x)**_, _**c(x)**_, and _**s'**_ give no clue about
       _**x**_
  3. a redundancy checking predicate _**r**_
     * checks for sufficient redundancy to make searching for valid signatures
       impractical

## Protocol

1. provider chooses _**x**_ at random such that _**r(x)**_ - forms _**c(x)**_
   and supplies _**c(x)**_ to the signer
2. signer signs _**c(x)**_ by applying _**s'**_
   * then returns the signed matter _**s'(c(x))**_ to the provider
3. provider strips signed matter by application of _**c'**_
   * this yields _**c'(s'(c(x))) = s'(x)**_
4. anyone can check that the stripped matter _**s'(x)**_ was formed by its
   signer
   * this is checked by applying the signer's public key _**s**_
     * _**r(s(s'(x)))**_

## properties

* desired security properties:
  1. digital signature - anyone can check that a stripped signature _**s'(x)**_
     was formed using the signer's private key _**s'**_
  2. blind signature - the signer knows nothing about the correspondence
     between the elements of the set of stripped signed matter
     _**s'(x<sub>i</sub>)**_ and the elements of the set of unstripped signed
     matter _**s'(c(x<sub>i</sub>))**_
  3. conservation of signatures - the provider can create at more only 1
     stripped signature for each thing that is signed be that signer
     * even with _**s'(c(x<sub>1</sub>)) ... s'(c(x<sub>n</sub>))**_ and choice
       of _**c**_, _**c'**_, and _**x<sub>i</sub>**_
     * it is impractical to produce _**s'(y)**_ such that _**r(y)**_ and
       _**y != x<sub>i</sub>**_
     * the possibility that the same random number could be generated
       independently is ignored

## untraceable payments system

* the blind signature system can be used to make an untraceable payments system
* the bank will sign anything with its private key
  * anything signed is worth a fixed amount

* bank, payer, and payee
  * a single note is formed by the payer, the bank signs it, it is then stripped
    by the payer and provided to the payee - this is cleared by the bank
  1. payer chooses _**x**_ at random such that _**r(x)**_
     * this forms the note _**c(x)**_
  2. payer forwards the note _**c(x)**_ to the bank
  3. the bank signs the note
     * this forms _**s'(c(x))**_ and debits the payer's account
  4. the bank returns the signed note _**s'(c(x))**_ to the payer
  5. the payer strips the note by forming _**c'(s'(c(x))) = s'(x)**_
  6. the payer checks the note by checking that _**s(s'(x)) = x**_
     * if this equation is false then the payment can be stopped
  7. the payer can make the payment by providing the note _**s'(x) directly to
     the payee
  8. the payee can check the note by forming _**r(s(s'(x)))**_
     * the payment can be stopped if this is false
  9. the payee forwards the note _**s'(x)**_ to the bank
  10. the bank checks the note by forming _**r(s(s'(x)))**_
      * the payment is stopped if this is false
  11. the bank adds this note to a comprehensive list of cleared notes
      * the payment is stopped if this note if already on this list
  12. the bank credits the payees account
  13. the bank informs the payee of the note acceptance
* when the bank receives a note to be cleared from the payee - the bank does
  not know which payer the note was originally issued to

## auditability

* payers receive digital receipts from the payees
  * this receipt could include a copy of the note
  * the account the note was actually deposited to can be verified
  * a receipt which indicates that a note was deposited to an account other
    than the specified payee account would flag as fraud
    * the fraudulent account which the payment ended up in can be traced
    * uncleared notes which are reported can be held in a clearing house list
      * prevents the reported fraudulent notes from being cleared

## elaborations

* this can be extended to different situations to provide:
  * economy of mechanism
  * disaggregation of services
  * decentralization
* the roles of the banks and the clearing houses can be separated
* the keys used to sign the notes can be periodically changed for security