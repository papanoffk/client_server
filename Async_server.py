import socket, time, asyncio

class Async_server():
    def __init__(self, host = 'localhost', port = 9090):
        self.host = host
        self.port = port
        self.users = {}

    async def all_send(self, writer, data):
        for addr, user_writer in self.users.items():
            user_writer.write(data)
            await user_writer.drain()


    #async def message_handler(self, _message):
        #message = _messsage.split(' ')



    async def speak_with_client(self, reader, writer):
        addr = writer.get_extra_info('peername')[1]
        self.users[addr] = writer
        while True:
            try:
                data = await reader.read(100)
                if not data:
                    break
                message = data.decode()

                print(f"Received {message!r} from {addr!r}")

                print(f"Send: {message!r}")
                await self.all_send(writer, data)
            except Exception as e:
                print('Err:', e)
                break

        self.users.pop(addr).close()
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
