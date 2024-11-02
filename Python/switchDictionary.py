from switchObject import *

def otherwise(input):
    return str(input).isdigit()

toggleBoolNumCOnversion = switch(0, False, False, 0, True, 1, 1, True, otherwise)

print(toggleBoolNumCOnversion(3))
