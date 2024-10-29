import math

def more_and(a, b):
    return math.floor(1 - (a - b) / (abs(a - b) + 1))

def less_and(a, b):
    return math.floor(1 - (b - a) / (abs(b - a) + 1))

def equal(a, b):
    return (more_and(a, b) + less_and(a, b)) - 1

def not_equal(a, b):
    return abs(equal(a, b) - 1)

def more(a, b):
    return more_and(a, b) - (equal(a, b) - 1)

def less(a, b):
    return less_and(a, b) - (equal(a, b) - 1)

def more_check(t, f, comp1, comp2):
    return (t * more_and(comp1, comp2)) + (f * less(comp1, comp2))

def equal_check(t, f, comp1, comp2):
    return (t * equal(comp1, comp2)) + (f * not_equal(comp1, comp2))

def less_check(t, f, comp1, comp2):
    return (t * less_and(comp1, comp2)) + (f * more(comp1, comp2))

def i_f(in1, in2, operand, outTrue, outFalse):
    return equal_check(
        equal_check(outTrue, outFalse, in1, in2),
        equal_check(
            less_check(outTrue, outFalse, in1, in2),
            equal_check(
                more_check(outTrue, outFalse, in1, in2),
                0, operand, 3
            ),
            operand, 2
        ),
        operand, 1
    )

def f(x):
    return i_f(
        x, 0, 1,
        0,
        i_f(
            x, 0, 3,
            (-abs(x) ** abs(x)) + 1,
            (abs(x) ** abs(x)) - 1
        )
    ) + 1

print(i_f(10, 10, 1, 1, 0))
