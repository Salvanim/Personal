import os
def clearConsole():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def typedText(text):
    textList = list(text)
    outputText = ""
    for t in textList:
        outputText += t
        print(outputText)
        clearConsole()
    print(outputText)

typedText("assdfghjklqwqertyuiopzxcvbnm<>?,./:{[]}|1234567890_+=-)(*&^%$#@!`~    )")