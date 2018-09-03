# Created on 11/04/2018 edited 30/08/2018
# Example of using the ris_processing package
# @author: James Moran edited by Casper Pikaar

import ris_processing.read_ris
import ris_processing.file_io_thermal
import ris_processing.process_image
import sys

#Time variable which has time passed to it from command executing script
time = sys.argv[1]

if __name__ == '__main__':
    file = "ris/A35.ris"
    f = open(file, 'rb')

    print('Reading file...')
    thermogram = ris_processing.read_ris.get_thermogram(f)
    
    print('Saving thermogram to .gif...')
    ris_processing.file_io_thermal.save_gif(thermogram, '/var/www/html/irscans/' + time + '.gif')
    
    print('Processing image...')
    phasemap = ris_processing.process_image.process_image(thermogram)
    
    print('Saving phasemap to .png...')
    ris_processing.file_io_thermal.save_png(phasemap, '/var/www/html/irscans/' + time + '.png')
    f.close()
    print("Done! Process Complete.")