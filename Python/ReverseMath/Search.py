import random
from random import randint
def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    while low <= high:
        mid = (high + low) // 2
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return mid
    return -1

def order(arr):
    changed = True
    count = 0
    while changed:
        changed = False
        for index in range(1, len(arr)):
            if arr[index-1] > arr[index]:
                temp = arr[index-1]
                arr[index-1] = arr[index]
                arr[index] = temp
                changed = True
                count += 1
            index += 1
    return arr

def quicksort(array):
    if len(array) < 2:
        return array

    low, same, high = [], [], []
    pivot = array[randint(0, len(array) - 1)]

    for item in array:
        if item < pivot:
            low.append(item)
        elif item == pivot:
            same.append(item)
        elif item > pivot:
            high.append(item)
    return quicksort(low) + same + quicksort(high)

array = list(range(0, 2))
random.shuffle(array)
print(array)
print(quicksort(array))
