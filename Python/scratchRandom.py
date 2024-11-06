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

    divisible = a
    while divisible >= b:
        divisible -= b

    divisible = divisible == 0

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

    if not divisible:
        count -= 1

    return output, count
