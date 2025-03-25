# listing 3.2
# Reading and writing data from and to the socket

import socket

server_socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
)  # create TCP socket server
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ("127.0.0.1", 8990)  # set the address of the socket to 127.0.0.1:8990
server_socket.bind(server_address)
server_socket.listen()  # listen for connections

try:
    connection, client_address = (
        server_socket.accept()
    )  # wait for a connection and assign the client an address
    print(f"I got a connection from {client_address}!")

    buffer = b""  # initializes an empty bytes object 'buffer' to store incoming data

    while buffer[-2:] != b"\r\n":
        data = connection.recv(
            2
        )  # .recv is blocking, either returns bytes or an empty buffer b"" when client closes connection
        if not data:  # if b"" is returned by data, break
            break
        else:
            print(f"I got data: {data}!")  # prints out byte-sized data until complete
            buffer = buffer + data

    print(f"All the data is: {buffer}")
    connection.sendall(buffer)

finally:
    server_socket.close()

# we just built a basic echo server with sockets!
