# notes from: _Blind Signatures for Untraceable Payments_

* by David Chaum ~ 1998

## basic idea

### the paper analog explanation/concept of a blind signature

* a blind signature can be implemented with carbon paper lined envelopes
* a signature is written on the outside of this type of envelope
  * this causes a carbon copy of that signature to be imprinted on a slip of
    paper inside that envelope

#### to hold an election by secret ballot in different locations at the same time

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
   addressed to the elector listed as the return address on the original envelope
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