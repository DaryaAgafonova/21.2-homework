from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def serve_file(self, filename, content_type='text/html'):
        try:
            with open(os.path.join('templates', filename), 'r', encoding='utf-8') as file:
                content = file.read()
            self.send_response(200)
            self.send_header('Content-type', f'{content_type}; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.serve_404()

    def serve_static(self, filename):
        try:
            with open(os.path.join('static', filename), 'rb') as file:
                content = file.read()
            self.send_response(200)
            if filename.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            else:
                self.send_header('Content-type', 'application/octet-stream')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.serve_404()

    def serve_404(self):
        self.send_error(404, "File not found")
        try:
            with open(os.path.join('templates', '404.html'), 'r', encoding='utf-8') as file:
                content = file.read()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.wfile.write(b"404 - Page not found")

    def do_GET(self):
        from urllib.parse import urlparse, parse_qs
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        if path == '/' or path == '/index' or path == '/index.html':
            self.serve_file('index.html')
        elif path == '/catalog' or path == '/catalog.html':
            self.serve_file('catalog.html')
        elif path == '/category' or path == '/category.html':
            self.serve_file('category.html')
        elif path == '/contacts' or path == '/contacts.html':
            if query:
                print("Received GET data for contacts:")
                print(json.dumps(query, indent=2))
            self.serve_file('contacts.html')
        elif path.startswith('/static/'):
            self.serve_static(path[8:])  
        else:
            self.serve_404()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print("Received POST data:")
        print(post_data.decode('utf-8'))
        
        try:
            json_data = json.loads(post_data.decode('utf-8'))
            print("Parsed JSON data:")
            print(json.dumps(json_data, indent=2))
        except json.JSONDecodeError:
            print("Received data is not valid JSON")
    
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps({"status": "success", "message": "Data received"})
        self.wfile.write(response.encode('utf-8'))

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

