# listing 3.8
# Building an asyncio echo server
# using asyncio now instead of low-level sockets and selectors for an event notification system

import asyncio
import logging
import socket
from asyncio import AbstractEventLoop


async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    # handling errors in asyncio echo server with asyncio tasks
    # two ways of doing it:
    # 1. you know where the error or exception will be raised - handle with "try, except, finally" block
    # this works if the tasks is not referenced anywhere in the code (hence garbage-collected)
    # 2. you don't know (and not garbage-collected) - await the asyncio created task to retrieve error
    try:
        while data := await loop.sock_recv(connection, 1024):
            print(f"New data, from {connection.getpeername()}: {data}")
            if data == b"boom\r\n":
                raise Exception("Unexpected network error")
            await loop.sock_sendall(connection, data)
    # catch exception
    except Exception as ex:
        logging.exception(ex)
    finally:
        # after handling exception, close the client connection
        connection.close()


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
# here, we also handled the error/exception that occured within a created task
