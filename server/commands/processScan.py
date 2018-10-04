from server.messages import message
from server.events import events, of_type, via_asyncio
from server.commands.ris_processing import image_process_interface
import numpy
import datetime
import base64

async def processScan(event):
    connection = event.connection
    print('Running scan')
    #get current time to save scan
    time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    ris_processing.image_process_interface.process_image(connection.send, 'C:/PNG Dumps/Processing/'+time, 'Final Thermal Hotspot', 0, -1)
    await connection.send(message('scan_progress', {'percent': 100}))
    await connection.send(message('scan_complete', {'base64EncodedString': scan.decode('utf-8')}))
    print('Scan complete')


events.filter(of_type('processScan')) \
    .subscribe(via_asyncio(processScan))


