import re
import time
import math
import random

class Turing:
    def __init__(self, startSet=[0], placement=0, changeRules={0:1, 1:0}, movementRules={"E": ["B", "extend_right"]}):
        self.set = startSet
        self.placement = placement
        self.crules = changeRules
        self.mrules = movementRules
        self.direction = 1

    def __call__(self):
        if self.placement < 0:
            self.placement = 0
        if self.placement > len(self)-1:
            self.placement = len(self)-1
        return self.set[self.placement]

    def __getitem__(self, index):
        self.placement = index
        return self()

    def __setitem__(self, index, other):
        self.set[index] = other

    def __len__(self):
        return len(self.set)

    def index(self, obj):
        return self.set.index(obj) if obj in self.set else -1

    def applyChangeRules(self):
        for rule, result in self.crules.items():
            if self[self.placement] == rule:
                self[self.placement] = result
                break

    def addCRule(self, key, value):
        self.crules[key] = value

    def getCRule(self, index):
        keys = list(self.crules.keys())
        values = list(self.crules.values())
        return keys[index], values[index]

    def cRuleLength(self):
        return len(self.crules)

    def addMRule(self, key, value):
        self.mrules[key] = value

    def getMRule(self, index):
        keys = list(self.mrules.keys())
        values = list(self.mrules.values())
        return keys[index], values[index]

    def mRuleLength(self):
        return len(self.mrules)

    def applyMovementRules(self):
        for rule, action in self.mrules.items():
            # Determine if the rule matches the current placement or condition
            atPoint = False
            rule = str(rule)
            if rule == "E":
                atPoint = (self.placement == len(self)-1)
            elif rule == "B":
                atPoint = (self.placement == 0)
            elif re.search("[iI]+", rule):
                afterI = rule.lower().split("i")[1]
                if afterI.isdigit():
                    atPoint = (self.placement == int(afterI))
                elif afterI == "H":
                    atPoint = (self.placement == math.floor((len(self))/2))
                else:
                    atPoint = (self.placement == self.index(afterI))
            elif rule == "H":
                atPoint = (self.placement == math.floor((len(self))/2))
            else:
                atPoint = (self[self.placement] == rule)

            # Apply action(s) if rule is met
            if atPoint:
                if isinstance(action, list):
                    for act in action:
                        self.execute_action(act)
                else:
                    self.execute_action(action)

    def execute_action(self, action):
        """Handles individual actions, including movement and extension."""
        if action == "E":
            self.placement = len(self)-1
        elif action == "B":
            self.placement = 0
        elif action == "F":
            self.direction = abs(self.direction)
        elif action == "H":
            self.placement = math.floor((len(self))/2)
        elif action == "R":
            self.direction *= -1
        elif isinstance(action, tuple) and action[0] == "ER":
            value = action[1] if len(action) > 1 else 0
            self.set.append(value)
        elif isinstance(action, tuple) and action[0] == "EL":
            value = action[1] if len(action) > 1 else 0
            self.set.insert(0, value)
            self.placement += 1
        elif callable(action):
            action(self)

    def __repr__(self):
        return f"Set: {self.set}"

    def __str__(self):
        return self.__repr__()

    def run(self, iterations=None, delay=1):
        count = 0
        while count != iterations:
            print(self)
            self.applyChangeRules()
            self.applyMovementRules()

            # Adjust placement based on the movement direction
            self.placement += self.direction
            count += 1
            time.sleep(delay)

# Testing with multiple actions for rule "E"
t = Turing(
    [0,0,0,0,0,0,0,0],
    changeRules={0:1, 1:0},
    movementRules={
        "E":["ER", "ER"],
        "B":"EL"
    }
)
t.run(iterations=255, delay=0.175)
