# Created on 04/10/2018
# Module to simplify interfacing with the processing scripts
# @author: James Moran

from . import file_io_thermal
from . import process_image_file
from server.messages import message
import numpy
import asyncio
import sys
import base64

async def process_image(connection, path_to_save, simulation_select, process_select, frames_to_process = -1):
    print('Reading file...')
    thermogram = ris_processing.file_io_thermal.open_png('C:/PNG Dumps/')
    await connection.send(message('scan_progress', {'percent': 30}))

    if not file_io_thermal.save_gif(thermogram, path_to_save + '.gif'):
        print('Failed to save .gif :(')
    await connection.send(message('scan_progress', {'percent': 60}))
    
    print('Processing image...')
    phasemap = process_image_file.process_image(thermogram, frame_length = frames_to_process, xStartSkip = 0, xEndSkip = 0, yStartSkip = 0)

    await connection.send(message('scan_progress', {'percent': 95}))

    print('Saving phasemap to .png...')
    if phasemap.shape[0] == 1: #Check if there is only one thermogram
        if not file_io_thermal.save_png(phasemap, path_to_save + '.png'):
            print('Failed to save .png :(')
    else: #Save all thermograms if more than one was produced
        for i in range(0, phasemap.shape[0] - 1):
            if not file_io_thermal.save_png(phasemap[i,:,:], path_to_save + '{0:04d}'.format(i) + '.png'):
                print('Failed to save .png :(')
    scanImg = open(path_to_save + '.png', 'rb')
    scan = base64.b64encode(scanImg.read())
    scanImg.close()
    await connection.send(message('scan_progress', {'percent': 100}))
    await connection.send(message('scan_complete', {'base64EncodedString': scan.decode('utf-8')}))
     

    print("Done! Process Complete.")
