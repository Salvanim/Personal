
from typing import Any

class reverseCalcuation():
    def __init__(self, firstNum, secondNum):
        self.addTarget = firstNum + secondNum
        self.subTarget = firstNum - secondNum
        self.mulTarget = firstNum * secondNum
        self.divTarget = firstNum / secondNum
        self.expTarget = firstNum ^ secondNum
        self.index = secondNum

    def set(self, name, value):
        nameChange = {}
        nameChange.update(nameChange.fromkeys(['add', '+', 'addition', 'sum', 'addTarget'], 'addTarget'))
        nameChange.update(nameChange.fromkeys(['sub', '-', 'subtract', 'subtraction', 'diff', 'diffrence', 'subTarget'], 'subTarget'))
        nameChange.update(nameChange.fromkeys(['mult', '*', 'mul', 'multiply','mutiplication', 'multarget'], 'mulTarget'))
        nameChange.update(nameChange.fromkeys(['div', 'divide', '/', 'division', 'divTarget'], 'divTarget'))
        nameChange.update(nameChange.fromkeys(['exp', 'exponent', '^', 'exponention', 'pow', 'power', 'expTarget'], 'expTarget'))
        nameChange.update(nameChange.fromkeys(['index', 'placement', 'i', 'location', 'list placement'], 'index'))
        name = nameChange[name]
        setattr(self, name, value)

    def getValue(self, name):
        nameChange = {}
        nameChange.update(nameChange.fromkeys(['add', '+', 'addition', 'sum', 'addTarget'], 'addTarget'))
        nameChange.update(nameChange.fromkeys(['sub', '-', 'subtract', 'subtraction', 'diff', 'diffrence', 'subTarget'], 'subTarget'))
        nameChange.update(nameChange.fromkeys(['mult', '*', 'mul', 'multiply','mutiplication', 'multarget'], 'mulTarget'))
        nameChange.update(nameChange.fromkeys(['div', 'divide', '/', 'division', 'divTarget'], 'divTarget'))
        nameChange.update(nameChange.fromkeys(['exp', 'exponent', '^', 'exponention', 'pow', 'power', 'expTarget'], 'expTarget'))
        nameChange.update(nameChange.fromkeys(['index', 'placement', 'i', 'location', 'list placement'], 'index'))
        name = nameChange[name]
        return getattr(self, name)

    def getCalc(self, name, withResult = False):
        originName = name
        method_list = [func for func in dir(self) if callable(getattr(self, func)) and func.startswith('calc')]
        nameChange = {}
        nameChange.update(nameChange.fromkeys(['add', '+', 'addition', 'sum', 'addTarget'], 'calcAdd'))
        nameChange.update(nameChange.fromkeys(['sub', '-', 'subtract', 'subtraction', 'diff', 'diffrence', 'subTarget'], 'calcSub'))
        nameChange.update(nameChange.fromkeys(['mult', '*', 'mul', 'multiply','mutiplication', 'multarget'], 'calcMul'))
        nameChange.update(nameChange.fromkeys(['div', 'divide', '/', 'division', 'divTarget'], 'calcDiv'))
        nameChange.update(nameChange.fromkeys(['exp', 'exponent', '^', 'exponention', 'pow', 'power', 'expTarget'], 'calcExp'))
        name = nameChange[name]
        for method in method_list:
            if method == name:
                if withResult:
                    return getattr(self, method)(), self.getValue(originName)
                else:
                    return getattr(self, method)()

    def calcAdd(self):
        return self.addTarget - self.index, self.index

    def calcSub(self):
        return self.subTarget + self.index, self.index

    def calcMul(self):
        if self.index == 0:
            return self.mulTarget, 1
        return self.mulTarget/self.index, self.index

    def calcDiv(self):
        return self.divTarget*self.index, self.index

    def calcExp(self):
        return self.__log(self.expTarget) ** 1/self.index, self.index

    def __log(number, base=10, tolerance=0.5e-15):
        low, high = 0, number

        while high - low > tolerance:
            mid = (low + high) / 2
            mid_pow = base ** mid

            if mid_pow < number:
                low = mid
            else:
                high = mid
        return (low + high) / 2

value = reverseCalcuation(10, 10)
print(value.getCalc("+", True))
