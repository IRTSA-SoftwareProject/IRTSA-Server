''' Created on 11 Apr. 2018
Processes thermgrams and returns the phase map.
@author: James Moran
'''

import scipy

def process_image(thermogram, return_phase = 1):
    ''' Expects a thermogram as a u_int16 3D numpy multdimensional array where
    each dimension is: [frame, row, column]. Return_phase controls 
    what phase will be returned, 0 is always a blank map; should almost
    always be 1.
    Returns a 2D phase map in the format: [row, column]    
    '''
    fftmap = scipy.fft(thermogram, axis = 0)
    phasemap = scipy.angle(fftmap[return_phase, :, :])
    return phasemap
