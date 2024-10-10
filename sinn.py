from math import sin, cos, radians

f = open("Created/WholeSINE_TABLE.txt", "w")

for i in range(360):
    f.write(str(sin(radians(i))) + "\n")

f.close()

f = open("Created/SINE_TABLE.txt", "w")
for i in range(0,10,1):
    f.write(str(sin(radians(i/10))) + "\n")

f.close()

f = open("Created/WholeCOSINE_TABLE.txt", "w")

for i in range(360):
    f.write(str(cos(radians(i))) + "\n")

f.close()

f = open("Created/COSINE_TABLE.txt", "w")

for i in range(0,10,1):
    f.write(str(cos(radians(i/10))) + "\n")

f.close()