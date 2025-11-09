#!/usr/bin/env python3
"""
Simple HTTP server to serve the customer dashboard HTML file
"""
import http.server
import socketserver
import os

# Change to the directory containing the HTML file
os.chdir('/home/jerrold/ussd-server')

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"🌐 Serving customer dashboard at http://localhost:{PORT}/customer-dashboard.html")
    print("📊 Appwrite endpoint: http://localhost/v1")
    print("🛑 Press Ctrl+C to stop the server")
    httpd.serve_forever()