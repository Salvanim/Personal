def mod(a, b):
    aNeg = a < 0
    bNeg = b < 0

    a = abs(a)
    b = abs(b)
    sum = 0
    count = 0
    while sum < a and count < a:
        sum += b
        count += 1

    diff = (max(sum, a) - min(sum, a))

    output = 0

    if aNeg and not bNeg:
        output = diff
    elif bNeg and not aNeg:
        output = -diff
    elif aNeg and bNeg:
        output = -(b - diff)
    else:
        output = (b - diff)

    return output


a = int(input("Enter 1st Number: "))
b = int(input("Enter 2nd Number: "))

print(mod(a, b))
print(a % b)
