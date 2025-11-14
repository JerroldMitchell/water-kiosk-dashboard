#!/usr/bin/env python3
"""
HTTP server to serve the Water Kiosk Customer Dashboard

This dashboard demonstrates how to use the Appwrite Proxy Server pattern.
Instead of connecting directly to Appwrite (which would require the API key),
the dashboard uses a proxy server that handles authentication automatically.

SETUP REQUIREMENTS:
1. Proxy server must be running on port 3000
   - Start with: cd /home/jerrold/cloud_server/proxy_server && ./start_proxy.sh

2. ngrok tunnel must be active for proxy (if using remote access)
   - Start with: ngrok start proxy

3. This dashboard server (optional - you can use any HTTP server)
   - Start with: python3 serve_dashboard.py
   - Then visit: http://localhost:8080/customer-dashboard.html

HOW THE PROXY PATTERN WORKS:
- Dashboard makes HTTP requests to the proxy server
- Proxy server automatically adds X-Appwrite-Key authentication
- Proxy forwards requests to Appwrite
- Appwrite returns data back through proxy
- Dashboard receives data without ever needing the API key

This is perfect for sharing with students - they can access the database
without needing sensitive credentials!
"""

import http.server
import socketserver
import os

# Change to the directory containing the HTML file
os.chdir('/home/jerrold/cloud_server/water-kiosk-dashboard')

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

print("=" * 60)
print("🚀 Water Kiosk Customer Dashboard")
print("=" * 60)
print(f"✅ Serving dashboard at http://localhost:{PORT}/customer-dashboard.html")
print()
print("📋 REQUIREMENTS (must be running):")
print("  1️⃣  Proxy server on port 3000")
print("      cd /home/jerrold/cloud_server/proxy_server && ./start_proxy.sh")
print()
print("  2️⃣  ngrok tunnel (for remote access)")
print("      ngrok start proxy")
print()
print("📡 The dashboard uses the proxy server to access Appwrite")
print("   No API key needed - the proxy handles authentication!")
print()
print("🛑 Press Ctrl+C to stop this server")
print("=" * 60)
print()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()