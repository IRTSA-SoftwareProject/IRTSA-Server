''' Created on 11 Apr. 2018, last editied 23 Oct. 2018
Example of using the ris_processing library to open and process a file.
@author: James Moran [jpmoran.pac@gmail.com] by Casper Pikaar
'''

import ris_processing.file_io_thermal
import ris_processing.process_image as process_image_file #this must be aliased, as the function shares the library name
import numpy
import sys
import os

if __name__ == '__main__':
    print('Reading file...')
    thermogram = ris_processing.file_io_thermal.open_file('../../src/scans/ris/')
    
    print('Stabilising image')
    
    # Use this line to save the output at any stage to a .gif for easy examination 
    # ris_processing.file_io_thermal.save_gif(thermogram, '../../src/processing/sacn.gif')
    
    # All the processing functionality is encapsulated in this function
    # Note that the phase map is stored in a numpy 3D array where the first dimension is the
    #  frame number
    phasemap = process_image_file.process_image(thermogram, method_select = 0,
                                                frames_to_process = -1, return_phase = 1,
                                                xStartSkip = 0, xEndSkip = 0, yStartSkip = 0,
                                                yEndSkip = 0, frame_start = 0)
    
    # In older builds, every phase of the thermogram used to be output, but this has
    #  been dummied out to improve functionality with the app.
    print('Saving phasemap to .png...')
    if phasemap.shape[0] == 1: #Check if there is only one thermogram
        if not ris_processing.file_io_thermal.save_png(phasemap, '../../src/processing/out.png'):
            print('Failed to save .png :(')
    else: #Save first thermogram if more than one was produced
        if not ris_processing.file_io_thermal.save_png(phasemap[0,:,:], '../../src/processing/out.png'):
            print('Failed to save.png :(')
    
    print("Done! Process Complete.")