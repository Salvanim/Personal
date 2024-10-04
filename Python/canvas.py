import tkinter as tk
from tkinter import ttk
import copy
from bs4 import BeautifulSoup
import webbrowser
from PIL import Image, ImageTk  # Ensure Pillow is installed

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

    def add_link(self, name, text, x, y, url):
        """Add a clickable link (Label) to the GUI."""
        link = tk.Label(self.root, text=text, fg="blue", cursor="hand2", font=("Arial", 12, "underline"))
        link.place(x=x, y=y)
        link.bind("<Button-1>", lambda e: webbrowser.open(url))  # Open the URL in the default browser
        self.widgets[name] = link
        return link

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
            if self.generation + 1 >= len(self.history):
                self.next_generation()
            else:
                self.generation += 1
                self.grid = self.history[self.generation - 1]
            self.gui.update_label("generation_label", f"Generation: {self.generation}")
            self.draw_grid()

class HTMLToGUI:
    def __init__(self, gui, html_content, canvas_id=None):
        self.gui = gui
        self.html_content = html_content
        self.canvas_id = canvas_id
        self.entries = {}  # To store entry widgets by name
        self.html_to_widgets()

    def html_to_widgets(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')

        current_y = 10

        for element in soup.find_all(True):
            tag = element.name
            if tag == 'h1':
                self._add_label(element.text, current_y, font=("Arial", 20))
                current_y += 30
            elif tag == 'h2':
                self._add_label(element.text, current_y, font=("Arial", 18))
                current_y += 25
            elif tag == 'p':
                self._add_label(element.text, current_y, font=("Arial", 12))
                current_y += 20
            elif tag == 'a':
                self._add_link(element.text, current_y, element.get('href'))
                current_y += 40
            elif tag == 'form':
                for input_tag in element.find_all('input'):
                    input_type = input_tag.get('type')
                    input_name = input_tag.get('name', f"input_{current_y}")
                    if input_type == 'text':
                        self._add_entry(input_name, current_y)
                        current_y += 40
                    elif input_type == 'submit':
                        self._add_button(input_tag.get('value'), current_y, action=lambda: self.submit_form())
                        current_y += 40
            elif tag == 'div':
                pass  # Extend functionality as needed

    def _add_label(self, text, y_position, font=("Arial", 12)):
        self.gui.add_label(f"label_{y_position}", text, 10, y_position, font=font)

    def _add_button(self, text, y_position, link=None, action=None):
        if action:
            button_action = action
        elif link:
            def button_action():
                webbrowser.open(link)
        else:
            def button_action():
                print(f"Button '{text}' clicked.")
        self.gui.add_button(f"button_{y_position}", text, 10, y_position, command=button_action)

    def _add_entry(self, name, y_position):
        entry = self.gui.add_entry(name, 10, y_position)
        self.entries[name] = entry

    def _add_canvas(self, y_position, width=500, height=500):
        if self.canvas_id:
            self.gui.add_canvas(self.canvas_id, 10, y_position, width, height)

    def _add_link(self, text, y_position, url):
        self.gui.add_link(f"link_{y_position}", text, 10, y_position, url)

    def add_image(self, name, img_path, x, y):
        img = Image.open(img_path)
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(self.gui.root, image=photo)
        label.photo = photo
        label.place(x=x, y=y)
        self.gui.widgets[name] = label
        return label

    def submit_form(self):
        # Example form submission handler
        username_entry = self.entries.get('username')  # Adjust based on entry names
        if username_entry:
            username = username_entry.get()
            print(f"Submitted username: {username}")
            self.gui.update_label("submission_label", f"Hello, {username}!")
        else:
            print("Username entry not found.")

# --- Sample HTML Content ---
html_content = """
<html>
<head>
    <title>Test HTML to GUI</title>
</head>
<body>
    <h1>Welcome to the GUI Conversion</h1>
    <p>This is a paragraph in the HTML document.</p>
    <a href="https://www.example.com">Click Here to Visit Example</a>
    <form>
        <input type="text" name="username" placeholder="Enter your name">
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

# --- Initialize GUI ---
gui = GUI()

# Add a label to display form submission result
gui.add_label("submission_label", "", 10, 200, font=("Arial", 12), color="green")

# Convert HTML to GUI widgets
html_to_gui = HTMLToGUI(gui, html_content)

# Example: Adding Game of Life (Optional)
# gui.add_label("generation_label", "Generation: 0", 10, 250)
# game = GameOfLife(gui, "canvas1")
# gui.add_button("start_button", "Start", 10, 280, command=game.start)
# gui.add_button("stop_button", "Stop", 100, 280, command=game.stop)
# gui.add_button("reset_button", "Reset", 190, 280, command=game.reset)
# gui.add_canvas("canvas1", 10, 310, width=500, height=500)

# --- Run the GUI ---
gui.run()
