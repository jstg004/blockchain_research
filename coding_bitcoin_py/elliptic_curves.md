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

        # Check if the point is on the curve:
        if self.y ** 2 != self.x ** 3 + self.a + self.x + self.b:
            # Throws and error is the point is not on the curve:
            raise ValueError(f'Point ({x}, {y}) is not on the curve')

    def __eq__(self, other):
        # Points are equal if and only if they are on the same curve
        # and have the same coordinates:
        return self.a == other.a and self.b == other.b \
            and self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.a != other.a and self.b != other.b \
            and self.x != other.x and self.y != other.y
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