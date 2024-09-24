import re

import numpy as np

def compString(s):
    if not s:
        return ""

    endString = ""
    count = 1
    prev_char = s[0]

    for i in range(1, len(s)):
        current_char = s[i]

        if current_char == prev_char:
            count += 1  # Increment count if same character as previous
        else:
            # Add previous character and its count to the string
            endString += prev_char
            if count > 4:
                endString += ":" + str(count) + ":"
            else:
                endString += prev_char * (count - 1)
            # Reset for the new character
            count = 1
            prev_char = current_char

    # Add the last character count
    endString += prev_char
    if count > 4:
        endString += ":" + str(count) + ":"
    else:
        endString += prev_char * (count - 1)

    return endString

def decompString(s):
    i = 0
    result = []

    while i < len(s):
        if s[i] == ':':
            # Check how many consecutive colons there are
            colon_count = 0
            while i < len(s) and s[i] == ':':
                colon_count += 1
                i += 1

            if colon_count % 2 == 0:
                # Even number of colons (including "::") should output literal colons
                result.append(':' * (colon_count // 2))
            else:
                # Handle cases like `:<count>:` compression pattern
                if i < len(s) and s[i].isdigit():
                    # We're expecting a number followed by another colon
                    count = ""
                    while i < len(s) and s[i].isdigit():
                        count += s[i]
                        i += 1

                    # Ensure the count is followed by a colon
                    if i < len(s) and s[i] == ':':
                        result.append(result.pop() * int(count))  # Repeat the last character
                        i += 1  # Move past the closing ':'
                    else:
                        # If no closing colon, treat the pattern as literal
                        result.append(':' * colon_count)
                else:
                    # If no number follows the colon, treat the pattern as literal
                    result.append(':' * colon_count)
        else:
            # Append normal characters
            result.append(s[i])
            i += 1

    return ''.join(result)

def char_indices(s):
    char_dict = {}

    for i, char in enumerate(s):
        if char not in char_dict:
            char_dict[char] = []
        char_dict[char].append(i)

    return char_dict

def reverse_char_indices(char_dict):
    # Find the length of the original string
    max_index = max([max(indices) for indices in char_dict.values()])

    # Initialize a list with None to hold characters in the correct order
    result = [None] * (max_index + 1)

    # Place each character in its respective indices
    for char, indices in char_dict.items():
        for index in indices:
            result[index] = char

    # Join the list into a string and return
    return ''.join(result)

