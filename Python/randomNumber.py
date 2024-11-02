from sympy import nextprime, prevprime
import time
import matplotlib.pyplot as plt

class SimpleRandom:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        current_time = int(''.join(str(time.time()).split(".")))
        closest_prime = self.closest_prime(current_time)
        self.seed = (self.seed * 48271) % closest_prime  # Using a known multiplier
        return self.seed % closest_prime

    def randint(self, min_value, max_value):
        if min_value > max_value:
            raise ValueError("min_value must be less than or equal to max_value")
        return min_value + self.next() % (max_value - min_value + 1)

    def sequence(self, min_value, max_value, size):
        if min_value > max_value:
            raise ValueError("min_value must be less than or equal to max_value")
        return [self.randint(min_value, max_value) for _ in range(size)]

    def closest_prime(self, n):
        return n - min(n - prevprime(n), nextprime(n) - n)
