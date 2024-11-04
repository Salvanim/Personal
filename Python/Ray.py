def Array2D(sizeX, sizeY):
    array = []
    for _ in range(sizeY):
        innerArray = []
        for _ in range(sizeX):
            innerArray.append([0])
        array.append(innerArray)
    return array

def strArray2D(Array2D):
    string = ""
    sizeY = len(Array2D)
    sizeX = max(list(map(len, Array2D)))
    for y in range(sizeY):
        innerString = "\n"
        for x in range(sizeX):
            print(Array2D[y][x])
            innerString += Array2D[y][x]
        string += innerString
    return string

print(strArray2D(Array2D(10,10)))

