from server.messages import message
from server.events import events, of_type, via_asyncio
from server.commands.ris_processing import image_process_interface
import numpy
import datetime
import base64

async def makeGif(event):
    connection = event.connection
    print('Making gif')
    #get current time to save scan
    time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    await image_process_interface.export_gif(connection, '/var/www/html/irscans/' +time, 'Final Thermal Hotspot')
    print('Made gif')


events.filter(of_type('makeGif')) \
    .subscribe(via_asyncio(makeGif))


