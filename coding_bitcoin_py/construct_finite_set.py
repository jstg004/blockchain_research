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