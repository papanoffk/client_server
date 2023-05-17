# python3
import socket, asyncio

class Client():
    def __init__(self):
        self.server = ('192.168.1.174', 9090)
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect(self.server)

    def __del__(self):
        self.client_sock.close()
        print('Connection is clossed')

    def listen(self)->str:
        data = self.client_sock.recv(1024).decode('utf-8')
        return data

    def new_message(self, text):
        self.client_sock.sendall(bytes(text, "utf8"))
        #если нечего есть, то кидает ошибку
        #data = self.client_sock.recv(1024)
        #print('Received', repr(data))

if __name__ == '__main__':
    app = Client()
    app.new_message(input())
