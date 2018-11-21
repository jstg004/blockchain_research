# Finite Fields

- 1st step to understand Elliptic Curve Cryptography.

## Finite Field Definition

- A finite field is a finite set of numbers and 2 operations
  - The 2 operations are addition and multiplication
  - A finite field satisfies:
    - The property closed
      - If _a_ and _b_ are in a set
        - Then _a + b_ and _a * b_ are also in the set
      - Closed under addition and multiplication
      - Need to define addition and multiplication to make sure the results
        stay in the set
      - Example:
        - Set containing _{0, 1, 2}_ is not closed under addition
          - _1 + 2 = 3_ and _3_ is not in the set
        - Set containing _{-1, 0, 1}_ is closed under normal multiplication
          - Any 2 numbers can be multiplied for a result in the set
    - The additive identity _0_ exists
      - _a + 0 = a_
    - The multiplicative identity _1_ exists
      - _a * 1 = a_
    - If _a_ is in the set
      - Then _-a_ is also in the set
      - The additive inverse:
        - _-a_ is defined as rhe value that makes _a +(-a) = 0_
    - If _a_ is in the set and is not _0_
      - Then _a<sup>-1</sup>_ is also in the set
      - The miltiplicative invers:
        - _a<sup>-1</sup>_ is defined as the value that makes
          _a * a<sup>-1</sup> = 1_
- An order of the set:
  - _p_ is designated to the size of the set

## Defining Finite Sets

- Example:
  - If the order/size of a set is _p_
    - Then the elements of the set are _0, 1, 2, ... p-1_
      - The numbers are the elements of the set.

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

- Finite Field of 19:
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

        # Subtraction in a Finite Field:
        num = (self.num - other.num) % self.prime

        # Return an instance of the class:
        return self.__class__(num, self.prime)
```

### Finite Field Multiplication and Exponentiation

- By multiplying the same number many times - can define exponentiation/power.
- Define multiplication on a Finite Field:
  - _F<sub>19</sub>_:
    - _5 *<sub>f</sub> 3 = 5 +<sub>f</sub> 5 +<sub>f</sub> 5 = 15 % 19 = 15_
    - _8 *<sub>f</sub> 17 = 8 +<sub>f</sub> 8 +<sub>f</sub> 8 +<sub>f</sub>..._
      _(17 total 8's)... +<sub>f</sub> 8 = (8 * 17) % 19 = 136 % 19 = 3_
- Exponentiation is multiplying a number many times:
  - _7<sup>3</sup> = 7 * 7 * 7 = 343_
  - Exponentiation in finite field using modulo arithmetic:
    - In _F<sub>19</sub>_:
      - _7<sup>3</sup> = 343 % 19 = 1_
      - _9<sup>12</sup> = 7_

#### Coding Multiplication in Python

- In FieldElement class:

```Python
    def __mul__(self, other):
        # Elements must be from the same Finite Field:
        if self.prime != other.prime:
            raise TypeError('Cannot multiply 2 numbers in different Fields')

        # Multiplication in a Finite Field:
        num = (self.num * other.num) % self.prime

        # Return an instance of the class:
        return self.__class__(num, self.prime)
```

#### Coding Exponentiation in Python

- Exponent is not a field element.
- The exponent is an integer, not another instance of ```FieldElement```
  - Receive the variable ```exponent``` as an integer.

```Python
    def __pow__(self, exponent):
        num = (self.num ** exponent) % self.prime

        return self.__class__(num, self.prime)
```

### Finite Field Division

- In _F<sub>19</sub>_:
  - _3 * 7 = 21 % 19 = 2_ implies that _2 / 7 = 3_
- Finite fields are closed under division.
  - Dividing any 2 numbers where the denominator is not 0 will result in
    another field element
- Fermat's Little Theorem:
  - _n<sup>(p - 1)</sup>_ is always _1_ for every _p_ and every _n > 0_
  - This only works when _p_ is prime
  - Theorem breakdown:
    - _n<sup>(p - 1)</sup> % p = 1_ where p is prime
      - This is always true when operating in prime fields
    - _{1, 2, 3, …​ p - 2, p - 1} =_
      _{n % p, 2n % p, 3n % p, …​ (p - 2)n % p, (p - 1)n % p}_
    - Multiplying every element results in the following:
      - _1 * 2 * 3 * …​ * (p - 2) * (p - 1) % p =_
        _n * 2n * 3n * …​ * (p - 2)n* (p - 1)n % p_
      - The left side is the same as _(p - 1)! % p_
        - _!_ is the factorial
        - Example: _5! = 5 * 4 * 3 * 2 * 1_
      - All the _n_ on right side can be gathered up:
        - _(p - 1)! * n<sup>(p - 1)</sup> % p_
      - Results in: _(p - 1)! % p = (p - 1)! * n<sup>(p - 1)</sup> % p_
        - The _(p - 1)! on both sides can be canceled out, resulting in:
          - _1 = n<sup>(p - 1)</sup> % p_
  - Division is multiplication with the inverse.
    - _a / b = a * (1 / b) = a * b<sup>-1</sup>_
    - If _b<sup>-1</sup>_ can be figured out, then the division problem can be
      reduced to a multiplication problem.
      - _b<sup>(p - 1)</sup> = 1_
      - Therefore _b_ is prime:
        - _b<sup>-1</sup> = b<sup>-1</sup> * 1 =_
          _b<sup>-1</sup> * b<sup>(p - 1)</sup> = b<sup>(p - 2)</sup>
        - Which equates to: _b<sup>-1</sup> = b<sup>(p - 2)</sup>_
      - The inverse can be calculated using the exponent function.
      - In _F<sub>19</sub>_:
        - _7 / 5 = 7 * 5<sup>(19 - 2)</sup> = 7 * 5<sup>17</sup> =_
          _5340576171875 % 19 = 9_
        - This is an expensive calculation.
          - Exponentiating grows very fast as primes grow bigger.
          - To make the calculations less expensive, utilize the ```pow```
            function in Python.
            - The ```pow``` function exponentiates.
            - ```pow(7, 17)``` equates to _7 ** 17_
              - The operator for raising a number to the power of another
                number is _**_.
            - The python ```pow``` function has an optional 3rd argument which
              makes the calculation more efficient.
            - ```pow``` with modulo by the 3rd argument:
              - ```pow(7, 7, 19)``` equates to _7 ** 17 % 19_
                - the ```pow``` will be faster because the modulo function is
                  done after each round of multiplication.

### Redefining Exponentiation

- ```__pow__``` method
  - Example: _a<sup>-3</sup>_ needs to be a finite field.

    ```Python
    a = FieldElement(7, 13)
    b = FieldElement(8, 13)
    print(a ** -3 == b)
        #prints(True)
    ```

- Because of Fermat's Little Theorem _a<sup>p - 1</sup> = 1_
  - This can be multiplied by _a<sup>p - 1</sup>_ as many times as needed.
  - To do negative exponents:

    ```Python
    def __pow__(self, exponent):
        n = exponent

        # Adds until 'n' is a positive exponent:
        while n < 0:
            n += self.prime - 1

        # Uses Python's built in function:
        num = pow(self.num, n, self.prime)

        return self.__class__(num, self.prime)
    ```

- The above code can be simplified to:

    ```Python
    def __pow__(self, exponent):
        # Turns 'exponent' into a number within 0 to (p - 1) range.
        # Use modulo to force a negative number to a positive:
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)

        return self.__class__(num, self.prime)
    ```