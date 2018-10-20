"""An example command that listens to the "scan" message from the client and pretends to do some
processing. For the actual scan message, have a look at the processScan module.
"""

from server.messages import message
from server.events import events, of_type, via_asyncio


async def scan(event):
    connection = event.connection
    print('Running scan')
    await connection.send(message('scan_progress', {'percent': 10}))
    await connection.send(message('scan_progress', {'percent': 30}))
    await connection.send(message('scan_progress', {'percent': 80}))
    await connection.send(message('scan_progress', {'percent': 90}))
    await connection.send(message('scan_progress', {'percent': 95}))
    await connection.send(message('scan_progress', {'percent': 100}))
    await connection.send(message('scan_complete', {'filename': '/scans/123611232334.png'}))
    print('Scan complete')


events.filter(of_type('scan')) \
    .subscribe(via_asyncio(scan))


