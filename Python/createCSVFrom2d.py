def isIterable(val):
    try:
        iter(val)
    except TypeError:
        return False
    return True

def get_depth(arr):
    if isIterable(arr) and type(arr) != str and arr:
        return 1 + max(get_depth(item) for item in arr)
    else:
        return 0

def generateArrayString(array, startingString='', count=0, savedArray=None, prev_depth=0):
    outputString = startingString
    index = 0
    if count == 0:
        savedArray = array if savedArray is None else savedArray

    for arr in array:
        current_depth = get_depth(arr)
        depth_difference = current_depth - prev_depth
        if depth_difference >= 0:
            outputString += '\n' * (depth_difference+1)

        if isIterable(arr) and not isinstance(arr, str):
            outputString = generateArrayString(arr, outputString, count+1, savedArray, current_depth)
            outputString += '\n'
        else:
            outputString += str(arr)
            if index != len(array) - 1:
                outputString += ","
        index += 1
    return outputString

def count_repeated_newlines(text):
    newline_counts = []
    
    current_count = 0
    
    for char in text:
        if char == '\n':
            current_count += 1
        else:
            if current_count > 0:
                newline_counts.append(current_count)
            current_count = 0
    
    if current_count > 0:
        newline_counts.append(current_count)
    
    return newline_counts

def csv2d(array, name):
    print(count_repeated_newlines(generateArrayString(array)))
    with open(name+'.csv', 'w') as file:
        file.write(generateArrayString(array))
    return file

def generate_multi_dimensional_array(value, dimensions, repeat):
    if dimensions == 1:
        return [value] * repeat
    return [generate_multi_dimensional_array(value, dimensions - 1, repeat) for _ in range(repeat)]


array = generate_multi_dimensional_array([1], 5, 30)
counts = count_repeated_newlines(generateArrayString(array))
countsSet = list(set(counts))
endDictionary = {}
for n in countsSet:
    endDictionary[n] = counts.count(n)
print(endDictionary)
#csv2d(array,'created')