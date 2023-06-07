import socket, asyncio
from random import choice
from datetime import datetime

class Async_server():
    def __init__(self, host = 'localhost', port = 9090):
        self.host = host
        self.port = port
        self.users = {}
        self.status = {}

    def __del__(self):
        print("Server close")
        for addr, user_writer in self.users.items():
            user_writer.close()

    async def all_send(self, data):
        for addr, user_writer in self.users.items():
            user_writer.write(data)
            await user_writer.drain()

    async def message_handler(self, _message, writer):
        print(_message)
        message = _message.split(' ') # [state] [name] text
        name = message[1]
        quit = False
        match message[0]:
            case '[CON]': # [state] [name]
                if self.users.get(name) is not None:
                    text = "{} Имя {} занято. Смените имя".format('[ERR]', message[1])
                    writer.write(text.encode('utf-8'))
                    await writer.drain()
                    return True
                else:
                    self.users[name] = writer
                    text = "{} зашел в чат!".format(message[1])

            case '[MES]': # [state] [name] text
                text = "{}: {}".format(name, ' '.join(message[2:]))

            case '[COM]': # [state] [name] command
                if message[2] == '/card':
                    card = choice(['Пики', 'Трефы', 'Червы', 'Бубны'])
                    text = "{}: вам выпали - {}".format(name, card)
                elif message[2] == '/status' and len(message) >= 4:
                    self.status[name] = message[3]
                    text = "Вам установлен статус - {}".format(self.status[name])
                else:
                    text = '[ANS]'+ ' ' +'Нераспознанная команда'
                    writer.write(text.encode('utf-8'))
                    await writer.drain()
                    return False

            case '[DIS]': # [state] [name]
                print(f'{name} - вышел из чата')
                if self.status.get(name) is not None:
                    self.status.pop(name)
                self.users.pop(name).close()
                text = "{} вышел из чата :(".format(name)
                quit = True

        current_datetime = datetime.now()
        if self.status.get(name) is not None:
            await self.all_send(('[ANS]'+ ' ' + self.status.get(name) + ' ' + text + '   ({}:{}:{})'.format(current_datetime.hour, current_datetime.minute, current_datetime.second)).encode('utf-8'))
        else:
            await self.all_send(('[ANS]'+ ' ' + text + '   ({}:{}:{})'.format(current_datetime.hour, current_datetime.minute, current_datetime.second)).encode('utf-8'))
        return quit

    async def speak_with_client(self, reader, writer):
        addr = writer.get_extra_info('peername')[1]
        print('connect: ', addr)
        quit = False
        while not quit:
            try:
                data = await reader.read(100)
                if not data:
                    break
                quit = await self.message_handler(data.decode('utf-8'), writer)
                #print(f"Received {message!r} from {addr!r}")
            except Exception as e:
                print('Err:', e)
                break
        print("Close the connection")

    async def main(self):
        server = await asyncio.start_server(
            self.speak_with_client, self.host, self.port)

        addr = server.sockets[0].getsockname()
        print(f'I start serving on {addr}')

        async with server:
            await server.serve_forever()

    def run_server(self):
        asyncio.run(self.main())
