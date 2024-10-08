def dmul(num1, num2):
    max_num1 = int('9' * len(str(num1)))
    max_num2 = int('9' * len(str(num2)))
    max_product = max_num1 * max_num2
    multiples = list(range(num1, max_product + 1, num1))
    return multiples[num2 - 1]


num1 = int(input("Num 1: "))
num2 = int(input("Num 2: "))

print(dmul(num1, num2))
