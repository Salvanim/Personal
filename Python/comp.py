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
            count += 1
        else:
            endString += prev_char
            if count > 4:
                endString += ":" + str(count) + ":"
            else:
                endString += prev_char * (count - 1)
            count = 1
            prev_char = current_char
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
            colon_count = 0
            while i < len(s) and s[i] == ':':
                colon_count += 1
                i += 1

            if colon_count % 2 == 0:
                result.append(':' * (colon_count // 2))
            else:
                if i < len(s) and s[i].isdigit():
                    count = ""
                    while i < len(s) and s[i].isdigit():
                        count += s[i]
                        i += 1
                    if i < len(s) and s[i] == ':':
                        result.append(result.pop() * int(count))
                        i += 1
                    else:
                        result.append(':' * colon_count)
                else:
                    result.append(':' * colon_count)
        else:
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
    max_index = max([max(indices) for indices in char_dict.values()])
    result = [None] * (max_index + 1)
    for char, indices in char_dict.items():
        for index in indices:
            result[index] = char
    return ''.join(result)

