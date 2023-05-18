# python3
import socket, asyncio

class Client():
    def __init__(self, name = 'user'):
        host = socket.gethostbyname(socket.gethostname())
        port = 9090
        self.name = f'[{name}]'
        self.server = (host, port)
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect(self.server)
        self.new_message('connect', self.name)

    def __del__(self):
        self.new_message('disconnect', self.name)
        self.client_sock.close()
        print('Connection is clossed')

    def listen(self)->str:
        data = self.client_sock.recv(1024).decode('utf-8')
        return data

    def new_message(self, state, text):
        event_massage = {'connect' : '[CONN] ',
                 'disconnect' : '[DIS] ' ,
                 'message' : '[MASS] '
        }

        _text = event_massage[state] + self.name + ' ' + text
        self.client_sock.sendall(bytes(_text, "utf8"))

if __name__ == '__main__':
    app = Client()
    app.new_message(input())
