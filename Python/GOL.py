import tkinter as tk
from tkinter import messagebox
import numpy as np

class Board:
    def __init__(self, xSize=30, ySize=30, randomize=False):
        self.xSize = xSize
        self.ySize = ySize
        self.looping = True
        self.state = np.zeros((self.xSize, self.ySize), dtype=bool)
        if randomize:
            self.randomize()

    def randomize(self):
        self.state = np.random.choice(a=[False, True], size=(self.xSize, self.ySize))

    def clear(self):
        self.state[:] = False

    def next_state(self):
        # Count neighbors using convolution
        neighbors = sum(np.roll(np.roll(self.state, i, 0), j, 1)
                        for i in (-1, 0, 1) for j in (-1, 0, 1)
                        if (i != 0 or j != 0))
        if self.looping:
            neighbors = neighbors % (self.xSize * self.ySize)
        # Apply rules
        birth = (neighbors == 3) & (~self.state)
        survive = ((neighbors == 2) | (neighbors == 3)) & self.state
        self.state = birth | survive

    def is_ended(self):
        # Check if the board has reached a stable state
        return False  # Simplified for performance; implement if needed

class MultiBoardGameOfLifeGUI:
    def __init__(self, root, num_boards=16, boards_per_row=4, board_size=30, cell_size=10, randomize=True):
        self.root = root
        self.num_boards = num_boards
        self.boards_per_row = boards_per_row
        self.board_size = board_size
        self.cell_size = cell_size
        self.running = False
        self.current_delay = 100  # milliseconds

        # Initialize boards
        self.boards = [Board(self.board_size, self.board_size, randomize=randomize) for _ in range(self.num_boards)]

        # Create main frames with scrollable area
        self.scrollable_frame = ScrollableFrame(root)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create PhotoImage canvases for each board
        self.canvases = []
        self.images = []
        for idx, board in enumerate(self.boards):
            row = idx // self.boards_per_row
            col = idx % self.boards_per_row
            canvas = tk.Canvas(self.scrollable_frame.scrollable_frame,
                               width=board.xSize * self.cell_size,
                               height=board.ySize * self.cell_size,
                               bg="white")
            canvas.grid(row=row, column=col, padx=2, pady=2)
            # Create a PhotoImage for the board
            image = tk.PhotoImage(width=board.xSize, height=board.ySize)
            canvas_image = canvas.create_image((0, 0), anchor="nw", image=image)
            self.canvases.append(canvas)
            self.images.append(image)
            # Bind click event
            canvas.bind("<Button-1>", lambda event, b=board: self.toggle_cell(event, b))
            self.update_photo(board, image)

        # Create shared controls
        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack(pady=5)

        self.start_button = tk.Button(self.controls_frame, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.controls_frame, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.step_button = tk.Button(self.controls_frame, text="Step", command=self.step)
        self.step_button.pack(side=tk.LEFT, padx=5)

        self.random_button = tk.Button(self.controls_frame, text="Random", command=self.randomize_boards)
        self.random_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.controls_frame, text="Clear", command=self.clear_boards)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.quit_button = tk.Button(self.controls_frame, text="Quit", command=self.root.quit)
        self.quit_button.pack(side=tk.LEFT, padx=5)

        # Dynamic Board Size Input
        self.size_frame = tk.Frame(root)
        self.size_frame.pack(pady=5)

        self.size_label = tk.Label(self.size_frame, text="Board Size:")
        self.size_label.pack(side=tk.LEFT)

        self.size_entry = tk.Entry(self.size_frame, width=5)
        self.size_entry.pack(side=tk.LEFT, padx=5)
        self.size_entry.insert(0, str(self.board_size))  # Default size

        self.set_size_button = tk.Button(self.size_frame, text="Set Size", command=self.set_board_size)
        self.set_size_button.pack(side=tk.LEFT)

        # Run Delay Input with validation
        self.delay_label = tk.Label(self.controls_frame, text="Run Delay (ms):")
        self.delay_label.pack(side=tk.LEFT, padx=(20, 5))

        def validate_input(P):
            if P == "":
                return True
            return P.isdigit()

        vcmd = (self.root.register(validate_input), '%P')

        self.delay_entry = tk.Entry(self.controls_frame, width=10, validate='key', validatecommand=vcmd)
        self.delay_entry.pack(side=tk.LEFT, padx=5)
        self.delay_entry.insert(0, str(self.current_delay))  # Default delay

        self.set_delay_button = tk.Button(self.controls_frame, text="Set", command=self.set_delay)
        self.set_delay_button.pack(side=tk.LEFT, padx=5)

        # Bind the Enter key to the set_delay method
        self.delay_entry.bind("<Return>", lambda event: self.set_delay())

    def toggle_cell(self, event, board):
        # Determine which board was clicked
        for idx, canvas in enumerate(self.canvases):
            bbox = canvas.bbox("all")
            x1, y1, x2, y2 = bbox
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                board_idx = idx
                break
        else:
            return  # Click was not on any canvas

        # Calculate cell coordinates
        cell_x = event.x // self.cell_size
        cell_y = event.y // self.cell_size
        if 0 <= cell_x < board.xSize and 0 <= cell_y < board.ySize:
            board.state[cell_x, cell_y] = not board.state[cell_x, cell_y]
            self.update_photo(board, self.images[board_idx])

    def update_photo(self, board, image):
        # Convert the boolean state to a list of color strings
        data = ""
        for y in range(board.ySize):
            row = ""
            for x in range(board.xSize):
                color = "black" if board.state[x, y] else "white"
                row += "black " if board.state[x, y] else "white "
            data += "{ " + row.strip() + "}\n"
        # Update the PhotoImage
        image.put(data)

    def update_all_photos(self):
        for board, image in zip(self.boards, self.images):
            self.update_photo(board, image)

    def start(self):
        if not hasattr(self, 'running') or not self.running:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.run()

    def stop(self):
        if hasattr(self, 'running') and self.running:
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def step(self):
        for board in self.boards:
            board.next_state()
        self.update_all_photos()

    def run(self):
        if self.running:
            self.step()
            self.root.after(self.current_delay, self.run)

    def randomize_boards(self):
        for board in self.boards:
            board.randomize()
        self.update_all_photos()

    def clear_boards(self):
        for board in self.boards:
            board.clear()
        self.update_all_photos()
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

    def set_board_size(self):
        size_str = self.size_entry.get()
        try:
            size = abs(int(size_str))
            if size <= 0:
                raise ValueError
            # Update board size
            self.board_size = size
            # Reinitialize boards
            self.boards = [Board(self.board_size, self.board_size, randomize=False) for _ in range(self.num_boards)]
            # Destroy existing canvases
            for canvas in self.canvases:
                canvas.destroy()
            self.canvases = []
            self.images = []
            # Recreate PhotoImages and canvases
            for idx, board in enumerate(self.boards):
                row = idx // self.boards_per_row
                col = idx % self.boards_per_row
                canvas = tk.Canvas(self.scrollable_frame.scrollable_frame,
                                   width=board.xSize * self.cell_size,
                                   height=board.ySize * self.cell_size,
                                   bg="white")
                canvas.grid(row=row, column=col, padx=2, pady=2)
                image = tk.PhotoImage(width=board.xSize, height=board.ySize)
                canvas_image = canvas.create_image((0, 0), anchor="nw", image=image)
                self.canvases.append(canvas)
                self.images.append(image)
                # Bind click event
                canvas.bind("<Button-1>", lambda event, b=board: self.toggle_cell(event, b))
                self.update_photo(board, image)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number for the board size.")

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self)
        scrollbar_v = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar_h = tk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        scrollbar_h.grid(row=1, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Game of Life - Multiple Boards Optimized")

    # Parameters
    NUM_BOARDS = 16         # Total number of boards
    BOARDS_PER_ROW = 4        # Number of boards per row in the grid
    BOARD_SIZE = 300           # Size of each board (30x30)
    CELL_SIZE = 10            # Pixel size of each cell
    RANDOMIZE_INITIAL = True  # Whether to randomize initial states

    game_gui = MultiBoardGameOfLifeGUI(root, num_boards=NUM_BOARDS, boards_per_row=BOARDS_PER_ROW,
                                      board_size=BOARD_SIZE, cell_size=CELL_SIZE, randomize=RANDOMIZE_INITIAL)

    # Handle window closing gracefully
    root.protocol("WM_DELETE_WINDOW", root.quit)

    root.mainloop()
