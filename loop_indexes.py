'''
How to loop with indexes in Python
'''

colors = ["red", "green", "blue", "purple"]
i = 0
while i < len(colors):
    print(colors[i])
    i += 1

'''
Range of length
'''
colors = ["red", "green", "blue", "purple"]
for i in range(len(colors)):
    print(colors[i])
# This first creates a range corresponding to the indexes in our list
# (0 to len(colors) - 1). We can loop over this range using Python’s for-in
# loop (really a foreach).
# This provides us with the index of each item in our colors list.
# To get the actual color, we use colors[i].

'''
For-in: the usual way
'''
# If you don't care about the indexes in our loop:
colors = ["red", "green", "blue", "purple"]
for color in colors:
    print(color)

'''
Deed indexes
    Use range(len(our_list)) and then lookup the index like before:
'''
presidents = ["Washington", "Adams", "Jefferson", "Madison", "Monroe", "Adams", "Jackson"]
for i in range(len(presidents)):
    print("President {}: {}".format(i + 1, presidents[i]))

'''
A more idiomatic way to accomplish this task:
    use the enumerate function
    Python’s built-in enumerate function allows us to loop over a list and
    retrieve both the index and the value of each item in the list:
'''
presidents = ["Washington", "Adams", "Jefferson", "Madison", "Monroe", "Adams", "Jackson"]
for num, name in enumerate(presidents, start=1):
    print("President {}: {}".format(num, name))


'''
Loop over multiple things
'''
# enumerate
# looping over two lists at the same time using indexes to look up
# corresponding elements:
colors = ["red", "green", "blue", "purple"]
ratios = [0.2, 0.3, 0.1, 0.4]
for i, color in enumerate(colors):
    ratio = ratios[i]
    print("{}% {}".format(ratio * 100, color))
# only need the index in this scenario because we’re using it to lookup
# elements at the same index in our second list

# zip
#  to loop over two lists at once
# zip function allows us to loop over multiple lists at the same time:
colors = ["red", "green", "blue", "purple"]
ratios = [0.2, 0.3, 0.1, 0.4]
for color, ratio in zip(colors, ratios):
    print("{}% {}".format(ratio * 100, color))
# The zip function takes multiple lists and returns an iterable that provides
# a tuple of the corresponding elements of each list as we loop over it.



######################

# Loop over a single list with a regular for-in:
for n in numbers:
    print(n)


# Loop over multiple lists at the same time with zip:
for header, rows in zip(headers, columns):
    print("{}: {}".format(header, ", ".join(rows)))


# Loop over a list while keeping track of indexes with enumerate:
for num, line in enumerate(lines):
    print("{0:03d}: {}".format(num, line))



# If you need to loop over multiple lists at the same time, use zip
# If you only need to loop over a single list just use a for-in loop
# If you need to loop over a list and you need item indexes, use enumerate
