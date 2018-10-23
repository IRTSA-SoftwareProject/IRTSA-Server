''' Created on 11 Apr. 2018, last edited 23 Oct. 2018
Processes thermgrams and returns the phase map.
@author: James Moran [jpmoran.pac@gmail.com]
'''

import scipy
import numpy
import warnings
from . import stabilise_image
warnings.filterwarnings('ignore')
from math import ceil
from scipy.optimize import curve_fit

def process_image(thermogram, method_select = 0, frames_to_process = -1, frame_start = 0,
                  return_phase = 1, xStartSkip = 0, xEndSkip = 0, yStartSkip = 0, yEndSkip = 0):
    ''' Expects a thermogram as a u_int16 3D numpy multdimensional array where
    each dimension is: [frame, row, column].
    Method_Select is to choose what form of processing to use what what stabilisation
    to implement. 
    Frames_to_process sets the numbers of frames to use in FFT analysis, uses all frames
    by default.
    Frame_start is the first frame to process.
    Return_phase controls what phase will be returned, 0 is always a blank map;
    should almost always be 1.
    xStart, yStart, xEndSkip, and yEndSkip control how many pixels are skipped in
    each direction from the x and y axis. Useful when there is a small area of
    interest or we want to maximise contrast in an area. Also speed up processing.
    Returns an array of 2D phase maps in the format: [frame_index, row, column]
    '''
    
    yLength = thermogram.shape[1]; # Note that y is before x; a carry over from 
    xLength = thermogram.shape[2]; #  Matlab...
    
    # Shrink the thermogram to the required size
    # The entire thermogram is passed even if only a section is to be analysed to
    #  ensure the stabilization has the maximum range to secure stability
    thermogram = thermogram[:, yStartSkip:yLength-yEndSkip, xStartSkip:xLength-xEndSkip]
    
    total_frames = thermogram.shape[0]
        
    # If the number of analysis frames hasn't been specified, use the total number
    # The default sent by the app is -1, so if this is sent assume we want to max
    #  number of frames.
    # If the number of frames is longer than the total, reset to zero.
    if (frame_start == -1) | (frame_start > total_frames):
        frame_start = 0
    
    # Also check the number of frames processed doesn't run longer than the file.
    if (frames_to_process == -1) | (frame_start + total_frames > total_frames):
        frames_to_process = total_frames - frame_start
    
    # (Pseudo-)Static PPT
    if (method_select == 0):
        thermogram = stabilise_image.stabilise_image(thermogram, frames_to_process = frames_to_process, start_frame = frame_start, global_motion = False)
        return pulse_phase_thermography(thermogram, frames_to_process = frames_to_process)
    # Dynamic PPT
    if (method_select == 1):
        thermogram = stabilise_image.stabilise_image(thermogram, frames_to_process = frames_to_process, start_frame = frame_start, global_motion = True)
        return pulse_phase_thermography(thermogram, frames_to_process = frames_to_process)
    # (Pseudo-)Static Image Subtraction
    if (method_select == 2):
        thermogram = stabilise_image.stabilise_image(thermogram, frames_to_process = frames_to_process, start_frame = frame_start, global_motion = False)
        return image_subtraction(thermogram, frames_to_process = frames_to_process)
    # Dynamic Image Subtraction
    if (method_select == 3):
        thermogram = stabilise_image.stabilise_image(thermogram, frames_to_process = frames_to_process, start_frame = frame_start, global_motion = True)
        return image_subtraction(thermogram, frames_to_process = frames_to_process)
    # (Pseudo-)Static TSR
    #  Note that this TSR is very basic and unoptimised
    if (method_select == 4):
        thermogram = stabilise_image.stabilise_image(thermogram, frames_to_process = frames_to_process, start_frame = frame_start, global_motion = False)
        return thermographic_signal_reconstruction(thermogram, frames_to_process = frames_to_process)
    # Dynamic TSR
    if (method_select == 5):
        thermogram = stabilise_image.stabilise_image(thermogram, frames_to_process = frames_to_process, start_frame = frame_start, global_motion = True)
        return thermographic_signal_reconstruction(thermogram, frames_to_process = frames_to_process)
    return thermogram[frame_start:frames_to_process, :, :];

def pulse_phase_thermography(thermogram, frames_to_process = -1, frame_start = 0, 
                             return_phase = 1):
    ''' Expects a thermogram as a u_int16 3D numpy multdimensional array where
    each dimension is: [frame, row, column]. 
    frames_to_process sets the numbers of frames to use in FFT analysis, uses all frames
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
    fftmap = scipy.fft(thermogram[frame_start : frame_start + frames_to_process, :, :],
                                  axis = 0)
    phasemap[0, :, :] = scipy.angle(fftmap[return_phase, :, :])
        
    return phasemap

def image_subtraction(thermogram, frames_to_process = -1, frame_start = 0):
    total_frames = thermogram.shape[0]
    
    yLength = thermogram.shape[1]; #Note that y is before x; a carry over from 
    xLength = thermogram.shape[2]; # Matlab...
    
    #Preallocate phase maps
    contrast_map = numpy.zeros([1, yLength, xLength], dtype = numpy.uint16)
    
    # sum the subtraction across each frame
    for frame in range(frame_start, frame_start + frames_to_process):
        contrast_map[0, :, :] += thermogram[frame] - thermogram[1]
               
    return contrast_map
    
def func(x, a, b, c, d, e):
    ''' The function used for curve fitting. Note that typical TSR uses a greater number
    of coefficients (hence the other coeffs specified in the arguments, but this is already
    very slow.
    '''
    return a + b * numpy.power(numpy.log(x), 1)

def thermographic_signal_reconstruction(thermogram, frames_to_process = -1, return_phase = 0, frame_start = 0):
    #Last argument is which argument to return
    
    yLength = thermogram.shape[1]; #Note that y is before x; a carry over from 
    xLength = thermogram.shape[2]; # Matlab...
    
    #Preallocate phase maps
    coefficient_map = numpy.zeros([1, yLength, xLength], dtype = numpy.uint16)
     
    # perform reconstruction over each pixel
    for xi in range (0, xLength):
        for yi in range(0, yLength):
            try: 
                popt, pcov = curve_fit(func, numpy.linspace(1, frames_to_process, frames_to_process),
                                       numpy.round(numpy.array(thermogram[frame_start:
                                                                          frame_start + frames_to_process,
                                                                          yi, xi]).ravel()), maxfev=100)
                coefficient_map[0, yi, xi] = popt[return_phase]
            except RuntimeError:
                print("No Match!")
                coefficient_map[0, yi, xi] = 0
            print((xi/xLength+yi/xLength/yLength)*100) #Print the number of pixels analysed as a percentage
        
    return coefficient_map

