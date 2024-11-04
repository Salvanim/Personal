def isItterable(input):
    try:
        iter(input)
        return not isinstance(input, str)
    except:
        return False

def depths(array, count=0, lengths=[]):
    if isItterable(array):
        for val in array:
            depths(val, count + 1, lengths)
    else:
        lengths.append(count)
    return lengths

def flatten(array, content=[]):
    if isItterable(array):
        for val in array:
            flatten(val, content)
    else:
        content.append(array)
    return content

def genDepthList(depth, value):
    if depth < 1:
        return value
    else:
        return [genDepthList(depth-1, value)]

def merge_arrays(arr1, arr2):
    if isinstance(arr1, list) and isinstance(arr2, list):
        return [merge_arrays(a1, a2) for a1, a2 in zip(arr1, arr2)]
    else:
        return arr1 if isinstance(arr1, list) else [arr1] + [arr2]
