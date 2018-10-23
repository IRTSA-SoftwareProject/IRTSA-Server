''' Created on 15 Oct. 2018, last editied 23 Oct. 2018
Command that returns the list of subdirectories in a hard-coded folder
@author: James Moran [jpmoran.pac@gmail.com]
'''

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
    
    # Send back the list of directories found, the folder matches the
    #  directory created in pi_setup.sh line 165 
    await connection.send(message('simulationList',
                                  {'directories': os.listdir('/home/pi/scans/png/')} ))


events.filter(of_type('getPngDir')) \
    .subscribe(via_asyncio(getPngDir))
