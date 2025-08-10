import socket
import datetime
import os
import mimetypes
from logging import log

class HttpServer():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # fixed args
        server.bind((self.host, self.port))
        print("Server is Starting...")
        print(f"Server is listening on {self.host}:{self.port}")
        while True:
            server.listen(5)
            conn, addr = server.accept()
            data = conn.recv(1024 * 4).decode()
            response = self.handle_request(data)  # added self
            conn.sendall(response)

    def handle_request(self, data):
        request = RequestParser(data)
        if request.method == "GET":
            response = HttpResponse().handle_GET(request.uri)
            return response


class HttpResponse():
    BASE_DIR = "http"
    blank_line = "\r\n"
    status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'Not Implemented',
    }
    
    response_headers = {
        "Server": "PortfolioServer"
    }
    
    def response_line(self, status_code):
        reason = self.status_codes[status_code]  # added self
        line = f"HTTP/1.1 {status_code} {reason}\r\n"
        return line
    
    def response_header(self):
        header = ""
        for i in self.response_headers:
            header += "%s: %s\r\n" % (i, self.response_headers[i])  # added self
        return header
        
    def handle_GET(self, uri):
        if uri == "/":
            uri = "/index.html"
        path = self.BASE_DIR + uri  # added self
        if os.path.exists(path) and not os.path.isdir(path):
            response_line = self.response_line(200)
            header = self.response_header()
            content_type = f"Content-Type: {mimetypes.guess_type(path)[0]}\r\n"
            header += content_type

            
            with open(path, "rb") as f:  # fixed wrong string literal
                response_body = f.read()
            content_length = f"Content-Length: {len(response_body)}\r\n"
            header += content_length
            response = (response_line + header + self.blank_line).encode() + response_body
            return response
        else:
            response_line = self.response_line(404)
            return (response_line + self.blank_line).encode() + b"<h1>404 Not Found</h1>"


class RequestParser():
    def __init__(self, data):
        self.method = None
        self.uri = None
        self.parse(data)
    
    def parse(self, data):  # added self
        lines = data.split("\r\n")
        request_line = lines[0]
        words = request_line.split(" ")
        if len(words) >= 2:
            self.method = words[0]
            self.uri = words[1]