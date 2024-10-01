import tkinter as tk
from tkinter import messagebox
import random

class Cell:
    def __init__(self, isOn, onCharacter=1, offCharacter=0, xLocation=0, yLocation=0):
        self.isOn = isOn
        self.on = onCharacter
        self.off = offCharacter
        self.x = xLocation
        self.y = yLocation
        self.next_state = isOn  # Initialize next_state with current state

    def toggle(self):
        self.isOn = not self.isOn

    def getNeighbors(self, board):
        neighbors = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue  # Exclude the cell itself
                nx = self.x + dx
                ny = self.y + dy

                if board.looping:
                    # Wrap around the edges using modulo operator for toroidal wrapping
                    nx = nx % board.xSize
                    ny = ny % board.ySize
                    neighbors.append((nx, ny))
                else:
                    # Only include neighbors within the grid bounds
                    if 0 <= nx < board.xSize and 0 <= ny < board.ySize:
                        neighbors.append((nx, ny))
        return neighbors

    def numNeighborsOn(self, board):
        onCount = 0
        for (nx, ny) in self.getNeighbors(board):
            if board.state[nx][ny].isOn:
                onCount += 1
        return onCount

    def computeNextState(self, board):
        numNeighbors = self.numNeighborsOn(board)
        if numNeighbors == 3:
            self.next_state = True
        elif numNeighbors < 2 or numNeighbors > 3:
            self.next_state = False
        else:
            self.next_state = self.isOn  # Remain in the current state

    def applyNextState(self):
        self.isOn = self.next_state

class Board:
    def __init__(self, xSize=30, ySize=30, randomize=False):
        self.xSize = xSize
        self.ySize = ySize
        self.state = []
        self.looping = True  # Default to looping (toroidal wrapping)
        self.generateNew(randomize)

    def generateNew(self, randomize=False):
        self.state = []
        for x in range(self.xSize):
            row = []
            for y in range(self.ySize):
                isOn = bool(random.randint(0, 1)) if randomize else False
                row.append(Cell(isOn, 1, 0, x, y))
            self.state.append(row)

    def nextState(self):
        # Phase 1: Compute next_state for all cells based on current state
        for x in range(self.xSize):
            for y in range(self.ySize):
                self.state[x][y].computeNextState(self)

        # Phase 2: Apply next_state to update isOn
        for x in range(self.xSize):
            for y in range(self.ySize):
                self.state[x][y].applyNextState()

    def clear(self):
        for row in self.state:
            for cell in row:
                cell.isOn = False

    def isEnded(self):
        for x in range(self.xSize):
            for y in range(self.ySize):
                cell = self.state[x][y]
                numNeighbors = cell.numNeighborsOn(self)
                if (cell.isOn and not (numNeighbors == 2 or numNeighbors == 3)) or \
                   (not cell.isOn and numNeighbors != 3):
                    return False  # The game is not ended
        return True  # The game has ended

class GameOfLifeGUI():
    def __init__(self, root, board):
        self.root = root
        self.board = board
        self.running = False
        self.cell_size = 20

        # Create Canvas
        self.canvas = tk.Canvas(root, width=self.board.xSize * self.cell_size,
                                height=self.board.ySize * self.cell_size, bg="white")
        self.canvas.pack()

        # Create Control Frame
        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack(pady=10)

        # Start Button
        self.start_button = tk.Button(self.controls_frame, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Stop Button
        self.stop_button = tk.Button(self.controls_frame, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Step Button
        self.step_button = tk.Button(self.controls_frame, text="Step", command=self.step)
        self.step_button.pack(side=tk.LEFT, padx=5)

        # Random Button
        self.random_button = tk.Button(self.controls_frame, text="Random", command=self.random)
        self.random_button.pack(side=tk.LEFT, padx=5)

        # Clear Button
        self.clear_button = tk.Button(self.controls_frame, text="Clear", command=self.clear_board)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Toggle Looping Button
        self.toggle_looping_button = tk.Button(self.controls_frame, text="Looping: On", command=self.toggle_looping)
        self.toggle_looping_button.pack(side=tk.LEFT, padx=5)

        # Quit Button
        self.quit_button = tk.Button(self.controls_frame, text="Quit", command=self.root.quit)
        self.quit_button.pack(side=tk.LEFT, padx=5)

        # Dynamic Board Size Input
        self.size_frame = tk.Frame(root)
        self.size_frame.pack(pady=10)

        self.size_label = tk.Label(self.size_frame, text="Board Size:")
        self.size_label.pack(side=tk.LEFT)

        self.size_entry = tk.Entry(self.size_frame, width=5)
        self.size_entry.pack(side=tk.LEFT, padx=5)
        self.size_entry.insert(0, "30")  # Default size

        self.set_size_button = tk.Button(self.size_frame, text="Set Size", command=self.set_board_size)
        self.set_size_button.pack(side=tk.LEFT)

        # Run Delay Input with validation
        self.delay_label = tk.Label(self.controls_frame, text="Run Delay (ms):")
        self.delay_label.pack(side=tk.LEFT, padx=(20, 5))

        # Define validation function
        def validate_input(P):
            if P == "":
                return True
            return P.isdigit()

        vcmd = (self.root.register(validate_input), '%P')

        self.delay_entry = tk.Entry(self.controls_frame, width=10, validate='key', validatecommand=vcmd)
        self.delay_entry.pack(side=tk.LEFT, padx=5)
        self.delay_entry.insert(0, "100")  # Default delay

        self.set_delay_button = tk.Button(self.controls_frame, text="Set", command=self.set_delay)
        self.set_delay_button.pack(side=tk.LEFT, padx=5)

        self.current_delay = 100  # Initial delay in milliseconds

        # Bind the Enter key to the set_delay method
        self.delay_entry.bind("<Return>", lambda event: self.set_delay())

        # Bind Click Event to Toggle Cells
        self.canvas.bind("<Button-1>", self.toggle_cell)

        # Draw Initial State
        self.update_canvas()

    def set_board_size(self):
        size_str = self.size_entry.get()
        try:
            size = abs(int(size_str))
            new_state = self.generate_new_state(size)  # Generate new state based on the new size
            self.board = Board(size, size, randomize=False)  # Create a new board with the specified size
            self.board.state = new_state  # Assign the new state to the new board
            self.update_canvas()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the board size.")

    def generate_new_state(self, new_size):
        # Create a new state array for the new board size
        new_state = []
        for x in range(new_size):
            row = []
            for y in range(new_size):
                # Retain cell state if the position was previously occupied, else create a new Cell
                if x < self.board.xSize and y < self.board.ySize:
                    isOn = self.board.state[x][y].isOn
                else:
                    isOn = False
                row.append(Cell(isOn, 1, 0, x, y))
            new_state.append(row)
        return new_state

    def toggle_cell(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 0 <= x < self.board.xSize and 0 <= y < self.board.ySize:
            self.board.state[x][y].toggle()
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        for x in range(self.board.xSize):
            for y in range(self.board.ySize):
                color = "black" if self.board.state[x][y].isOn else "white"
                self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill=color, outline="gray"
                )

    def start(self):
        if not self.running:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.toggle_looping_button.config(state=tk.DISABLED)
            self.run()

    def stop(self):
        if self.running:
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.toggle_looping_button.config(state=tk.NORMAL)

    def step(self):
        self.board.nextState()
        self.update_canvas()
        if self.board.isEnded():
            self.stop()

    def run(self):
        if self.running:
            self.step()
            self.root.after(self.current_delay, self.run)

    def random(self):
        self.board.generateNew(randomize=True)
        self.update_canvas()

    def clear_board(self):
        self.board.clear()
        self.update_canvas()
        self.stop()

    def set_delay(self):
        delay_str = self.delay_entry.get()
        try:
            delay = abs(int(delay_str))
            if delay == 0:
                raise ValueError
            self.current_delay = delay
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a non-zero number for the delay.")
            self.delay_entry.delete(0, tk.END)
            self.delay_entry.insert(0, str(self.current_delay))  # Revert to previous valid delay

    def toggle_looping(self):
        self.board.looping = not self.board.looping
        state = "On" if self.board.looping else "Off"
        self.toggle_looping_button.config(text=f"Looping: {state}")

    def on_closing(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Game of Life")

    board = Board(30, 30, randomize=True)  # Create a 30x30 board with random starting cells
    game_gui = GameOfLifeGUI(root, board)

    # Handle window closing gracefully
    root.protocol("WM_DELETE_WINDOW", game_gui.on_closing)

    root.mainloop()
