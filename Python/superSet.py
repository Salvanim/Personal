def stringAdd(string1, string2):
    # Split the input strings into whole and decimal parts
    if '.' in string1:
        whole1, decimal1 = string1.split('.')
    else:
        whole1, decimal1 = string1, '0'

    if '.' in string2:
        whole2, decimal2 = string2.split('.')
    else:
        whole2, decimal2 = string2, '0'

    # Pad the decimal parts to equal length
    max_decimal_len = max(len(decimal1), len(decimal2))
    decimal1 += '0' * (max_decimal_len - len(decimal1))
    decimal2 += '0' * (max_decimal_len - len(decimal2))

    # Add the whole numbers and decimal parts separately
    whole_sum = stringAddWithoutDecimal(whole1, whole2)
    decimal_sum = stringAddWithoutDecimal(decimal1, decimal2)

    # Handle decimal carry if the sum is longer than the original decimal length
    if len(decimal_sum) > max_decimal_len:
        whole_sum = stringAddWithoutDecimal(whole_sum, '1')
        decimal_sum = decimal_sum[1:]  # Remove carry digit

    return f"{whole_sum}.{decimal_sum}".rstrip('0').rstrip('.')

def stringAddWithoutDecimal(string1, string2):
    # Same as before (without decimal handling)
    differenceZeros = "0" * (max(len(string1), len(string2)) - min(len(string1), len(string2)))
    if len(string1) < len(string2):
        string1 = differenceZeros + string1
    elif len(string1) > len(string2):
        string2 = differenceZeros + string2

    string1Numbers = list(map(int, string1))
    string2Numbers = list(map(int, string2))

    outputStringList = []
    carry = 0

    for i in range(len(string1Numbers)-1, -1, -1):
        sum_digits = string1Numbers[i] + string2Numbers[i] + carry
        carry = sum_digits // 10
        outputStringList.append(str(sum_digits % 10))

    if carry:
        outputStringList.append(str(carry))

    return ''.join(outputStringList[::-1])


def stringMultiply(string1, string2):
    decimal_places = 0
    if '.' in string1:
        decimal_places += len(string1) - string1.index('.') - 1
        string1 = string1.replace('.', '')
    if '.' in string2:
        decimal_places += len(string2) - string2.index('.') - 1
        string2 = string2.replace('.', '')
    product = stringMultiplyWithoutDecimal(string1, string2)
    if decimal_places > 0:
        product = product[:-decimal_places] + '.' + product[-decimal_places:]

    return product.rstrip('0').rstrip('.')

def stringMultiplyWithoutDecimal(string1, string2):
    string1 = string1[::-1]
    string2 = string2[::-1]
    result = [0] * (len(string1) + len(string2))

    for i in range(len(string1)):
        for j in range(len(string2)):
            mul = int(string1[i]) * int(string2[j])
            result[i + j] += mul
            if result[i + j] >= 10:
                result[i + j + 1] += result[i + j] // 10
                result[i + j] %= 10

    while len(result) > 1 and result[-1] == 0:
        result.pop()

    return ''.join(map(str, result[::-1]))

def stringSubtract(string1, string2):
    # Split the input strings into whole and decimal parts
    if '.' in string1:
        whole1, decimal1 = string1.split('.')
    else:
        whole1, decimal1 = string1, '0'

    if '.' in string2:
        whole2, decimal2 = string2.split('.')
    else:
        whole2, decimal2 = string2, '0'

    # Pad the decimal parts to equal length
    max_decimal_len = max(len(decimal1), len(decimal2))
    decimal1 += '0' * (max_decimal_len - len(decimal1))
    decimal2 += '0' * (max_decimal_len - len(decimal2))

    # Subtract the whole numbers and decimal parts separately
    decimal_diff = stringSubtractWithoutDecimal(decimal1, decimal2)
    whole_diff = stringSubtractWithoutDecimal(whole1, whole2)

    # Handle borrowing if necessary for decimals
    if len(decimal_diff) > max_decimal_len:
        whole_diff = stringSubtractWithoutDecimal(whole_diff, '1')
        decimal_diff = decimal_diff[1:]

    return f"{whole_diff}.{decimal_diff}".rstrip('0').rstrip('.')

def stringSubtractWithoutDecimal(string1, string2):
    # Ensure string1 is the larger number
    if len(string1) < len(string2) or (len(string1) == len(string2) and string1 < string2):
        string1, string2 = string2, string1  # Swap to avoid negative results
        negative = True
    else:
        negative = False

    differenceZeros = "0" * (len(string1) - len(string2))
    string2 = differenceZeros + string2

    string1Numbers = list(map(int, string1))
    string2Numbers = list(map(int, string2))

    outputStringList = []

    for i in range(len(string1Numbers) - 1, -1, -1):
        if string1Numbers[i] < string2Numbers[i]:
            string1Numbers[i] += 10
            string1Numbers[i - 1] -= 1
        result = string1Numbers[i] - string2Numbers[i]
        outputStringList.append(str(result))

    outputStringList = outputStringList[::-1]
    while len(outputStringList) > 1 and outputStringList[0] == '0':
        outputStringList.pop(0)

    if negative:
        outputStringList.insert(0, '-')

    return ''.join(outputStringList)

def stringDivide(string1, string2, precision=10):
    if string2 == '0' or string1 == '0':
        return "0"
    decimal_places1 = 0
    if '.' in string1:
        decimal_places1 = len(string1) - string1.index('.') - 1
        string1 = string1.replace('.', '')

    decimal_places2 = 0
    if '.' in string2:
        decimal_places2 = len(string2) - string2.index('.') - 1
        string2 = string2.replace('.', '')
    total_decimal_places = decimal_places1 - decimal_places2
    quotient, remainder = longDivision(string1, string2, precision)
    if total_decimal_places > 0:
        if len(quotient) <= total_decimal_places:
            quotient = '0.' + '0' * (total_decimal_places - len(quotient)) + quotient
        else:
            quotient = quotient[:-total_decimal_places] + '.' + quotient[-total_decimal_places:]
    elif total_decimal_places < 0:
        quotient += '0' * abs(total_decimal_places)
    quotient = quotient.rstrip('0').rstrip('.')

    return quotient if quotient else '0'

def longDivision(dividend, divisor, precision):
    quotient = []
    remainder = '0'

    for digit in dividend:
        remainder = str(int(remainder + digit))
        quotient_digit = 0
        while int(remainder) >= int(divisor):
            remainder = str(int(remainder) - int(divisor))
            quotient_digit += 1
        quotient.append(str(quotient_digit))

    if remainder != '0':
        quotient.append('.')
        for _ in range(precision):
            remainder += '0'
            quotient_digit = 0
            while int(remainder) >= int(divisor):
                remainder = str(int(remainder) - int(divisor))
                quotient_digit += 1
            quotient.append(str(quotient_digit))
            if remainder == '0':
                break

    return remove_leading_zeros(''.join(quotient)), remainder

def remove_leading_zeros(number_string):
    cleaned_string = number_string.lstrip('0')
    if cleaned_string[0] == '.':
        cleaned_string = "0" + cleaned_string
    return cleaned_string if cleaned_string else '0'



