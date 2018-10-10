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
from server.messages import message
import asyncio
import sys

def process_image(thermogram, frame_length = -1, return_phase = 1,
                  xStartSkip = 0, xEndSkip = 0, yStartSkip = 0, yEndSkip = 0):
    ''' Expects a thermogram as a u_int16 3D numpy multdimensional array where
    each dimension is: [frame, row, column]. 
    Frame_length sets the numbers of frames to use in FFT analysis, uses all frames
    by default.
    Return_phase controls what phase will be returned, 0 is always a blank map;
    should almost always be 1.
    xStart, yStart, xEndSkip, and yEndSkip control how many pixels are skipped in
    each direction from the x and y axis. Useful when there is a small area of
    interest or we want to maximise contrast in an area. Also speed up processing.
    Returns an array of 2D phase maps in the format: [frame_index, row, column]
    '''
    
    total_frames = thermogram.shape[0]
        
    #If the number of analysis frames hasn't been specified, use the total number
    if frame_length == -1:
        frame_length = total_frames
    
    yLength = thermogram.shape[1]; #Note that y is before x; a carry over from 
    xLength = thermogram.shape[2]; # Matlab...
    
    frame_index = 0 #Slice index
    #Preallocate phase maps
    phasemap_count = ceil(total_frames/frame_length)
    phasemap = numpy.zeros([phasemap_count,
                            yLength - yStartSkip - yEndSkip,
                            xLength - xStartSkip - xEndSkip], 
                            dtype = numpy.complex64)
    
    #If the number of frames have been specified, loop over the fft until the entire
    # thermogram has been analysed. 
    for frame_index in range (0, phasemap_count):
        #Perform the fft over the frame_index'th slice of the thermogram
        fftmap = scipy.fft(thermogram[frame_index * frame_length :
                                      (frame_index + 1) * frame_length,
                                      yStartSkip:yLength-yEndSkip,
                                      xStartSkip:xLength-xEndSkip],
                                      n = frame_length,
                                      axis = 0)
        phasemap[frame_index, :, :] = scipy.angle(fftmap[return_phase, :, :])
        frame_index += 1
        
    return phasemap


async def process_image_publish_updates(connection, thermogram, frame_length = -1,
                                  return_phase = 1, xStartSkip = 0, xEndSkip = 0,
                                  xStartSkip = 0, yEndSkip = 0):
    ''' Expects a thermogram as a u_int16 3D numpy multdimensional array where
    each dimension is: [frame, row, column]. 
    Frame_length sets the numbers of frames to use in FFT analysis, uses all frames
    by default.
    Return_phase controls what phase will be returned, 0 is always a blank map;
    should almost always be 1.
    xStart, yStart, xEndSkip, and yEndSkip control how many pixels are skipped in
    each direction from the x and y axis. Useful when there is a small area of
    interest or we want to maximise contrast in an area. Also speed up processing.
    Returns an array of 2D phase maps in the format: [frame_index, row, column]
    Includes a new first parameter that indicates the function used to publish updates.
    '''
    
    total_frames = thermogram.shape[0]
        
    #If the number of analysis frames hasn't been specified, use the total number
    if frame_length == -1:
        frame_length = total_frames
    
    yLength = thermogram.shape[1]; #Note that y is before x; a carry over from 
    xLength = thermogram.shape[2]; # Matlab...
    
    frame_index = 0 #Slice index
    #Preallocate phase maps
    phasemap_count = ceil(total_frames/frame_length)
    phasemap = numpy.zeros([phasemap_count,
                            yLength - yStartSkip - yEndSkip,
                            xLength - xStartSkip - xEndSkip], 
                            dtype = numpy.complex64)
    
    #If the number of frames have been specified, loop over the fft until the entire
    # thermogram has been analysed. 
    for frame_index in range (0, phasemap_count):
        #Perform the fft over the frame_index'th slice of the thermogram
        fftmap = scipy.fft(thermogram[frame_index * frame_length :
                                      (frame_index + 1) * frame_length,
                                      yStartSkip:yLength-yEndSkip,
                                      xStartSkip:xLength-xEndSkip],
                                      n = frame_length,
                                      axis = 0)
        phasemap[frame_index, :, :] = scipy.angle(fftmap[return_phase, :, :])
        frame_index += 1
        await connection.send(message('scan_progress', {'percent':
                                                        10+floor(80*frame_index/phasemap_count)}))
        
    return phasemap