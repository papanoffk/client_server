
import socket, time, threading, asyncio

host = socket.gethostbyname(socket.gethostname())
port = 9090
print('My adress: ', host)

'''

#def all_send():

clients = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

print('I wait')
server.listen(2)
print('прослушал')

quit = False
while not quit:
    try:
        print('cycle')
        client, address = server.accept()
        clients[address] = client
        print()
        print('address connected: ', address)
        data, _address = client.recv(1024).decode("utf-8")
        print('data: ', data)

    except Exception as e:
        print("STOP", e)
        quit = True

server.close()
'''

'''import socket, time

host = socket.gethostbyname(socket.gethostname())
port = 9090
print('My adress: ', host)

clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host, port))

print('I wait')

quit = False
while not quit:
    try:
        data, addr = server.recvfrom(1024)

        if addr not in clients:
            clients.append(addr)

        itsattime = time.strftime("%Y - %m - %d - %H.%M.%S.", time.localtime())

        print("[{} - {}] - {}".format(addr[0], addr[1], itsattime))
        print(data.decode('utf-8'))

        for client in clients:
            if addr != client:
                server.sendto(data, client)
    except Exception as e:
        print("STOP", e)
        quit = True

server.close()'''

users = {}

async def all_send(writer, data):
    for addr, user_writer in users.items():
        user_writer.write(data)
        await user_writer.drain()


async def handle_echo(reader, writer):
    addr = writer.get_extra_info('peername')[1]
    users[addr] = writer
    while True:
        try:
            data = await reader.read(100)
            if not data:
                break
            message = data.decode()

            print(f"Received {message!r} from {addr!r}")

            print(f"Send: {message!r}")
            await all_send(writer, data)
        except Exception as e:
            print('Err:', e)
            break

    users.pop(addr).close()
    print("Close the connection")

async def main():
    server = await asyncio.start_server(
        handle_echo, host, port)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
