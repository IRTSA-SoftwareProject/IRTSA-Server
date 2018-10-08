# Created on 11/04/2018 edited 30/08/2018
# Example of using the ris_processing package
# @author: James Moran edited by Casper Pikaar

import ris_processing.read_ris
import ris_processing.file_io_thermal
import ris_processing.process_image
import ris_processing.stabilise_image
import numpy
import sys

#Time variable which has time passed to it from command executing script
#time = sys.argv[1]

if __name__ == '__main__':
    print('Reading file...')
    thermogram = ris_processing.file_io_thermal.open_png('C:\PNG Dumps\Final Thermal Hotspot/0')
    
    print('Saving thermogram to .gif...')
    if not ris_processing.file_io_thermal.save_gif(thermogram, 'C:/PNG Dumps/Processing/out.gif'):
        print('Failed to save .gif :(')
        
    print('Stabilising image')
    thermogram = ris_processing.stabilise_image.stabilise_image(thermogram,10)
    
    print('Saving  stabilised thermogram to .gif...')
    if not ris_processing.file_io_thermal.save_gif(thermogram, 'C:/PNG Dumps/Processing/out2.gif'):
        print('Failed to save .gif :(')
        
    print('Processing image...')
    #phasemap = ris_processing.process_image.process_image(thermogram, frame_length = 10, xStartSkip = 45, xEndSkip = 60, yStartSkip = 175)
    phasemap = ris_processing.process_image.process_image(thermogram, frame_length = 10, xStartSkip = 0, xEndSkip = 0, yStartSkip = 0)
    
    print('Saving phasemap to .png...')
    if phasemap.shape[0] == 1: #Check if there is only one thermogram
        if not ris_processing.file_io_thermal.save_png(phasemap, 'C:/PNG Dumps/Processing/out.png'):
            print('Failed to save .png :(')
    else: #Save all thermograms if more than one was produced
        for i in range(0, phasemap.shape[0] - 1):
            if not ris_processing.file_io_thermal.save_png(phasemap[i,:,:], 'C:/PNG Dumps/Processing/out-' + '{0:04d}'.format(i) + '.png'):
                print('Failed to save .png :(')
    
    print("Done! Process Complete.")