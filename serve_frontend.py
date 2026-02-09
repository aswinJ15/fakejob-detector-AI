"""
Simple HTTP server to serve the frontend.
Run this to access the web UI at http://localhost:8000
"""

import http.server
import socketserver
import os

os.chdir('frontend')

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("=" * 60)
    print("🌐 Frontend server running at http://localhost:8000")
    print("=" * 60)
    print("📌 Make sure the backend API is running:")
    print("   python backend/app.py")
    print("=" * 60)
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ Server stopped")
