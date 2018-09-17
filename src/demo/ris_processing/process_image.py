''' Created on 11 Apr. 2018
Processes thermgrams and returns the phase map.
@author: James Moran
'''

import scipy
import numpy
import warnings
warnings.filterwarnings('ignore')
from math import ceil

def process_image(thermogram, frame_length = -1, return_phase = 1):
    ''' Expects a thermogram as a u_int16 3D numpy multdimensional array where
    each dimension is: [frame, row, column]. 
    Frame_length sets the numbers of frames to use in FFT analysis, uses all frames
    by default.
    Return_phase controls what phase will be returned, 0 is always a blank map;
    should almost always be 1.
    Returns an array of 2D phase maps in the format: [frame_index, row, column]
    '''
    
    total_frames = thermogram.shape[0]
        
    #If the number of analysis frames hasn't been specified, use the total number
    if frame_length == -1:
        frame_length = total_frames
    
    #If the number of frames have been specified, loop over the fft until the entire
    # thermogram has been analysed. 
    frame_index = 0 #Slice index
    #Preallocate phase maps
    phasemap_count = ceil(total_frames/frame_length)
    
    phasemap = numpy.zeros([phasemap_count, thermogram.shape[1],
                            thermogram.shape[2]], dtype = numpy.complex64)
    
    

    for frame_index in range (0, phasemap_count):
        #Perform the fft over the frame_index'th slice of the thermogram
        fftmap = scipy.fft(thermogram[frame_index * frame_length :
                                      (frame_index + 1) * frame_length,
                                      :, :],
                                      n = frame_length,
                                      axis = 0)
        phasemap[frame_index, :, :] = scipy.angle(fftmap[return_phase, :, :])
        frame_index += 1
        
    return phasemap
