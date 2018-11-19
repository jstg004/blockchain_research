# Finite Fields

- essential to learning Elliptic Curve Cryptography

## Finite Field Definition

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

- Example:
  - if the order/size of a set is _p_
    - then the elements of the set are _0, 1, 2, ... p-1_
      - the numbers are the elements of the set

### Constructing a Finite Set in Python

```Python
# Constructing a Finite Set

class FieldElement:

    def __init__(self, num, prime):
        # check if num is between '0 and prime - 1' inclusive
        if num >= prime or num < 0:
            error = f"Num {num} not in field range 0 to {prime - 1}"
            #error = 'Num {} not in field range 0 to {}'.format(num, prime-1)

            # if num is NOT between '0 and prime - 1'
            # then it is an inappropriate value - so ERROR
            raise ValueError(error)

        # assign the initialization values
        self.num = num
        self.prime = prime


    def __repr__(self):
        return f"FieldElement_{self.prime}({self.num})"
        #return 'FieldElement_{}({})'.format(self.prime, self.num)


    # check if objects in the class 'FieldElement' are = or not
    # only True when 'num' and 'prime' are =
    def __eq__(self, other):
        # python allows '==' operator to be replaced with the '__eq__' method
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    '''
    Write the corresponding method __ne__ which checks if two FieldElement
    objects are not equal to each other.
    '''
    def __ne__(self, other):
        if other is None:
            return False
        return self.num != other.num and self.prime != other.prime
```

### Modulo Arithmetic

- Used to make a field closed under addition, subtraction, multiplication,
  and division.
- The _%_ symbol is used for modulo arithmetic:
  - _7 % 3_ will equal _1_
    - 7 divided by 3 equals 2 with the remainder of 1, so the modulo is 1.
- Very large numbers can be brought down in size using modulo arithmetic.
  - _341234321423165750432 % 60_ = _32_

### Finite Field Addition and Subtraction

- Need to make sure addition in a Finite Field is closed.
- Example:
  - Finite Field of 19
    - _F<sub>19</sub> = {0, 1, 2, ... 18}_
    - where _a and b_ are elements of _F<sub>19</sub>_
    - +<sub>f</sub> denotes finite field addition
    - Addition being closed:
      - _a +<sub>f</sub> b_ are elements of _F<sub>19</sub>_
    - Modulo arithmetic can be used to guarantee _a +<sub>f</sub> b_:
      - _a +<sub>f</sub> b = (a + b) % 19_
    - _7 +<sub>f</sub> 8 = (7 + 8) % 19 = 15_
    - _11 +<sub>f</sub> 17 = (11 + 17) % 19 = 9_
- Take 2 numbers in the set, add and wrap around the end to get the sum.
- Field addition can be defined as follows:
  - _a +<sub>f</sub> b = (a + b) % p where a and b are elements of F<sub>p</sub>_
- Additive inverse can be defined as follows:
  - _-<sub>f</sub>_ denotes finite field subtraction
  - _a is an element of F<sub>p</sub>_
    - implies that _-<sub>f</sub> a is an element of F<sub>p</sub>_
  - _-<sub>f</sub> a = (-a) % p_
  - In _F<sub>19</sub>_:
    - _-<sub>f</sub> 9 = (-9) % 19 = 10_
      - means _9 +<sub>f</sub> 10 = 0_
- Field subtraction:
  - _a -<sub>f</sub> b = (a - b) % p where a and b are elements of F<sub>p</sub>_
  - In _F<sub>19</sub>_:
    - _11 -<sub>f</sub> 9 = (11 - 9) % 19 = 2_
    - _6 -<sub>f</sub> 13 = (6 - 13) % 19 = 12_

#### Coding Addition and Subtraction in Python

- In FieldElement class:

```Python
    def __add__(self, other):
        # Elements must be from the same Finite Field:
        if self.prime != other.prime:
            raise TypeError('Cannot add 2 numbers in different Fields')

        # Addition in a Finite Field:
        num = (self.num + other.num) % self.prime

        # Return an instance of the class:
        return self.__class__(num, self.prime)

    def __sub__(self, other):
        # Elements must be from the same Finite Field:
        if self.prime != other.prime:
            raise TypeError('Cannot subtract 2 numbers in different Fields')

        # Addition in a Finite Field:
        num = (self.num - other.num) % self.prime

        # Return an instance of the class:
        return self.__class__(num, self.prime)
```