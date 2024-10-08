import random
import time

winAmount = int(input("WinAmount: "))
inputValue = 2

randomValue = random.randint(0, 1)
itterations = 0

wins = {}

while inputValue <= winAmount:
    winCount = 0
    while(randomValue != random.randint(0, 1)):
        inputValue *= 2
        winCount += 1
        randomValue = random.randint(0, 1)
    if inputValue in wins:
        wins[inputValue] = list(zip(wins[inputValue],[{"winCount":winCount, "itter":itterations}]))
    else:
        wins[inputValue] = [{"winCount":winCount, "itter":itterations}]

    itterations += 1

print(wins)
