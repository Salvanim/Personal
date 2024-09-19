import re

def compString(s):
    if not s:
        return ""

    result = []
    count = 1
    prev_char = s[0]

    for i in range(1, len(s)):
        current_char = s[i]

        if current_char == prev_char:
            count += 1  # Increment count if same character as previous
        else:
            # Store the count of consecutive characters as a tuple (character, count)
            result.append((prev_char, count))
            count = 1  # Reset count for the new character
            prev_char = current_char

    # Add the last character count
    result.append((prev_char, count))

    endString = ""
    for char, count in result:
        endString += char
        if count > 4:
            endString += ":" + str(count) + ":"
        else:
            endString += char * (count - 1)

    return endString

def decompressString(s):
    result = []
    i = 0

    while i < len(s):
        if i + 1 < len(s) and s[i + 1] == ':':
            char = s[i]
            i += 2
            count_end = s.index(':', i)
            count = int(s[i:count_end])
            result.append(char * count)
            i = count_end + 1
        else:
            result.append(s[i])
            i += 1

    return ''.join(result)

# Example usage
string = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
print(compString(string))
print(string == decompressString(compString(string)))
