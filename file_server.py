from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import socket
from datetime import datetime
import json


def skip():
    os.system('echo.' if os.name == 'nt' else 'echo.')

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "Unable to detect IP"

class FileReceiverHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        """Handle incoming file uploads"""
        if self.path == '/upload':
            try:
                
                content_length = int(self.headers['Content-Length'])
                
                
                file_data = self.rfile.read(content_length)
                
                
                content_type = self.headers.get('Content-Type', '')
                
                
                extension_map = {
                    'image/jpeg': '.jpg',
                    'image/jpg': '.jpg',
                    'video/mp4': '.mp4',
                    'video/quicktime': '.mov',    
                    'video/x-m4v': '.mp4',        
                    'audio/mpeg': '.mp3',
                    'audio/mp3': '.mp3',
                    'audio/wav': '.wav',
                    'audio/x-wav': '.wav',        
                    'audio/wave': '.wav',         
                    'application/pdf': '.pdf'
                }
                
                
                extension = extension_map.get(content_type, '.bin')
                
                
                if not os.path.exists('received_files'):
                    os.makedirs('received_files')
                
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"received_files/file_{timestamp}{extension}"
                
                
                with open(filename, 'wb') as f:
                    f.write(file_data)
                
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"File saved as {filename}".encode())
                
                print(f"✓ File received and saved as: {filename} ({len(file_data)} bytes)")
                
            except Exception as e:
                
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"Error: {str(e)}".encode())
                print(f"✗ Error receiving file: {e}")
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        """Handle browser requests"""
        if self.path == '/':
            local_ip = get_local_ip()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = f"""
            <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        max-width: 600px;
                        margin: 50px auto;
                        padding: 20px;
                        background: #f5f5f5;
                    }}
                    .card {{
                        background: white;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    h1 {{ color: #333; }}
                    .ip-box {{
                        background: #e8f5e9;
                        padding: 15px;
                        border-radius: 5px;
                        margin: 20px 0;
                        font-family: monospace;
                        font-size: 18px;
                        text-align: center;
                        color: #2e7d32;
                    }}
                    a {{
                        display: inline-block;
                        background: #667eea;
                        color: white;
                        padding: 12px 24px;
                        text-decoration: none;
                        border-radius: 5px;
                        margin-top: 10px;
                    }}
                    a:hover {{ background: #764ba2; }}
                    .instruction {{
                        background: #fff3cd;
                        padding: 15px;
                        border-radius: 5px;
                        margin: 15px 0;
                        border-left: 4px solid #ffc107;
                    }}
                    .supported {{
                        background: #f0f0f0;
                        padding: 10px;
                        border-radius: 5px;
                        margin: 10px 0;
                        font-size: 14px;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>File Receiver Server is Running!</h1>
                    
                    <div class="ip-box">
                        Server IP: {local_ip}:8080
                    </div>
                    
                    <div class="instruction">
                        <strong>On your phone:</strong><br>
                        Make sure you're on the same WiFi network, then visit:<br>
                        <code>http://{local_ip}:8080/sender.html</code>
                    </div>
                    
                    <div class="supported">
                        <strong>Supported file types:</strong><br>
                        Images (JPG)<br>
                        Videos (MP4)<br>
                        Audio (MP3, WAV)<br>
                        Documents (PDF)
                    </div>
                    
                    <p>Files will be saved in the 'received_files' folder</p>
                    <a href="/sender.html">Open File Sender App</a>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        elif self.path == '/sender.html':
            
            try:
                if os.path.exists('sender.html'):
                    with open('sender.html', 'rb') as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(content)
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"<h1>sender.html not found</h1><p>Make sure sender.html is in the same folder as the server</p>")
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"Error: {str(e)}".encode())
        elif self.path == '/api/server-ip':
            # API endpoint to get server IP
            local_ip = get_local_ip()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = json.dumps({'ip': local_ip, 'port': 8080})
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, FileReceiverHandler)
    local_ip = get_local_ip()
    
    print("=" * 120)
    print(f"Server started successfully!")
    skip()
    print(f"Server IP: {local_ip}:{port}")
    skip()
    print("=" * 120)
    skip()
    print(f"On your phone, visit:")
    skip()
    print(f"   http://{local_ip}:{port}/sender.html")
    skip()
    print(f"On this computer, visit:")
    skip()
    print(f"   http://localhost:{port}")
    skip()
    print("Supported file types:")
    skip()
    print("   JPG, MP4, MP3, WAV, PDF")
    skip()
    print("Make sure your phone is on the same WiFi network!")
    skip()
    print("Press Ctrl+C to stop the server")
    skip()
    print("=" * 120)
    
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
