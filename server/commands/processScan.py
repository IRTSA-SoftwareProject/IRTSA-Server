from server.messages import message
from server.events import events, of_type, via_asyncio
from server.commands.ris_processing import read_ris
from server.commands.ris_processing import file_io_thermal
from server.commands.ris_processing import process_image
import numpy
import datetime

async def processScan(event):
    connection = event.connection
    print('Running scan')
    #get current time to save scan
    time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    thermogram = file_io_thermal.open_png('/home/pi/scans/png/')
    await connection.send(message('scan_progress', {'percent': 30}))
    print('Saving thermogram to .gif...')
    if not file_io_thermal.save_gif(thermogram, '/var/www/html/irscans/' + time + '.gif'):
        print('Failed to save .gif :(')
    await connection.send(message('scan_progress', {'percent': 60}))
    print('Processing image...')
    phasemap = process_image.process_image(thermogram, frame_length = -1, xStartSkip = 0, xEndSkip = 0, yStartSkip = 0)
    await connection.send(message('scan_progress', {'percent': 95}))
    print('Saving phasemap to .png...')
    if phasemap.shape[0] == 1: #Check if there is only one thermogram
        if not file_io_thermal.save_png(phasemap, '/var/www/html/irscans/' + time + '.png'):
            print('Failed to save .png :(')
    else: #Save all thermograms if more than one was produced
        for i in range(0, phasemap.shape[0] - 1):
            if not file_io_thermal.save_png(phasemap[i,:,:], '/var/www/html/irscans/' + time + '{0:04d}'.format(i) + '.png'):
                print('Failed to save .png :(')
    await connection.send(message('scan_progress', {'percent': 100}))
    await connection.send(message('scan_complete', {'filename': '/irscans/' + time + '.png'}))
    print('Scan complete')


events.filter(of_type('processScan')) \
    .subscribe(via_asyncio(processScan))


