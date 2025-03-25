# listing 3.1
# Starting a socket server and listening for a connection

import socket

server_socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
)  # create TCP socket server
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ("127.0.0.1", 8990)  # set the address of the socket to 127.0.0.1:8990
server_socket.bind(server_address)
server_socket.listen()  # listen for connections

connection, client_address = (
    server_socket.accept()
)  # wait for a connection and assign the client an address
print(f"I got a connection from {client_address}!")

# after running this code, go to another terminal and type:
# telnet localhost 8990
