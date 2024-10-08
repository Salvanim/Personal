import tkinter as tk
from tkinter import ttk, filedialog
import json
import uuid

# Assuming the GUI class is defined in the same file or imported appropriately

class GUIDesigner:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI Designer")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)

        # Initialize main frames
        self.toolbox_frame = tk.Frame(self.root, width=200, bg="#f0f0f0")
        self.toolbox_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas_frame = tk.Frame(self.root, width=1000, bg="white")
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Initialize design canvas
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", width=980, height=680, bd=2, relief=tk.SUNKEN)
        self.canvas.pack(padx=10, pady=10)

        # Initialize toolbar
        self.toolbar = tk.Frame(self.toolbox_frame, bg="#d0d0d0", height=700)
        self.toolbar.pack(fill=tk.X, pady=10)

        # Add widget buttons to the toolbox
        self.add_toolbox_widgets()

        # Initialize widget storage
        self.design_widgets = {}

        # Variables for dragging
        self.current_drag = None
        self.offset_x = 0
        self.offset_y = 0

        # Bind events for drag and drop
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        # Add menu
        self.add_menu()

    def add_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export GUI", command=self.export_gui)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

    def add_toolbox_widgets(self):
        # Label
        label_btn = tk.Button(self.toolbar, text="Label", width=20, command=lambda: self.start_adding_widget("Label"))
        label_btn.pack(pady=5)

        # Button
        button_btn = tk.Button(self.toolbar, text="Button", width=20, command=lambda: self.start_adding_widget("Button"))
        button_btn.pack(pady=5)

        # Entry
        entry_btn = tk.Button(self.toolbar, text="Entry", width=20, command=lambda: self.start_adding_widget("Entry"))
        entry_btn.pack(pady=5)

        # Text
        text_btn = tk.Button(self.toolbar, text="Text", width=20, command=lambda: self.start_adding_widget("Text"))
        text_btn.pack(pady=5)

        # Checkbutton
        checkbox_btn = tk.Button(self.toolbar, text="Checkbutton", width=20, command=lambda: self.start_adding_widget("Checkbutton"))
        checkbox_btn.pack(pady=5)

        # Radiobutton
        radiobutton_btn = tk.Button(self.toolbar, text="Radiobutton", width=20, command=lambda: self.start_adding_widget("Radiobutton"))
        radiobutton_btn.pack(pady=5)

        # Dropdown
        dropdown_btn = tk.Button(self.toolbar, text="Dropdown", width=20, command=lambda: self.start_adding_widget("Dropdown"))
        dropdown_btn.pack(pady=5)

        # Canvas
        canvas_btn = tk.Button(self.toolbar, text="Canvas", width=20, command=lambda: self.start_adding_widget("Canvas"))
        canvas_btn.pack(pady=5)

    def start_adding_widget(self, widget_type):
        # Removed the alert to prompt user to click on the canvas
        self.current_widget_type = widget_type

    def on_canvas_click(self, event):
        if hasattr(self, 'current_widget_type'):
            self.add_widget_to_canvas(event.x, event.y, self.current_widget_type)
            del self.current_widget_type
        else:
            # Check if a widget is clicked for moving
            widget = self.get_widget_at_position(event.x, event.y)
            if widget:
                self.current_drag = widget
                widget_props = self.design_widgets[widget]
                self.offset_x = event.x - widget_props['x']
                self.offset_y = event.y - widget_props['y']

    def on_canvas_drag(self, event):
        if self.current_drag:
            new_x = event.x - self.offset_x
            new_y = event.y - self.offset_y
            widget_props = self.design_widgets[self.current_drag]
            # Keep widget within canvas bounds
            new_x = max(0, min(new_x, self.canvas.winfo_width() - widget_props['width']))
            new_y = max(0, min(new_y, self.canvas.winfo_height() - widget_props['height']))
            # Update widget position
            self.canvas.coords(self.current_drag, new_x, new_y)
            widget_props['x'] = new_x
            widget_props['y'] = new_y

    def on_canvas_release(self, event):
        self.current_drag = None

    def add_widget_to_canvas(self, x, y, widget_type):
        widget_id = str(uuid.uuid4())
        if widget_type == "Label":
            text = "Label"
            item = self.canvas.create_text(x, y, text=text, anchor=tk.NW, font=("Arial", 12), fill="black")
            self.design_widgets[item] = {
                "type": "Label",
                "text": text,
                "x": x,
                "y": y,
                "font": ("Arial", 12),
                "color": "black",
                "width": 100,
                "height": 20
            }
        elif widget_type == "Button":
            text = "Button"
            item = self.canvas.create_rectangle(x, y, x+100, y+40, fill="lightgray")
            self.canvas.create_text(x+50, y+20, text=text, font=("Arial", 12))
            self.design_widgets[item] = {
                "type": "Button",
                "text": text,
                "x": x,
                "y": y,
                "width": 100,
                "height": 40,
                "font": ("Arial", 12),
                "bg": "lightgray",
                "fg": "black"
            }
        elif widget_type == "Entry":
            item = self.canvas.create_rectangle(x, y, x+200, y+30, fill="white")
            self.design_widgets[item] = {
                "type": "Entry",
                "x": x,
                "y": y,
                "width": 200,
                "height": 30
            }
        elif widget_type == "Text":
            item = self.canvas.create_rectangle(x, y, x+200, y+100, fill="white")
            self.design_widgets[item] = {
                "type": "Text",
                "x": x,
                "y": y,
                "width": 200,
                "height": 100
            }
        elif widget_type == "Checkbutton":
            text = "Check"
            item = self.canvas.create_rectangle(x, y, x+120, y+30, fill="white")
            self.canvas.create_text(x+20, y+15, text=text, anchor=tk.W, font=("Arial", 12))
            self.design_widgets[item] = {
                "type": "Checkbutton",
                "text": text,
                "x": x,
                "y": y,
                "width": 120,
                "height": 30
            }
        elif widget_type == "Radiobutton":
            text = "Option"
            item = self.canvas.create_rectangle(x, y, x+120, y+30, fill="white")
            self.canvas.create_text(x+20, y+15, text=text, anchor=tk.W, font=("Arial", 12))
            self.design_widgets[item] = {
                "type": "Radiobutton",
                "text": text,
                "x": x,
                "y": y,
                "width": 120,
                "height": 30
            }
        elif widget_type == "Dropdown":
            options = ["Option 1", "Option 2", "Option 3"]
            item = self.canvas.create_rectangle(x, y, x+150, y+30, fill="white")
            self.canvas.create_text(x+10, y+15, text="Dropdown", anchor=tk.W, font=("Arial", 12))
            self.design_widgets[item] = {
                "type": "Dropdown",
                "options": options,
                "x": x,
                "y": y,
                "width": 150,
                "height": 30
            }
        elif widget_type == "Canvas":
            item = self.canvas.create_rectangle(x, y, x+200, y+200, fill="white")
            self.design_widgets[item] = {
                "type": "Canvas",
                "x": x,
                "y": y,
                "width": 200,
                "height": 200,
                "bg": "white"
            }
        else:
            # Unknown widget type; do nothing or handle accordingly
            return

        # Bind right-click to remove widget
        self.canvas.tag_bind(item, "<Button-3>", lambda event, itm=item: self.remove_widget(itm))

    def get_widget_at_position(self, x, y):
        items = self.canvas.find_overlapping(x, y, x, y)
        if items:
            # Return the topmost widget
            return items[-1]
        return None

    def remove_widget(self, item):
        # Optional: Remove confirmation dialog if desired
        # if messagebox.askyesno("Remove Widget", "Are you sure you want to remove this widget?"):
        self.canvas.delete(item)
        del self.design_widgets[item]

    def export_gui(self):
        if not self.design_widgets:
            # Optional: Remove or keep the warning
            # messagebox.showwarning("Export GUI", "No widgets to export.")
            return

        export_data = []
        for widget_id, props in self.design_widgets.items():
            export_data.append(props)

        # Ask user where to save the file
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if not file_path:
            return

        # Generate Python code using the GUI class
        code = self.generate_python_code(export_data)

        try:
            with open(file_path, "w") as f:
                f.write(code)
            # Optional: Remove or keep the success message
            # messagebox.showinfo("Export Successful", f"GUI exported successfully to {file_path}")
        except Exception as e:
            # Optional: Remove or keep the error message
            # messagebox.showerror("Export Failed", f"Failed to export GUI: {e}")
            pass

    def generate_python_code(self, widgets):
        code = """import tkinter as tk
from tkinter import ttk
import webbrowser
from PIL import Image, ImageTk

# Assuming the GUI class is defined in the same file or imported appropriately

class GeneratedGUI(GUI):
    def __init__(self):
        super().__init__(title="Generated GUI", width=800, height=600)
        self.create_widgets()

    def create_widgets(self):
"""
        for idx, widget in enumerate(widgets):
            widget_type = widget["type"]
            identifier = f"widget_{idx}"
            x = widget["x"]
            y = widget["y"]

            if widget_type == "Label":
                text = widget.get("text", "Label")
                font = widget.get("font", ("Arial", 12))
                color = widget.get("color", "black")
                code += f'        self.add_label("{identifier}", "{text}", {x}, {y}, font={font}, color="{color}")\n'

            elif widget_type == "Button":
                text = widget.get("text", "Button")
                font = widget.get("font", ("Arial", 12))
                bg = widget.get("bg", "lightgray")
                fg = widget.get("fg", "black")
                code += f'        self.add_button("{identifier}", "{text}", {x}, {y}, command=None, width=10, height=2)\n'

            elif widget_type == "Entry":
                width = widget.get("width", 20)
                code += f'        self.add_entry("{identifier}", {x}, {y}, width={width})\n'

            elif widget_type == "Text":
                width = widget.get("width", 40)
                height = widget.get("height", 10)
                code += f'        self.add_text("{identifier}", {x}, {y}, width={width}, height={height})\n'

            elif widget_type == "Checkbutton":
                text = widget.get("text", "Check")
                code += f'        self.add_checkbox("{identifier}", "{text}", {x}, {y})\n'

            elif widget_type == "Radiobutton":
                text = widget.get("text", "Option")
                code += f'        self.add_radiobutton("{identifier}", "{text}", {x}, {y}, variable=tk.IntVar(), value=1)\n'

            elif widget_type == "Dropdown":
                options = widget.get("options", ["Option 1", "Option 2", "Option 3"])
                code += f'        self.add_dropdown("{identifier}", {options}, {x}, {y})\n'

            elif widget_type == "Canvas":
                width = widget.get("width", 200)
                height = widget.get("height", 200)
                bg = widget.get("bg", "white")
                code += f'        self.add_canvas("{identifier}", {x}, {y}, width={width}, height={height}, bg="{bg}")\n'

            else:
                code += f'        # Unknown widget type: {widget_type}\n'

        code += """
if __name__ == "__main__":
    gui = GeneratedGUI()
    gui.run()
"""
        return code

def main():
    root = tk.Tk()
    app = GUIDesigner(root)
    root.mainloop()

if __name__ == "__main__":
    main()
