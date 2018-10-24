"""The implementation of the socket. New connections will be passed to the await_events function
in the events module.
"""

import websockets
import socket

from .events import await_events


port = 8765
host = socket.gethostbyname(socket.gethostname())


async def on_connection(connection, path):
    """ Pushes new connections into the connections subject """
    await await_events(connection)


def server():
    """ Returns a co-routine that will listen for new socket connections """
    print(f'Listening for connections at ws://{host}:{port}')
    return websockets.serve(on_connection, '0.0.0.0', port)
