import http.server
import socketserver
import webbrowser
import threading
import os

PORT = 8000

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve the HTML content as a response to a GET request
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sample HTML Page</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f0f0f0; }
                h1 { color: #333333; }
                p { font-size: 14px; }
                a { color: #1a0dab; }
            </style>
        </head>
        <body>
            <h1>Welcome to the HTML Viewer</h1>
            <p>This is a sample HTML content displayed in a Python-based local server.</p>
            <p>Visit <a href="https://www.python.org">Python's official website</a> for more information.</p>
        </body>
        </html>
        """
        # Send HTML content as response
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

def open_browser():
    # Open the web browser to the local server
    webbrowser.open(f'http://localhost:{PORT}')

def start_server():
    # Start the server in a new thread
    handler = MyHttpRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    # Open the browser after the server starts
    open_browser()

    # Keep the main thread alive
    input("Press Enter to stop the server...\n")
