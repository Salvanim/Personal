def pairPrime(n):
    # List to store pairs of factors
    pair_factors = []

    # Loop from 1 to the square root of n
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:  # If i is a factor
            pair_factors.append((i, n // i))  # Append the pair (i, n // i)

    return pair_factors

def prime(n):

    # All prime numbers are odd except two
    if (n & 1):
        n -= 2
    else:
        n -= 1

    i,j = 0,3

    for i in range(n, 2, -2):
        if(i % 2 == 0):
            continue

        while(j <= floor(math.sqrt(i)) + 1):
            if (i % j == 0):
                break
            j += 2

        if (j > floor(math.sqrt(i))):
            return i

    # It will only be executed when n is 3
    return 2
