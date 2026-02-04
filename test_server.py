"""
Simple HTTP server for testing PDF downloads.
Serves test PDFs from the test_pdfs directory.
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys


class PDFServerHandler(SimpleHTTPRequestHandler):
    """Custom handler to serve PDFs."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="test_pdfs", **kwargs)


if __name__ == '__main__':
    port = 8000
    
    # Check if test_pdfs directory exists
    if not os.path.exists('test_pdfs'):
        print("Error: test_pdfs directory not found.")
        print("Run test_parser.py first to create test PDFs.")
        sys.exit(1)
    
    print(f"Starting test PDF server on port {port}...")
    print(f"Access PDFs at: http://localhost:{port}/")
    print("\nPress Ctrl+C to stop the server.")
    
    server = HTTPServer(('localhost', port), PDFServerHandler)
    server.serve_forever()
