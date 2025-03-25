# listing 4.1
# An asynchronous context manager to wait for client connection
# instead of using "try, finally" block


import asyncio
import socket
from types import TracebackType
from typing import Optional, Type


class ConnectedSocket:
    def __init__(self, server_socket):
        self._connection = None
        self._server_socket = server_socket

    async def __aenter__(self):
        print("Entering context manager, waiting for connection")
        loop = asyncio.get_running_loop()
        connection, client_address = await loop.sock_accept(self._server_socket)
        # self._connection = connection.setblocking(False) # this is wrong because remembering
        # how non-blocking sockets work, this 'connection' will fail if not handed-off to
        # an event notification service with selectors, event loop, or awaited
        self._connection = connection
        print("Accepted a connection")
        return self._connection

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        print("Exiting context manager")
        self._connection.close()
        print("Closed connection")


async def main():
    loop = asyncio.get_running_loop()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ("127.0.0.1", 8990)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    async with ConnectedSocket(server_socket) as connection:
        data = await loop.sock_recv(connection, 1024)
        print(data)


if __name__ == "__main__":
    asyncio.run(main())
