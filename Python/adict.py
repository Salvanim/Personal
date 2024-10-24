import sys

def numContainReturn(num1, num2):
    sys.setrecursionlimit(round(sys.getrecursionlimit()*1.001))
    if str(num2).__contains__(str(num1)):
        return num2, num1
    else:
        num1 = int(str(num1)[1:])
        return numContainReturn(num1, num2)[0], num1

def continuousAdictSet(start, length, array=[], count=0):
    sys.maxsize *= 2
    sys.set_int_max_str_digits(round(sys.get_int_max_str_digits()*1.5))
    next = start**2
    array.append([start,next, numContainReturn(start, next)[1]])
    if count < length:
        return continuousAdictSet(numContainReturn(start, next)[0], length, array, count+1)
    else:
        return array

print(continuousAdictSet(25, 100))