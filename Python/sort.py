def sortArray(array):
    sort = True
    while sort:
        for i in range(1,len(array)):
                if array[i-1] > array[i]:
                    temp = array[i]
                    array[i] = array[i-1]
                    array[i-1] = temp
        for i in range(1,len(array)):
            if array[i-1] > array[i]:
                break
        sort = False
    return array
