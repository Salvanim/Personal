def compString(inputString):
    currentLetter = inputString[0]
    stringCharacters = list(inputString)
    currentCount = 0
    endingString = ""
    for string in stringCharacters:
        if string != currentLetter:
            endingString += currentLetter + str(currentCount)
            currentCount = 1
            currentLetter = string
        else:
            currentCount += 1
    endingString += currentLetter + str(currentCount)
    if len(endingString) > len(inputString):
        return inputString
    return endingString

print(compString("Helloooo"))