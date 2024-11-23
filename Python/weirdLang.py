def sepersToBin(string, isCharacter = False):
    output = ""
    for i in range(len(string)):
        if string[i] == ".":
            output += "1"
        elif string[i] == ",":
            output += "0"
        else:
            output += ''.join(format(ord(x), 'b') for x in string[i])

    return output

print(sepersToBin("", True))

