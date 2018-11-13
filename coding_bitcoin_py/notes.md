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

# Test run:
a = FieldElement(7, 13)
print("a = FieldElement(7, 13), a =", a)

b = FieldElement(6, 13)
print("b = FieldElement(6, 13), b =", b)

print("a = b?", a == b)
print("a = a?", a == a)

# Prints out:
'''
a = FieldElement(7, 13), a = FieldElement_13(7)
b = FieldElement(6, 13), b = FieldElement_13(6)
a = b? False
a = a? True
'''

#ToDo:
'''
Write the corresponding method __ne__ which checks if two FieldElement
objects are not equal to each other.
'''
```