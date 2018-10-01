from server.messages import message
from server.events import events, of_type, via_asyncio
from server.commands.ris_processing import read_ris
from server.commands.ris_processing import file_io_thermal
from server.commands.ris_processing import process_image
import numpy
import datetime

async def scan(event):
    connection = event.connection
    print('Running scan')
    time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file = "server/commands/ris/A35.ris"
    f = open(file, 'rb')
    await connection.send(message('scan_progress', {'percent': 30}))
    print('Reading file...')
    thermogram = read_ris.get_thermogram(f)
    await connection.send(message('scan_progress', {'percent': 60}))
    print('Saving thermogram to .gif...')
    file_io_thermal.save_gif(thermogram, '/var/www/html/irscans/' + time + '.gif')
    await connection.send(message('scan_progress', {'percent': 90}))
    print('Processing image...')
    phasemap = process_image.process_image(thermogram)
    await connection.send(message('scan_progress', {'percent': 95}))
    print('Saving phasemap to .png...')
    file_io_thermal.save_png(phasemap, '/var/www/html/irscans/' + time + '.png')
    f.close()
    await connection.send(message('scan_progress', {'percent': 100}))
    await connection.send(message('scan_complete', {'filename': '/scans/' + time + '.png'}))
    print('Scan complete')

events.filter(of_type('scan')) \
    .subscribe(via_asyncio(scan))






