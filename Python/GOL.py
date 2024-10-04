import tkinter as tk
from tkinter import messagebox
import numpy as np
from tkinter import ttk
import threading
import time
import copy
from bs4 import BeautifulSoup
import webbrowser
import image


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

class GUI:
    def __init__(self, title="Custom GUI", width=800, height=600):
        # Initialize the root window
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)  # Optional: Prevent window resizing

        # Dictionary to store widgets with unique identifiers
        self.widgets = {}

    # --- Adding Widgets ---
    def add_label(self, identifier, text, x, y, font=("Arial", 12), color="black"):
        label = tk.Label(self.root, text=text, font=font, fg=color)
        label.place(x=x, y=y)
        self.widgets[identifier] = label
        return label

    def add_button(self, identifier, text, x, y, command=None, width=10, height=2):
        button = tk.Button(self.root, text=text, command=command, width=width, height=height)
        button.place(x=x, y=y)
        self.widgets[identifier] = button
        return button

    def add_entry(self, identifier, x, y, width=20):
        entry = tk.Entry(self.root, width=width)
        entry.place(x=x, y=y)
        self.widgets[identifier] = entry
        return entry

    def add_text(self, identifier, x, y, width=40, height=10):
        text = tk.Text(self.root, width=width, height=height)
        text.place(x=x, y=y)
        self.widgets[identifier] = text
        return text

    def add_checkbox(self, identifier, text, x, y, variable=None, command=None):
        if variable is None:
            variable = tk.IntVar()
        checkbox = tk.Checkbutton(self.root, text=text, variable=variable, command=command)
        checkbox.place(x=x, y=y)
        self.widgets[identifier] = (checkbox, variable)
        return checkbox, variable

    def add_radiobutton(self, identifier, text, x, y, variable, value, command=None):
        radiobutton = tk.Radiobutton(self.root, text=text, variable=variable, value=value, command=command)
        radiobutton.place(x=x, y=y)
        self.widgets[identifier] = radiobutton
        return radiobutton

    def add_dropdown(self, identifier, options, x, y, width=20, command=None):
        variable = tk.StringVar(self.root)
        variable.set(options[0] if options else "")
        dropdown = ttk.Combobox(self.root, textvariable=variable, values=options, width=width)
        if command:
            dropdown.bind("<<ComboboxSelected>>", lambda event: command(variable.get()))
        dropdown.place(x=x, y=y)
        self.widgets[identifier] = (dropdown, variable)
        return dropdown, variable

    def add_canvas(self, identifier, x, y, width=200, height=200, bg="white"):
        canvas = tk.Canvas(self.root, width=width, height=height, bg=bg)
        canvas.place(x=x, y=y)
        self.widgets[identifier] = canvas
        return canvas

    # --- Retrieving Widgets ---
    def get_widget(self, identifier):
        return self.widgets.get(identifier, None)

    # --- Updating Widgets ---
    def update_label(self, identifier, new_text):
        widget = self.get_widget(identifier)
        if isinstance(widget, tk.Label):
            widget.config(text=new_text)
        else:
            print(f"No Label found with identifier '{identifier}'.")

    def update_button(self, identifier, new_text=None, new_command=None):
        widget = self.get_widget(identifier)
        if isinstance(widget, tk.Button):
            if new_text:
                widget.config(text=new_text)
            if new_command:
                widget.config(command=new_command)
        else:
            print(f"No Button found with identifier '{identifier}'.")

    def update_entry(self, identifier, new_text=None):
        widget = self.get_widget(identifier)
        if isinstance(widget, tk.Entry):
            if new_text is not None:
                widget.delete(0, tk.END)
                widget.insert(0, new_text)
        else:
            print(f"No Entry found with identifier '{identifier}'.")

    def update_checkbox(self, identifier, new_state=None):
        widget = self.get_widget(identifier)
        if isinstance(widget, tuple) and isinstance(widget[0], tk.Checkbutton):
            checkbox, variable = widget
            if new_state is not None:
                variable.set(new_state)
        else:
            print(f"No Checkbutton found with identifier '{identifier}'.")

    def update_dropdown(self, identifier, new_options=None, new_selected=None):
        widget = self.get_widget(identifier)
        if isinstance(widget, tuple) and isinstance(widget[0], ttk.Combobox):
            dropdown, variable = widget
            if new_options is not None:
                dropdown['values'] = new_options
            if new_selected is not None:
                variable.set(new_selected)
        else:
            print(f"No Combobox found with identifier '{identifier}'.")

    # --- Additional Methods ---
    def remove_widget(self, identifier):
        widget = self.get_widget(identifier)
        if widget:
            if isinstance(widget, tuple):
                widget = widget[0]
            widget.destroy()
            del self.widgets[identifier]
            print(f"Widget '{identifier}' removed.")
        else:
            print(f"No widget found with identifier '{identifier}'.")

    def move_widget(self, identifier, new_x, new_y):
        widget = self.get_widget(identifier)
        if widget:
            if isinstance(widget, tuple):
                widget = widget[0]
            widget.place(x=new_x, y=new_y)
            print(f"Widget '{identifier}' moved to ({new_x}, {new_y}).")
        else:
            print(f"No widget found with identifier '{identifier}'.")

    def style_label(self, identifier, font=None, color=None):
        widget = self.get_widget(identifier)
        if isinstance(widget, tk.Label):
            if font:
                widget.config(font=font)
            if color:
                widget.config(fg=color)
            print(f"Label '{identifier}' styled.")
        else:
            print(f"No Label found with identifier '{identifier}'.")

    def style_button(self, identifier, font=None, color=None, bg=None):
        widget = self.get_widget(identifier)
        if isinstance(widget, tk.Button):
            if font:
                widget.config(font=font)
            if color:
                widget.config(fg=color)
            if bg:
                widget.config(bg=bg)
            print(f"Button '{identifier}' styled.")
        else:
            print(f"No Button found with identifier '{identifier}'.")

    def style_entry(self, identifier, font=None, bg=None, fg=None):
        widget = self.get_widget(identifier)
        if isinstance(widget, tk.Entry):
            if font:
                widget.config(font=font)
            if bg:
                widget.config(bg=bg)
            if fg:
                widget.config(fg=fg)
            print(f"Entry '{identifier}' styled.")
        else:
            print(f"No Entry found with identifier '{identifier}'.")

    # --- Running the GUI ---
    def run(self):
        self.root.mainloop()

# --- Game of Life Implementation ---
class GameOfLife:
    def __init__(self, gui, canvas_id, grid_size=50, cell_size=10, alive_color="black", dead_color="white"):
        self.gui = gui
        self.canvas = self.gui.get_widget(canvas_id)
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.alive_color = alive_color
        self.dead_color = dead_color

        self.grid = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.generation = 0
        self.running = False
        self.speed = 10

        self.history = []

        self.draw_grid()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def draw_grid(self):
        self.canvas.delete("all")
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                fill = self.alive_color if self.grid[row][col] else self.dead_color
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="gray")

    def toggle_cell(self, row, col):
        self.grid[row][col] = not self.grid[row][col]
        self.draw_grid()

    def on_canvas_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.toggle_cell(row, col)
            self.history = self.history[:self.generation]

    def count_neighbors(self, row, col):
        count = 0
        for i in range(max(0, row - 1), min(self.grid_size, row + 2)):
            for j in range(max(0, col - 1), min(self.grid_size, col + 2)):
                if (i, j) != (row, col) and self.grid[i][j]:
                    count += 1
        return count

    def next_generation(self):

        self.history.append(copy.deepcopy(self.grid))
        if len(self.history) > 1000:
            self.history.pop(0)

        new_grid = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                neighbors = self.count_neighbors(row, col)
                if self.grid[row][col]:
                    if neighbors in [2, 3]:
                        new_grid[row][col] = True
                else:
                    if neighbors == 3:
                        new_grid[row][col] = True
        self.grid = new_grid
        self.generation += 1
        self.gui.update_label("generation_label", f"Generation: {self.generation}")
        self.draw_grid()

    def run_simulation(self):
        if self.running:
            self.next_generation()
            delay = int(1000 / self.speed)
            self.gui.root.after(delay, self.run_simulation)

    def start(self):
        if not self.running:
            self.running = True
            self.run_simulation()

    def stop(self):
        self.running = False

    def reset(self):
        self.stop()
        self.grid = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.history = []
        self.generation = 0
        self.gui.update_label("generation_label", f"Generation: {self.generation}")
        self.draw_grid()

    def set_speed(self, speed):
        self.speed = speed

    def back_generation(self):
        if self.history:
            self.generation -= 1
            if self.generation < 0:
                self.generation = 0
            self.grid = self.history[self.generation]
            self.gui.update_label("generation_label", f"Generation: {self.generation}")
            self.draw_grid()

    def forward_generation(self):
        if self.history:
            if self.generation+1 >= len(self.history):
                self.next_generation()
            else:
                self.generation += 1
                self.grid = self.history[self.generation-1]
            self.gui.update_label("generation_label", f"Generation: {self.generation}")
            self.draw_grid()
