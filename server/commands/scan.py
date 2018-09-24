from server.messages import message
from server.events import events, of_type


async def scan(event):
    connection = event.connection
    await connection.send(message('scan_progress', {'percent': 10}))
    await connection.send(message('scan_progress', {'percent': 30}))
    await connection.send(message('scan_progress', {'percent': 80}))
    await connection.send(message('scan_progress', {'percent': 90}))
    await connection.send(message('scan_progress', {'percent': 95}))
    await connection.send(message('scan_progress', {'percent': 100}))
    await connection.send(message('scan_complete', {'filename': '/scans/123611232334.png'}))


events.filter(of_type('scan'))\
    .subscribe(scan)


