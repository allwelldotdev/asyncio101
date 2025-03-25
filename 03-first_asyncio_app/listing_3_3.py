# listing 3.3
# Allowing multiple clients to connect to socket server

import socket

server_socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
)  # create TCP socket server
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ("127.0.0.1", 8990)  # set the address of the socket to 127.0.0.1:8990
server_socket.bind(server_address)
server_socket.listen()  # listen for connections

connections = []

try:
    while True:
        connection, client_address = (
            server_socket.accept()  # .accept is blocking
        )  # wait for a connection and assign the client an address
        print(f"I got a connection from {client_address}!")

        # print(f"0: {connection}") # debug

        connections.append(connection)

        # print(connections) # debug

        for connection in connections:
            # print(f"1: {connection}") # debug

            buffer = (
                b""  # initializes an empty bytes object 'buffer' to store incoming data
            )

            while buffer[-2:] != b"\r\n":
                # print(f"2: {connection}") # debug

                data = connection.recv(
                    2
                )  # .recv is blocking, either returns bytes or an empty buffer b"" when client closes connection

                # print(f"3: {connection}") # debug

                if not data:  # if b"" is returned by data, break
                    break
                else:
                    print(
                        f"I got data: {data}!"
                    )  # prints out byte-sized data until complete
                    buffer = buffer + data

            print(f"All the data is: {buffer}")
            connection.sendall(buffer)

            # print(f"4: {connection}") # debug

finally:
    server_socket.close()

# notice the problem here?
# PS: I added some print statements `print(f"[0..4] {connection}")` for easier debugging, you can uncomment them if you like

# The problem:
# When we try connecting to this server with multiple clients and send data, they won't all receive data at the same time
# they send because some socket methods .accept and .recv are blocking, and will pause the server program until the
# first connector sends another message. This causes the other clients to be stuck waiting on the next iteration of the loop,
# which won't happen until the first client sends data to the server.
