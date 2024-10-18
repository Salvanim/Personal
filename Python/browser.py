import tkinter as tk
from tkinter import ttk
import copy
from bs4 import BeautifulSoup
import webbrowser
from PIL import Image, ImageTk
from tkinterhtml import HTMLLabel

class GUI:
    def __init__(self, title="Custom GUI", width=800, height=600):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)
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

    def add_html(self, identifier, html):
        label = HTMLLabel(self.root, html)
        label.pack()
        return label

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

    def get_widget(self, identifier):
        return self.widgets.get(identifier, None)

    def add_webview(self, identifier, html_content, x, y, width=800, height=600):
        self.root.update_idletasks()  # Ensure the window is updated before placing webview
        window = webview.create_window("Webview", html=html_content, width=width, height=height)

        # pywebview has its own loop, so we start it in a separate thread to keep Tkinter responsive
        import threading
        threading.Thread(target=webview.start, daemon=True).start()

        self.widgets[identifier] = window
        return window

    def update_label(self, identifier, new_text, updateText=True, new_x=0, new_y=0, updateX=False, updateY=False, new_font=("Arial", 12), updateFont=False, new_color="black", updateColor=False):
        widget = self.get_widget(identifier)
        if isinstance(widget, tk.Label):
            if updateText:
                widget.config(text=new_text)
            if updateX:
                widget.config(x=new_x)
            if updateY:
                widget.config(y=new_y)
            if updateFont:
                widget.config(font=new_font)
            if updateColor:
                widget.config(color=new_color)
        else:
            self.add_label(identifier, new_text, new_x, new_y, new_font, new_color)

    def update_button(self, identifier, new_text=None, updateText=False, new_x=0, new_y=0, updateX=False, updateY=False, new_width=10, new_height=2, updateWidth=False, updateHeight=False, new_command=None, updateCommand=False):
        widget = self.get_widget(identifier)
        if isinstance(widget, tk.Button):
            if updateText:
                widget.config(text=new_text)
            if updateCommand:
                widget.config(command=new_command)
            if updateX:
                widget.config(x=new_x)
            if updateY:
                widget.config(y=new_y)
            if updateWidth:
                widget.config(width=new_width)
            if updateHeight:
                widget.config(height=new_height)
        else:
            self.add_button(identifier, new_text, new_x, new_y, new_command, width=new_width, height=new_height)

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

if __name__ == "__main__":
    gui = GUI("HTML GUI Example", 1000, 800)

    # Example HTML/CSS/JavaScript content
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; }
            h1 { color: green; }
            button { padding: 10px 20px; background-color: blue; color: white; border: none; cursor: pointer; }
        </style>
        <script>
            function sayHello() {
                alert("Hello from HTML, CSS, and JavaScript!");
            }
        </script>
    </head>
    <body>
        <h1>Welcome to HTML GUI</h1>
        <p>This is a GUI rendered with HTML, CSS, and JavaScript!</p>
        <button onclick="sayHello()">Click Me</button>
    </body>
    </html>
    """

    # Adding the webview
    gui.add_html(html_content)

    # Run the GUI
    gui.run()
