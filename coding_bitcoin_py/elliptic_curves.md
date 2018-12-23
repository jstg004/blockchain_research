# Elliptic Curves

- Elliptical Curve form:
  - _y<sup>2</sup> = x<sup>3</sup> + ax + b_

- Linear Equation:
  - _y = mx + b_

- Quadratic Equation:
  - _y = ax<sup>2</sup> + bx + c_

- Cubic Equation:
  - _y = ax<sup>3</sup> + bx<sup>2</sup> + cx + d_

- The elliptic curve in Bitcoin is called 'secp256k1'
  - Equation:
    - _y<sup>2</sup> = x<sup>3</sup> + 7_
    - Canonical form: _y<sup>2</sup> = x<sup>3</sup> + ax + b_

## Coding Elliptic Curves

- Define a class 'Point' to be an actual point on a specific curve:
  - The curve has the form _y<sup>2</sup> = x<sup>3</Sup> + ax + b_
  - The curve can be defined with just the two numbers _a_ and _b_

```Python
class Point:

    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y

        if self.x is None and self.y is None:
            return
        # Check if the point is on the curve:
        if self.y ** 2 != self.x ** 3 + a * x + b:
            # Throws and error is the point is not on the curve:
            raise ValueError(f'Point ({x}, {y}) is not on the curve')

    def __eq__(self, other):
        # Points are equal if and only if they are on the same curve
        # and have the same coordinates:
        return self.x == other.x and self.y == other.y \
            and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not (self == other)
```

## Point Addition

- Perform an operation on 2 of the points on the elliptic curve to get a 3rd
  point also on the curve.
- Point addition is commutative.
  - Adding point _A_ to point _B_ is the same as adding point _B_ to point _A_.
- Except for in some special cases, a line will intersect at either 1 or 3
  points on an elliptic curve.
- Point addition is defined as:
  - For any 2 points: _P<sub>1</sub> = (x<sub>1</sub>, y<sub>1</sub>)_
    and _P<sub>2</sub> = (x<sub>2</sub>, y<sub>2</sub>)_
    _P<sub>1</sub> + P<sub>2</sub>_ can be found by:
    - Finding the point intersecting the elliptic curve a 3rd time by
      drawing a line through _P<sub>1</sub>_ and _P<sub>2</sub>_
    - Then reflecting the resulting point over the x-axis.

## Math of Point Addition

### Identity

- There exists some point (_I_) which when added to a point (_A_)
  results in _A_.
  - This point is the point at infinity.
    - There is 1 extra point in the elliptic curve which makes the vertical
      line intersect the curve a 3rd time.
  - _I + A = A_
  - This is related to invertibility.
    - For some point _A_, there is some other point _-A_ which results in the
      identity point.
      - _A + (-A) = I_
  - These points are opposite of each other on the elliptic curve.

### Commutativity

- _A + B = B + A_
- The line going through _A_ and _B_ will intersect the curve a 3rd time in
  the same place no matter what order.

### Associativity

- _(A + B) + C = A + (B + C)_

## Coding Point Addition

- Python does not have infinity numbers.
  - Use ```None``` value

- The ```__init__``` method is modified to not check if the curve equation is
  satisfied when the point is at infinity:

```Python
if self.y ** 2 != self.x ** 3 + self.a * self.x + self.b:
    raise ValueError(f'Point ({x}, {y}) is not on the curve')
```

```Python
# Overload '+' operator:
def __add__(self, other):
    if self.a != other.a or self.b != other.b:
        raise TypeError

    '''
    x and y coordinates being None signifies the point at infinity.
    '''

    # If 'self.x' is None, 'self' is the point at infinity (additive identity)
    if self.x is None:
        return other

    # If 'other.x' is None, 'other' is the point at infinity (additive identity)
    if other.x is None:
        return self
```

## Point addition when _x<sub>1</sub> != x<sub>2</sub>_

- 1st find the slope created by the 2 points
  - _P<sub>1</sub> = (x<sub>1</sub>, y<sub>1</sub>)_,
    _P<sub>2</sub> = (x<sub>2</sub>, y<sub>2</sub>)_,
    _P<sub>3</sub> = (x<sub>3</sub>, y<sub>3</sub>)_
  - _P<sub>1</sub> + P<sub>2</sub> = P<sub>3</sub>_
  - _s = (y<sub>2</sub> - y<sub>1</sub>)(x<sub>2</sub> - x<sub>1</sub>)_
- The slope can be used to calculate _x<sub>3</sub>_
  - Once _x<sub>3</sub>_ is known, _y<sub>3</sub>_ can be calculated.
  - _P<sub>3</sub>_ can be derived using the following formula:
    - _x<sub>3</sub> = s<sup>2</sup> - x<sub>1</sub> - x<sub>2</sub>_
    - _y<sub>3</sub> = s(x<sub>1</sub>) - x<sub>3</sub>) - y<sub>1</sub>_
    - _y<sub>3</sub>_ is the reflection over the x-axis

### Deriving the point addition formula

- _P<sub>1</sub> = (x<sub>1></sub>, y<sub>1</sub>)_,
  _P<sub>2</sub> = (x<sub>2></sub>, y<sub>2</sub>)_,
  _P<sub>3</sub> = (x<sub>3></sub>, y<sub>3</sub>)_
- _P<sub>1</sub> + P<sub>2</sub> = P<sub>3</sub>_
- To figure out that _P<sub>3</sub>_ is:
  - The line that goes through _P<sub>1</sub>_ and _P<sub>2</sub>_ has the
    following formula:
    - _s = (y<sub>2</sub> - y<sub>1</sub>) / (x<sub>2</sub> - x<sub>1</sub>)_
    - _y = s(x - x<sub>1</sub>) + y<sub>1</sub>_
      - This is the equation of the line tha tintersects at both _P<sub>1</sub>_
        and _P<sub>2</sub>_
      - Plugging in this formula to the Elliptic Curve equation results in:
        - _y<sup>2</sup> = x<sup>3</sup> + ax + b_
        - _y<sup>2</sup> = (s(x - x<sub>1</sub>) + y<sub>1</sub>)<sup>2</sup> =_
          _x<sup>3</sup> + ax + b_
      - All the terms result in the following polynomial:
        - _x<sup>3</sup> - s<sup>2</sup> * x<sup>2</sup> +_
          _(a + 2s<sup>2</sup>) * x<sub>1</sub> - 2sy<sub>1</sub>) *_
          _x + b - x<sub>1</sub><sup>2</sup> + 2sx<sup>1</sup> *_
          _y<sub>1</sub> - y<sub>1</sub><sup>2</sup> = 0_
      - _x<sup>1</sup>_, _x<sup>2</sup>_, and _x<sup>3</sup>_ are solutions to
        this equation
        - _(x - x<sub>1</sub>) * (x - x<sub>2</sub>) * (x - x<sub>3</sub>) = 0_
        - _x<sup>3</sup> - (x<sub>1</sub> + x<sub>2</sub> + x<sub>3</sub>) *_
          _x<sup>2</sup> + (x<sub>1</sub> * x<sub>2</sub> + x<sub>1</sub> *_
          _x<sub>3</sub> + x<sub>2</sub> * x<sub>3</sub>) * x -_
          _x<sub>1</sub> * x<sub>2</sub> * x<sub>3</sub> = 0_