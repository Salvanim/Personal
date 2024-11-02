from switchObject import *
import random
def case0():
    return switch(0, False, 1, True)(random.randint(0, 1))

toggleBoolNumCOnversion = switch(0, case0())

print(toggleBoolNumCOnversion(0))
