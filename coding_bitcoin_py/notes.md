# Finite Fields

- essential to learning Elliptic Curve Cryptography

## Finite Field Defi nition

- a finite field is a finite set of numbers and 2 operations
  - the 2 operations are addition and multiplication
  - a finite field satisfies:
    - the property closed
      - if _a_ and _b_ are in a set
        - then _a + b_ and _a * b_ are also in the set
      - closed under addition and multiplication
      - need to define addition and multiplication to make sure the results
        stay in the set
      - Example:
        - set containing _{0, 1, 2}_ is not closed under addition
          - _1 + 2 = 3_ and _3_ is not in the set
        - set containing _{-1, 0, 1}_ is closed under normal multiplication
          - any 2 numbers can be multiplied for a result in the set
    - the additive identity _0_ exists
      - _a + 0 = a_
    - the multiplicative identity _1_ exists
      - _a * 1 = a_
    - if _a_ is in the set
      - then _-a_ is also in the set
      - the additive inverse:
        - _-a_ is defined as rhe value that makes _a +(-a) = 0_
    - if _a_ is in the set and is not _0_
      - then _a<sup>-1</sup>_ is also in the set
      - the miltiplicative invers:
        - _a<sup>-1</sup>_ is defined as the value that makes
          _a * a<sup>-1</sup> = 1_
- an order of the set
  - _p_ is designated to the size of the set

## Defining Finite Sets

