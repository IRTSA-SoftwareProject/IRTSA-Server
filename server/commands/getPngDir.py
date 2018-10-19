from server.messages import message
from server.events import events, of_type, via_asyncio
from server.commands.ris_processing import image_process_interface
import numpy
import datetime
import base64
import os

async def getPngDir(event):
    connection = event.connection
    print(os.listdir('/home/pi/scans/png/'))
    connection.send(message('simulationList', os.listdir('/home/pi/scans/png/')))


events.filter(of_type('getPngDir')) \
    .subscribe(via_asyncio(getPngDir))


