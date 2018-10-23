''' Created on 04 Oct. 2018, last edited 23 Oct. 2018
Module to simplify interfacing with the processing scripts
@author: James Moran [jpmoran.pac@gmail.com]
'''

from . import file_io_thermal
from . import process_image as process_image_file # Must be aliased, as the function matches the filename
from server.messages import message
import asyncio
import sys
import numpy
import base64

async def process_image(connection, path_to_save, simulation_select,
                        process_select, frames_to_process = -1, frame_start = -1):
    '''Encapsulates the processing methods implemented. Returns a 3D numpy array containing
    the processed image, with [0, y, x]. Note that the first dimension only ever has a length
    of one.
    
    Connection is the address of the object encapsulating the request event from the app.
    Path_to_save is the directory to save the file .png to.
    Simulation_select chooses which folder to search for files (in theory each folder
    contains a different simulation, but in the actual application this could store the
    .ris files output by the camera).
    Frames_to_process is the total number of frames that should be processed out of the total.
    Frame_start is which frame to start from.
    '''
    
    print('Reading file...')
    try:
        thermogram = file_io_thermal.open_file('/home/pi/scans/png/' + simulation_select + '/')
    except:
        print('Unable to load file!')
        # The app hasn't implemented an error code that can be read from the server, so 
        #  we hack an error message by sending back a .png with the error written on it.
        # Load the error image
        scanImg = open('/home/pi/error/error.png', 'rb')
        scan = base64.b64encode(scanImg.read())
        scanImg.close()
        await connection.send(message('scan_progress', {'percent': 100}))
        # Send the error image
        await connection.send(message('scan_complete', {'base64EncodedString': scan.decode('utf-8')}))
        return
        
    await connection.send(message('scan_progress', {'percent': 10}))
    
    print('Selecting process...')
    # Select the processing method based on the case statement
    #  Python doesn't have real switch..case :(
    method = 0
    if process_select == "PPT Static": # The app directly sends the names from the combo box
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

    print('Processing image...')
    try:
        phasemap = process_image_file.process_image(thermogram, method_select = method,
                                                    frame_start = frame_start,
                                                    frames_to_process = frames_to_process,
                                                    xStartSkip = 0, xEndSkip = 0,
                                                    yStartSkip = 0, yEndSkip = 0)
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

    # Open the .png that was saved and code it in base 64 to send back
    scanImg = open(path_to_save + '.png', 'rb')
    scan = base64.b64encode(scanImg.read())
    scanImg.close()
    await connection.send(message('scan_progress', {'percent': 100}))
    await connection.send(message('scan_complete', {'base64EncodedString':
                                                    scan.decode('utf-8')}))

    print("Done! Process Complete.")

