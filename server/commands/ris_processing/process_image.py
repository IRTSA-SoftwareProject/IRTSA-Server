''' Created on 11 Apr. 2018
Processes thermgrams and returns the phase map.
@author: James Moran
'''

import scipy
import numpy
import warnings
from . import stabilise_image
warnings.filterwarnings('ignore')
from math import ceil
from scipy.optimize import curve_fit

def process_image(thermogram, method_select = 0, frame_length = -1, return_phase = 1,
                  xStartSkip = 0, xEndSkip = 0, yStartSkip = 0, yEndSkip = 0, frame_start = 0):
    ''' Expects a thermogram as a u_int16 3D numpy multdimensional array where
    each dimension is: [frame, row, column].
    Method_Select is to choose what form of processing to use what what stabilisation
    to implement. 
    Frame_length sets the numbers of frames to use in FFT analysis, uses all frames
    by default.
    Return_phase controls what phase will be returned, 0 is always a blank map;
    should almost always be 1.
    xStart, yStart, xEndSkip, and yEndSkip control how many pixels are skipped in
    each direction from the x and y axis. Useful when there is a small area of
    interest or we want to maximise contrast in an area. Also speed up processing.
    Returns an array of 2D phase maps in the format: [frame_index, row, column]
    '''
    
    yLength = thermogram.shape[1]; #Note that y is before x; a carry over from 
    xLength = thermogram.shape[2]; # Matlab...
    
    #Shrink the thermogram to the required size
    #The entire thermogram is passed even if only a section is to be analysed to
    #ensure the stabilization has the maximum range to secure stability
    thermogram = thermogram[:, yStartSkip:yLength-yEndSkip, xStartSkip:xLength-xEndSkip]
    
    total_frames = thermogram.shape[0]
        
    #If the number of analysis frames hasn't been specified, use the total number
    if (frame_start == -1) | (frame_start > total_frames):
        frame_start = 0
        
    if (frame_length == -1) | (frame_start + total_frames > total_frames):
        frame_length = total_frames - frame_start
    
    if (method_select == 0):
        thermogram = stabilise_image.stabilise_image(thermogram, frequency = frame_length, start_frame = frame_start, global_motion = False)
        return pulse_phase_thermography(thermogram, frame_length = frame_length)
    if (method_select == 1):
        thermogram = stabilise_image.stabilise_image(thermogram, frequency = frame_length, start_frame = frame_start, global_motion = True)
        return pulse_phase_thermography(thermogram, frame_length = frame_length)
    if (method_select == 2):
        thermogram = stabilise_image.stabilise_image(thermogram, frequency = frame_length, start_frame = frame_start, global_motion = False)
        return image_subtraction(thermogram, frame_length = frame_length)
    if (method_select == 3):
        thermogram = stabilise_image.stabilise_image(thermogram, frequency = frame_length, start_frame = frame_start, global_motion = True)
        return image_subtraction(thermogram, frame_length = frame_length)
    if (method_select == 4):
        thermogram = stabilise_image.stabilise_image(thermogram, frequency = frame_length, start_frame = frame_start, global_motion = False)
        return thermographic_signal_reconstruction(thermogram, frame_length = frame_length)
    if (method_select == 5):
        thermogram = stabilise_image.stabilise_image(thermogram, frequency = frame_length, start_frame = frame_start, global_motion = True)
        return thermographic_signal_reconstruction(thermogram, frame_length = frame_length)
    return thermogram[frame_start:frame_length, :, :];

def pulse_phase_thermography(thermogram, frame_length = -1, return_phase = 1, frame_start = 0):
    ''' Expects a thermogram as a u_int16 3D numpy multdimensional array where
    each dimension is: [frame, row, column]. 
    Frame_length sets the numbers of frames to use in FFT analysis, uses all frames
    by default.
    Return_phase controls what phase will be returned, 0 is always a blank map;
    should almost always be 1.
    Returns an array of 2D phase maps in the format: [frame_index, row, column]
    '''

    yLength = thermogram.shape[1]; #Note that y is before x; a carry over from 
    xLength = thermogram.shape[2]; # Matlab...
    
    #Preallocate phase maps
    phasemap = numpy.zeros([1, yLength, xLength], dtype = numpy.complex64)
    
    # Perform FFT over the range specified
    fftmap = scipy.fft(thermogram[frame_start : frame_start + frame_length, :, :],
                                  axis = 0)
    phasemap[0, :, :] = scipy.angle(fftmap[return_phase, :, :])
        
    return phasemap

def image_subtraction(thermogram, frame_length = -1, return_phase = 0, frame_start = 0):
    total_frames = thermogram.shape[0]
    
    yLength = thermogram.shape[1]; #Note that y is before x; a carry over from 
    xLength = thermogram.shape[2]; # Matlab...
    
    #Preallocate phase maps
    contrast_map = numpy.zeros([1, yLength, xLength], dtype = numpy.uint16)
    
    # sum the subtraction across each frame
    for frame in range(frame_start, frame_start + frame_length):
        contrast_map[0, :, :] += thermogram[frame] - thermogram[1]
               
    return contrast_map
    
def func(x, a, b, c, d, e):
    return a + b * numpy.power(numpy.log(x), 1)

def thermographic_signal_reconstruction(thermogram, frame_length = -1, return_phase = 0, frame_start = 0):
    #Last argument is which argument to return
    
    yLength = thermogram.shape[1]; #Note that y is before x; a carry over from 
    xLength = thermogram.shape[2]; # Matlab...
    
    #Preallocate phase maps
    coefficient_map = numpy.zeros([1, yLength, xLength], dtype = numpy.uint16)
     
    # perform reconstruction
    for xi in range (0, xLength):
        for yi in range(0, yLength):
            try: 
                popt, pcov = curve_fit(func, numpy.linspace(1, frame_length, frame_length),
                                       numpy.round(numpy.array(thermogram[frame_start:
                                                                          frame_start + frame_length,
                                                                          yi, xi]).ravel()), maxfev=100)
                coefficient_map[0, yi, xi] = popt[return_phase]
            except RuntimeError:
                print("No Match!")
                coefficient_map[0, yi, xi] = 0
            print((xi/xLength+yi/xLength/yLength)*100)
        
    return coefficient_map

