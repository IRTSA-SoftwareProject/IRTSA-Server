import asyncio

from server.socket import server

# Wait for connections forever
try:
    asyncio.get_event_loop().run_until_complete(server())
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    print('Server stopped')
