"""This is the main entrypoint of the server. Start it by running `python -m server`.
It starts the server and adds it to the global event loop which will continue to run until a
KeyboardInterrupt is sent over the command line.
"""

import asyncio

from server.socket import server

# Wait for connections forever
try:
    asyncio.get_event_loop().run_until_complete(server())
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    print('Server stopped')
