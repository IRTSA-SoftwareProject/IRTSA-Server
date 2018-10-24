''' Created on 23 Sep. 2018, last editied 23 Oct. 2018
Command that runs processing on the folder sent by the app
@author: Caspar Pikaar, edited by James Moran [jpmoran.pac@gmail.com]
'''

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
    # The event object contains two parameters: .connection and .message;
    #  .connection contains a .send function that accepts a message, while
    #  .message is a dictionary containing the parameters sent from the app side.
    await image_process_interface.process_image(connection,
                                                path_to_save = '/var/www/html/irscans/' +time, # The save path is hard-coded
                                                simulation_select = event.message['pngPath'],
                                                process_select = event.message['processingTechnique'],
                                                frames_to_process = event.message['framesToProcess']-event.message['frameStart'],
                                                frame_start = event.message['frameStart'])
    print('Scan complete')


events.filter(of_type('processScan')) \
    .subscribe(via_asyncio(processScan))


