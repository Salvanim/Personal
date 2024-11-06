import switchObject
from switchObject import *

class March:
    def __init__(self, content: list, rules: switchObject, origins=[(0, 0)]):
        self.content = content  # 2D array (list of lists)
        self.rules = rules
        self.origins = origins

    def next(self):
        for y in range(len(self.content)):  # Loop through rows
            for x in range(len(self.content[y])):  # Loop through columns
                originLength = len(self.origins)
                for o in range(originLength):
                    if self.origins[o] == (x, y):  # If current position is an origin
                        del self.origins[o]
                        # Loop through the 8 neighboring cells
                        for sx in range(-1, 2):
                            for sy in range(-1, 2):
                                if (sx != 0 or sy != 0) and (0 <= x+sx < len(self.content[y]) and 0 <= y+sy < len(self.content)):
                                    # Add new origin and update content based on rules
                                    self.origins.append((x+sx, y+sy))
                                    self.content[y+sy][x+sx] = self.rules(self.content[y+sy][x+sx])

def toggle(value):
    return switch(
        0, lambda: 1,  # If current value is 0, switch it to 1
        1, lambda: 0,  # If current value is 1, switch it to 0
          # Default: leave value unchanged
    )(value)

# Create a 2D grid (content) with initial states
content = [
    [0, 1, 0],
    [0, 1, 1],
    [1, 0, 0]
]

# Set the initial origins (starting points)
origins = [(1, 1)]  # Starting at the center of the grid

# Initialize the March object with the content, rules, and origins
march_simulation = March(content, toggle, origins)

# Print the initial state
print("Initial Grid:")
for row in march_simulation.content:
    print(row)

# Move to the next step in the simulation
march_simulation.next()

# Print the updated state
print("\nUpdated Grid:")
for row in march_simulation.content:
    print(row)
