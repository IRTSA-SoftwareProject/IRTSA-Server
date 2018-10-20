""" Created on 11 Apr. 2018
Processes thermgrams and returns the phase map.
@author: James Moran
"""

import scipy
import numpy
import warnings
from . import stabilise_image
warnings.filterwarnings('ignore')
from math import ceil
from scipy.optimize import curve_fit

def process_image(thermogram, method_select = 0, frame_length = -1, return_phase = 1,
                  xStartSkip = 0, xEndSkip = 0, yStartSkip = 0, yEndSkip = 0):
    """ Expects a thermogram as a u_int16 3D numpy multdimensional array where
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
    """

    yLength = thermogram.shape[1]; #Note that y is before x; a carry over from
    xLength = thermogram.shape[2]; # Matlab...

    #Shrink the thermogram to the required size
    thermogram = thermogram[:, yStartSkip:yLength-yEndSkip, xStartSkip:xLength-xEndSkip]

    if (method_select == 0):
        thermogram = ris_processing.stabilise_image.stabilise_image(thermogram, frame_length)
        return pulse_phase_thermography(thermogram, frame_length, 1)
    if (method_select == 1):
        return pulse_phase_thermography(thermogram, frame_length, 1)
    if (method_select == 2):
        thermogram = stabilise_image.stabilise_image(thermogram, frame_length)

        return image_subtraction(thermogram, frame_length, 1)
    if (method_select == 3):
        return image_subtraction(thermogram, frame_length, 1)
    if (method_select == 4):
        thermogram = ris_processing.stabilise_image.stabilise_image(thermogram, frame_length)
        return thermographic_signal_reconstruction(thermogram, frame_length, 1)
    if (method_select == 5):
        return thermographic_signal_reconstruction(thermogram, frame_length, 1)

def pulse_phase_thermography(thermogram, frame_length = -1, return_phase = 1):
    """ Expects a thermogram as a u_int16 3D numpy multdimensional array where
    each dimension is: [frame, row, column].
    Frame_length sets the numbers of frames to use in FFT analysis, uses all frames
    by default.
    Return_phase controls what phase will be returned, 0 is always a blank map;
    should almost always be 1.
    Returns an array of 2D phase maps in the format: [frame_index, row, column]
    """

    total_frames = thermogram.shape[0]

    #If the number of analysis frames hasn't been specified, use the total number
    if (frame_length == -1) | (total_frames > total_frames):
        frame_length = total_frames

    yLength = thermogram.shape[1]; #Note that y is before x; a carry over from
    xLength = thermogram.shape[2]; # Matlab...

    frame_index = 0 #Slice index
    #Preallocate phase maps
    phasemap_count = ceil(total_frames/frame_length)
    phasemap = numpy.zeros([phasemap_count, yLength, xLength], dtype = numpy.complex64)

    #If the number of frames have been specified, loop over the fft until the entire
    # thermogram has been analysed.
    for frame_index in range (0, phasemap_count):
        #Perform the fft over the frame_index'th slice of the thermogram
        fftmap = scipy.fft(thermogram[frame_index * frame_length :
                                      (frame_index + 1) * frame_length, :, :],
                                      n = frame_length, axis = 0)
        phasemap[frame_index, :, :] = scipy.angle(fftmap[return_phase, :, :])
        frame_index += 1

    return phasemap

def image_subtraction(thermogram, frame_length = -1, return_phase = 0):
    total_frames = thermogram.shape[0]

    #If the number of analysis frames hasn't been specified, use the total number
    if (frame_length == -1) | (total_frames > total_frames):
        frame_length = total_frames

    yLength = thermogram.shape[1]; #Note that y is before x; a carry over from
    xLength = thermogram.shape[2]; # Matlab...

    frame_index = 0 #Slice index
    #Preallocate phase maps
    contrast_count = ceil(total_frames/frame_length)
    contrast_map = numpy.zeros([contrast_count, yLength, xLength], dtype = numpy.uint16)

    #If the number of frames have been specified, loop over the fft until the entire
    # thermogram has been analysed.
    for frame_index in range (0, contrast_count):
        # sum the subtraction across each frame
        for frame in range(0, frame_length-1):
             contrast_map[frame_index, :, :] += thermogram[frame_index*frame_length+frame] - thermogram[frame_index*frame_length+frame+1]

        frame_index += 1

    return contrast_map

def func(x, a, b, c, d, e):
    return a + b * numpy.power(numpy.log(x), 1)

def thermographic_signal_reconstruction(thermogram, frame_length = -1, return_phase = 0):
    #Last argument is which argument to return
    total_frames = thermogram.shape[0]

    #If the number of analysis frames hasn't been specified, use the total number
    if (frame_length == -1) | (total_frames > total_frames):
        frame_length = total_frames

    yLength = thermogram.shape[1]; #Note that y is before x; a carry over from
    xLength = thermogram.shape[2]; # Matlab...

    frame_index = 0 #Slice index
    #Preallocate phase maps
    coefficient_count = ceil(total_frames/frame_length)
    coefficient_map = numpy.zeros([coefficient_count, yLength, xLength], dtype = numpy.uint16)

    #If the number of frames have been specified, loop over the fft until the entire
    # thermogram has been analysed.
    for frame_index in range (0, coefficient_count):
        # perform reconstruction
        for xi in range (0, xLength):
            for yi in range(0, yLength):
                try:
                    popt, pcov = curve_fit(func, numpy.linspace(1, frame_length, frame_length),
                                           numpy.round(numpy.array(thermogram[frame_index * frame_length :
                                                      (frame_index + 1) * frame_length,
                                                      yi, xi]).ravel()), maxfev=100)
                    coefficient_map[frame_index, yi, xi] = popt[return_phase]
                except RuntimeError:
                    print("No Match!")
                    coefficient_map[frame_index, yi, xi] = 0
                print((xi/xLength+yi/xLength/yLength)*100)
        frame_index += 1

    return coefficient_map

"""
popt, pcov = curve_fit(func, numpy.linspace(1, frame_length, frame_length),
                                           numpy.round(numpy.array(thermogram[frame_index * frame_length :
                                                      (frame_index + 1) * frame_length,
                                                      0, 150]).ravel()), maxfev=100)
                    
popt, pcov = curve_fit(func, numpy.array(list(range(0, frame_length)), dtype = numpy.uint16),
                                           scipy.ones(19), maxfev=100)

popt, pcov = curve_fit(func, numpy.linspace(1, frame_length, frame_length),
                                           scipy.ones([19]), maxfev=100)

popt, pcov = curve_fit(func, numpy.array(list(range(0, frame_length)), dtype = numpy.uint16),
                                           scipy.ones(19), maxfev=100)
                                           """
