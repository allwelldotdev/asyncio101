# listing 3.7
# Using selectors to build a non-blocking (concurrent) server

import selectors
import socket
from selectors import SelectorKey
from typing import List, Tuple

# choosing DefaultSelector class for most efficient sys implementation
selector = selectors.DefaultSelector()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ("127.0.0.1", 8990)
server_socket.setblocking(False)  # set server socket to nonblocking
server_socket.bind(server_address)
server_socket.listen()


# register server socket with selector for read events
selector.register(server_socket, selectors.EVENT_READ)


while True:
    # create selector that will timeout after 1 second
    # allowing other code to execute
    events: List[Tuple[SelectorKey, int]] = selector.select(timeout=None)

    # if events == 0, print it out
    # this happens when timeout occurs
    if len(events) == 0:
        print("No events, waiting a bit more!")

    # get the socket for the event
    # stored in fileobj
    for event, _ in events:
        event_socket = event.fileobj

        # if socket event == server_socket it's a connection
        if event_socket == server_socket:
            connection, client_address = server_socket.accept()
            connection.setblocking(False)
            print(f"New connection from: {client_address}!")

            # register client socket with selector for read events
            selector.register(connection, selectors.EVENT_READ)
        # if socket event != server_socket it's data from client
        # echo it back!
        else:
            data = event_socket.recv(1024)
            print(f"New data: {data}")
            event_socket.send(data)


# this works beautifully, without bordering the CPU - true single-threaded concurency
# just build a mini event loop using selectors from Python stdlib for our socket chat server
# and it works!
