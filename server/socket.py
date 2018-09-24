import websockets
import socket

from rx.subjects import Subject


port = 8765
host = socket.gethostbyname(socket.gethostname())
connections = Subject()


async def on_connection(connection, path):
    """ Pushes new connections into the connections subject """
    connections.on_next(connection)


def server():
    """ Returns a co-routine that will listen for new socket connections """
    print('Listening for connections at ws://{host}:{port}')
    return websockets.serve(on_connection, '0.0.0.0', port)
