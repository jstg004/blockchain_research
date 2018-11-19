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


    # check if objects in the class 'FieldElement' are =
    # only True when 'num' and 'prime' are =
    def __eq__(self, other):
        # python allows '==' operator to be replaced with the '__eq__' method
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime


    # check if objects in the class 'FieldElement' are not =
    # only True when 'num' and 'prime' are not =
    def __ne__(self, other):
        if other is None:
            return False
        return self.num != other.num and self.prime != other.prime