# Created on 11/04/2018 edited 30/08/2018
# Example of using the ris_processing package
# @author: James Moran edited by Casper Pikaar

import ris_processing.file_io_thermal
import ris_processing.process_image as process_image_file
import ris_processing.noise
import numpy
import sys

import os

#Time variable which has time passed to it from command executing script

if __name__ == '__main__':
    print('Reading file...')
    thermogram = ris_processing.file_io_thermal.open_file('C:/PNG Dumps/FINAL HOTSPOT/')
    
    #thermogram = ris_processing.noise.noisy("s&p", thermogram)
    
    print('Stabilising image')
    #thermogram = ris_processing.stabilise_image.stabilise_image(thermogram, start_frame = 50, frequency = 20, global_motion = True)
    
    #ris_processing.file_io_thermal.save_gif(thermogram, 'C:/PNG Dumps/Processing/stable.gif')
    
    phasemap = process_image_file.process_image(thermogram, 1, frame_length = 20, frame_start = 0, xStartSkip = 0, xEndSkip = 0, yStartSkip = 0, yEndSkip = 0)
    
    print('Saving phasemap to .png...')
    if phasemap.shape[0] == 1: #Check if there is only one thermogram
        if not ris_processing.file_io_thermal.save_png(phasemap, 'C:/PNG Dumps/Processing/out.png'):
            print('Failed to save .png :(')
    else: #Save first thermogram if more than one was produced
        if not ris_processing.file_io_thermal.save_png(phasemap[0,:,:], 'C:/PNG Dumps/Processing/out.png'):
            print('Failed to save.png :(')
    
    print("Done! Process Complete.")