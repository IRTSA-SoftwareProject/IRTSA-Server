''' Created on 12 Apr. 2018
Saves thermograms obtained from read_ris as gifs and png files.
@author: James Moran
'''

import numpy
import imageio
import os

def _convert_to_u_int8(image):
    # Some information is lost in the casting process, but data operations still
    # occur on the full 16-bit pixels, so the only losses are in the display image
    # Maximise pixel depth by setting the lowest value to 0
    image = image-numpy.amin(image)
    image = numpy.uint8(image*256/numpy.amax(image))
    return image

def save_png(image, file_name):
    ''' Expects a 2D u_int16 numpy multdimensional array where
    each dimension is: [row, column].
    Converts to a u_int8 array and saves to *.png.
    '''
    #Check that the directory exists/was created
    check_dir(file_name)
    
    # Convert 16-bit range to 8-bit range (imageio.imsave is incompatible with 16-bit)
    image = _convert_to_u_int8(image)
    imageio.imsave(file_name, image)
    return True
    
def save_gif(images, file_name):
    ''' Expects a 3D u_int16 numpy multdimensional array where
    each dimension is: [frame, row, column].
    Converts to a u_int8 array and saves to *.gif.
    '''
    
    #Check that the directory exists/was created
    if not check_dir(file_name):
        return False
    
    # Convert 16-bit range to 8-bit range (imageio.imsave is incompatible with 16-bit)
    images = _convert_to_u_int8(images)
    imageio.mimsave(file_name, images)
    return True
    
def check_dir(directory):
    ''' Takes string as input and checks if the specified
    directory exists. Creates the directory if it doesn't,
    returns false if creation fails
    '''
    
    #Check if there is a directory specified
    slash_index = directory.rfind('/')
    if not slash_index == -1:
        path = directory[0:slash_index+1]
        
        if not os.path.exists(path):
            os.makedirs(path)
            
        #Check that path creation was successful
        if not os.path.exists(path):
            return False
    
    return True