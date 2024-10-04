import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget, QInputDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML parsing

class HTMLViewer(QMainWindow):
    def __init__(self, urls):
        super().__init__()
        self.setWindowTitle("HTML Viewer with Tabs")
        self.setGeometry(100, 100, 800, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Tab widget setup
        self.tab_widget = QTabWidget()
        self.tab_widget.setMovable(True)  # Allow tabs to be moved
        self.tab_widget.setTabsClosable(True)  # Allow tabs to be closed
        self.tab_widget.tabCloseRequested.connect(self.close_tab)  # Connect tab close event
        self.tab_widget.currentChanged.connect(self.check_new_tab)  # Detect when "+" is clicked

        layout.addWidget(self.tab_widget)

        # Add initial tabs for given URLs
        for url in urls:
            self.add_tab_from_url(url)

        # Add "+" tab
        self.add_plus_tab()

    def add_tab_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            html_content = response.text

            soup = BeautifulSoup(html_content, 'html.parser')
            page_title = soup.title.string if soup.title else "Untitled"

            browser = QWebEngineView()
            browser.setHtml(html_content)
            self.tab_widget.insertTab(self.tab_widget.count() - 1, browser, page_title)
            self.tab_widget.setCurrentIndex(self.tab_widget.count() - 2)
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            browser = QWebEngineView()
            browser.setHtml(f"<h1>Error fetching page</h1><p>{e}</p>")
            self.tab_widget.insertTab(self.tab_widget.count() - 1, browser, "Error")
            self.tab_widget.setCurrentIndex(self.tab_widget.count() - 2)

    def add_plus_tab(self):
        plus_tab = QWidget()
        self.tab_widget.addTab(plus_tab, "+")

    def check_new_tab(self, index):
        if index == self.tab_widget.count() - 1:
            self.open_new_tab_dialog()

    def open_new_tab_dialog(self):
        # Open a dialog to enter a new URL
        url, ok = QInputDialog.getText(self, "New Tab", "Enter URL:")
        if ok and url:
            self.add_tab_from_url(url)

    def close_tab(self, index):
        # Prevent closing the "+" tab
        if index != self.tab_widget.count() - 1:
            self.tab_widget.removeTab(index)  # Remove the tab at the given index

    def show_viewer(self):
        self.show()

def display_html(urls):
    """
    Function to display HTML content in a GUI window with tabs from URLs.

    :param urls: List of URLs to fetch HTML content from.
    """
    app = QApplication(sys.argv)
    viewer = HTMLViewer(urls)
    viewer.show_viewer()
    sys.exit(app.exec_())

if __name__ == "__main__":
    urls = [
        "https://www.google.com"
    ]
    display_html(urls)
