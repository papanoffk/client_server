import socket, time, Async_server

if __name__ == '__main__':
    host = socket.gethostbyname(socket.gethostname())
    port = 9090

    server = Async_server.Async_server(host, port)
    server.run_server()
