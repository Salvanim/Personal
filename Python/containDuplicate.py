def containDuplicate(array):
    seen = set()
    for element in array:
        if element in seen:
            return True  # Duplicate found
        seen.add(element)
    return False

print(containDuplicate([1,2,3,4,5]))
