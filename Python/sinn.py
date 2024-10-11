from math import sin, cos, radians

f = open("Created/WholeSINE_TABLE.txt", "w")

for i in range(360):
    f.write(str(sin(i)) + ",")

f.close()

f = open("Created/SINE_TABLE.txt", "w")
for i in range(1,10,1):
    f.write(str(sin(i/10)) + ",")

f.close()
