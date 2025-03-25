# listing 3.6
# First attempt at a non-blocking server: update: .accept and .recv through a
# BlockingIOError when they execute in nonblocking fashion and don't
# receive incoming data

# Solution?
# Handling the exceptions.

import socket

server_socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
)  # create TCP socket server
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ("127.0.0.1", 8990)  # set the address of the socket to 127.0.0.1:8990
server_socket.bind(server_address)
server_socket.listen()  # listen for connections

server_socket.setblocking(False)  # set server socket to nonblocking

connections = []

try:
    while True:
        try:
            connection, client_address = (
                server_socket.accept()  # .accept is blocking
            )  # wait for a connection and assign the client an address

            connection.setblocking(False)  # set client socket to nonblocking

            print(f"I got a connection from {client_address}!")

            # print(f"0: {connection}")  # debug

            connections.append(connection)
        except BlockingIOError:
            pass

        # print(connections) # debug

        for connection in connections:
            # print(f"1: {connection}")  # debug

            try:
                buffer = b""  # initializes an empty bytes object 'buffer' to store incoming data

                while buffer[-2:] != b"\r\n":
                    # print(f"2: {connection}")  # debug

                    data = connection.recv(
                        2
                    )  # .recv is blocking, either returns bytes or an empty buffer b"" when client closes connection

                    # print(f"3: {connection}")  # debug

                    if not data:  # if b"" is returned by data, break
                        break
                    else:
                        print(
                            f"I got data: {data}!"
                        )  # prints out byte-sized data until complete
                        buffer = buffer + data

                print(f"All the data is: {buffer}")
                connection.sendall(buffer)

                # print(f"4: {connection}")  # debug
            except BlockingIOError:
                pass

finally:
    server_socket.close()

# this works!
# our socket server is finally concurrent!
# but because we're constantly (in a loop) handling the exception and looping infinitely
# it's damaging for CPU
