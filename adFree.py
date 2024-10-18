import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    try:
        # Get the HTML content from the URL
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching the page: {e}"

def remove_ads(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all elements with id or class containing 'ad'
    for tag in soup.find_all(True):  # True means any tag
        if tag.get('id') and 'ad' in tag.get('id').lower():
            tag.decompose()  # Remove the tag completely
        elif tag.get('class'):
            # Check if any class contains 'ad'
            if any('ad' in class_name.lower() for class_name in tag.get('class')):
                tag.decompose()

    return soup.prettify()

def load_page():
    url = url_entry.get()
    if not url.startswith("http"):
        url = "http://" + url

    html_content = fetch_page(url)
    if html_content:
        clean_html = remove_ads(html_content)
        # Display the cleaned HTML in the text area
        browser_text.delete(1.0, tk.END)
        browser_text.insert(tk.END, clean_html)

# Setting up the GUI
root = tk.Tk()
root.title("Custom Browser")

# URL Entry
url_label = ttk.Label(root, text="Enter URL:")
url_label.pack(pady=5)

url_entry = ttk.Entry(root, width=50)
url_entry.pack(pady=5)

# Load Button
load_button = ttk.Button(root, text="Load Page", command=load_page)
load_button.pack(pady=5)

# Display area for HTML content
browser_text = ScrolledText(root, wrap=tk.WORD, height=30, width=100)
browser_text.pack(pady=10)

# Start the Tkinter loop
root.mainloop()
