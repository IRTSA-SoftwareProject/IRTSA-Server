# Created on 04/10/2018
# Module to simplify interfacing with the processing scripts
# @author: James Moran

from . import file_io_thermal
from . import process_image as process_image_file
from server.messages import message
import asyncio
import sys
import numpy
import base64

async def process_image(connection, path_to_save, simulation_select, process_select, frames_to_process = -1, frame_start = -1):
    print('Reading file...')
    try:
        thermogram = file_io_thermal.open_file('/home/pi/scans/png/' + simulation_select + '/')
    except:
        print('Unable to load file!')
        scanImg = open('/home/pi/error/error.png', 'rb')
        scan = base64.b64encode(scanImg.read())
        scanImg.close()
        await connection.send(message('scan_progress', {'percent': 100}))
        await connection.send(message('scan_complete', {'base64EncodedString': scan.decode('utf-8')}))
        return
        
    await connection.send(message('scan_progress', {'percent': 10}))
    
    print('Processing image...')
    #Select the processing method based on the case statement:
    method = 0

    print(simulation_select)

    if process_select == "PPT Static":
        method = 0
    if process_select == "PPT Dynamic":
        method = 1
    if process_select == "Image Subtraction Static":
        method = 2
    if process_select == "Image Subtraction Dynamic":
        method = 3
    if process_select == "TSR Static":
        method = 4
    if process_select == "TSR Dynamic":
        method = 5

    print(method)

    try:
        phasemap = process_image_file.process_image(thermogram, method_select = method, frame_start = frame_start, frame_length = frames_to_process, xStartSkip = 0, xEndSkip = 0, yStartSkip = 0, yEndSkip = 0)
    except:
        print('Unable to process file!')
        scanImg = open('/home/pi/error/error.png', 'rb')
        scan = base64.b64encode(scanImg.read())
        scanImg.close()
        await connection.send(message('scan_progress', {'percent': 100}))
        await connection.send(message('scan_complete', {'base64EncodedString': scan.decode('utf-8')}))
        return

    await connection.send(message('scan_progress', {'percent': 90}))

    print('Saving phasemap to .png...')
    if phasemap.shape[0] == 1: #Check if there is only one thermogram
        if not file_io_thermal.save_png(phasemap, path_to_save + '.png'):
            print('Failed to save .png :(')
    else: #Save first thermogram if more than one was produced
        if not file_io_thermal.save_png(phasemap[0,:,:], path_to_save + '.png'):
            print('Failed to save.png :(')

    scanImg = open(path_to_save + '.png', 'rb')
    scan = base64.b64encode(scanImg.read())
    scanImg.close()
    await connection.send(message('scan_progress', {'percent': 100}))
    await connection.send(message('scan_complete', {'base64EncodedString': scan.decode('utf-8')}))

    print("Done! Process Complete.")


async def export_gif(connection, path_to_save, simulation_select):
    print('Reading file...')
    thermogram = file_io_thermal.open_png('/home/pi/scans/png/')
    await connection.send(message('export_progress', {'percent': 50}))

    if not file_io_thermal.save_gif(thermogram, path_to_save + '.gif'):
        print('Failed to save .gif :(')
        await connection.send(message('error', {'Unable to save'}))
    
    scanImg = open(path_to_save + '.gif', 'rb')
    scan = base64.b64encode(scanImg.read())
    scanImg.close()
    await connection.send(message('export_progress', {'percent': 100}))
    await connection.send(message('exprot_complete', {'base64EncodedString': scan.decode('utf-8')}))
     

    print("Done! Process Complete.")
