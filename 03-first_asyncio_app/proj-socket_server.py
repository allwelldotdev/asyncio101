# built a concurrent (non-blocking) socket server
# turning it into some kind of "AI chat interface mimic"
# let's go! 🚀


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


def msg_send(action: str = None, name: str | None = None) -> str:
    match action:
        case "greet":
            return "::: Hi! I'm just code but let's pretend I'm AI. What's your name?\r\n".encode()
        case "name":
            return f"::: Nice to meet you, {name}!\r\n".encode()
        case "color":
            return "::: Yeah so, what's your favourite color?\r\n".encode()
        case "color_response":
            return f"::: Cool! I like {name} too!\r\n".encode()
        case _:
            return f"::: Okay, {name}, it's been fun. Gotta go now though. See ya later. Be good ;)\r\n".encode()


client_db = {}


print("Waiting for connection...")

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

            if data == b"q\r\n":
                print(f"client quit :from: {event_socket.getpeername()}\r\n", end="")
                event_socket.close()
                selector.unregister(event_socket)
                continue

            print(
                f"New data: {data.decode()} :from: {event_socket.getpeername()}\r\n",
                end="",
            )

            data = data.decode()

            search_data = " ".join(data.lower().split())
            split_data = data.lower().split()

            if "hello" in search_data or "hi" in search_data:
                event_socket.send(msg_send("greet"))

            elif "name" in search_data:
                client_name = split_data[-1]

                client_name_dict = {"name": client_name.title()}
                client_db.get(
                    event_socket,
                    client_db.setdefault(event_socket, client_name_dict),
                )
                client_name = client_db[event_socket].get("name")

                event_socket.send(msg_send("name", client_name))

            elif "too" in search_data or "same" in search_data or "yeah" in search_data:
                event_socket.send(msg_send("color"))

            elif " " != search_data and search_data in [
                "blue",
                "red",
                "purple",
                "white",
                "black",
                "yellow",
                "pink",
                "orange",
                "green",
                "brown",
                "violet",
                "indigo",
            ]:
                client_color = search_data

                # client_color_dict = {"color": client_color}
                client_db[event_socket].get(
                    "color",
                    client_db[event_socket].setdefault("color", client_color),
                )
                client_color = client_db[event_socket].get("color")

                event_socket.send(msg_send("color_response", client_color))

            else:
                event_socket.send(msg_send(name=client_db[event_socket].get("name")))
