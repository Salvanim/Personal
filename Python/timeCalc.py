import timeit
def calcAverageRunTime(function, *args, testAmount = 10000):
    def calcRunTime():
        start = timeit.default_timer()
        function(*args)
        stop =  timeit.default_timer()
        return abs(stop-start)*1000
    lengths = []
    for _ in range(testAmount):
        lengths.append(calcRunTime())
    return sum(lengths)/len(lengths)

def calcRunTime(function, *args):
    start = timeit.default_timer()
    function(*args)
    stop =  timeit.default_timer()
    return abs(stop-start)*1000
