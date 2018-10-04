# Created on 04/10/2018
# Module to simplify interfacing with the processing scripts
# @author: James Moran

import ris_processing.file_io_thermal
import ris_processing.process_image
import numpy
import asyncio
import sys

def process_image(reporting_function, path_to_save, simulation_select, process_select, frames_to_process = -1):
    print('Reading file...')
    thermogram = ris_processing.file_io_thermal.open_png('C:/PNG Dumps/' + simulation_select + '/0')
    
    asyncio.get_event_loop().run_until_complete(reporting_function("hi"))
    if not ris_processing.file_io_thermal.save_gif(thermogram, path_to_save + '.gif'):
        print('Failed to save .gif :(')
        
    print('Processing image...')
    phasemap = ris_processing.process_image.process_image(thermogram, frame_length = frames_to_process, xStartSkip = 0, xEndSkip = 0, yStartSkip = 0)
    
    print('Saving phasemap to .png...')
    if phasemap.shape[0] == 1: #Check if there is only one thermogram
        if not ris_processing.file_io_thermal.save_png(phasemap, path_to_save + '.png'):
            print('Failed to save .png :(')
    else: #Save all thermograms if more than one was produced
        for i in range(0, phasemap.shape[0] - 1):
            if not ris_processing.file_io_thermal.save_png(phasemap[i,:,:], path_to_save + '{0:04d}'.format(i) + '.png'):
                print('Failed to save .png :(')
    
    print("Done! Process Complete.")