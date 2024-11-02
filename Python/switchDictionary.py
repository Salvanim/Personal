from switch_package import switch
import random
t = switch(end=random.randint)


for n in range(100):
    t[n] = n+1


