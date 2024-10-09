import re
import itertools

def generate_binary_strings(l):
    # Initialize an empty list to store the binary strings
    binary_strings = []
    
    # Loop over all lengths from 0 to l
    for length in range(l + 1):
        # Use itertools.product to generate all combinations of '0' and '1' of the given length
        for bits in itertools.product('01', repeat=length):
            # Join the bits tuple into a string and add it to the list
            binary_strings.append(''.join(bits))
    
    return binary_strings

# Example usage:
l = 3  # Set the maximum length
binary_strings = generate_binary_strings(l)


def check_regex(pattern, string):
    # Compile the regular expression pattern
    regex = re.compile(pattern)
    
    # Use the fullmatch method to check if the entire string matches the pattern
    if regex.fullmatch(string):
        return True
    else:
        return False

# Example usage:
pattern = "(0*|(0)*0)(0)*1*(1)*"  # Regular expression pattern (you can replace this with any regex)
test_string = '0011'  # String to test against the pattern


thing = generate_binary_strings(4)
print(thing)
for i in thing:
    result = check_regex(pattern, i)
    print(f"Does the string '{i}' match the pattern? {result}")
