class TuringMachine:
    def __init__(self, tape, transition_function, start_state, halt_state):
        self.tape = tape
        self.head = 0
        self.state = start_state
        self.transition_function = transition_function
        self.halt_state = halt_state

    def step(self):
        current_symbol = self.tape[self.head]
        if (self.state, current_symbol) in self.transition_function:
            new_state, new_symbol, direction = self.transition_function[(self.state, current_symbol)]
            self.tape[self.head] = new_symbol  # Write symbol
            self.state = new_state  # Change state

            # Move head
            if direction == "R":
                self.head += 1
            elif direction == "L":
                self.head -= 1

            # Ensure head does not go out of bounds (extend tape if necessary)
            if self.head < 0:
                self.tape.insert(0, 0)  # Extend tape to the left
                self.head = 0
            elif self.head >= len(self.tape):
                self.tape.append(0)  # Extend tape to the right

    def __repr__(self):
        return f"{self.tape}"

    def run(self):
        while self.state != self.halt_state:
            print(self)
            self.step()

# Example transition function
transition_function = {
    (0, 0): (0, 1, "R"),
    (0, 1): (1, 1, "R"),
    (1, 0): (1, 1, "L"),
    (1, 1): (2, 0, "L"),  # Halt condition
}

# Create a Turing machine
tm = TuringMachine(tape=[0, 0, 0, 0], transition_function=transition_function, start_state=0, halt_state=2)
tm.run()
print(tm.tape)
