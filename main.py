from httpserver import HttpServer

if __name__ == "__main__":
    server = HttpServer("127.0.0.1", 8080)
    server.start()
