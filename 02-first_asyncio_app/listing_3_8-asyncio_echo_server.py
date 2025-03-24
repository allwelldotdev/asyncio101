# listing 3.8
# Building an asyncio echo server
# using asyncio now instead of low-level sockets and selectors for an event notification system

import asyncio
import socket
from asyncio import AbstractEventLoop


async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    while data := await loop.sock_recv(connection, 1024):
        print(f"New data, from {connection.getpeername()}: {data}")
        await loop.sock_sendall(connection, data)


async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop) -> None:
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Got a connection: {address}")
        asyncio.create_task(echo(connection, loop))


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ("127.0.0.1", 8990)
    # always remember to set the server and client socket to non-blocking
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    await listen_for_connection(server_socket, asyncio.get_running_loop())


if __name__ == "__main__":
    asyncio.run(main())

# this echo server works just like the one built with low-level sockets and selectors
# but with asyncio APIs.
