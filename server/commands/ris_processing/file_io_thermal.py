''' Created on 12 Apr. 2018
Saves thermograms obtained from read_ris as gifs and png files.
@author: James Moran
'''

import numpy
import imageio
import math
import os
import ris_processing.read_ris

def _max_range(image):
    '''Scales the image such that the highest value is one and
    the lowest is 0. Intended to expand the pixel differences
    for more clear visuals and to minimise data loss.
    '''
    
    image = numpy.real(image) #ignore complex values
    #Maximise pixel depth by setting the lowest value to 0
    image = image-numpy.amin(image)
    #Scale to one
    image = image/numpy.amax(image)
    return image

def _convert_to_u_int8(image):
    ''' Some information is lost in the casting process, but data operations still
    occur on the full 16-bit pixels, so the only losses are in the display image
    '''
    
    image = _max_range(image)
    image = numpy.uint8(numpy.floor(numpy.real(image)/numpy.max(image)*255))
    return image

def _convert_to_u_int16(image):
    '''Most image formats are only 8-bit per pixel, so they have to be padded to
    get approximations of the full 16-bit data. Ideally the images should be stored
    in a 16-bit format
    '''
    
    image = _max_range(image)
    image = numpy.uint16(numpy.floor(numpy.real(image)*65535/numpy.max(image)))
    return image

def open_file(file_name):
    '''Receives the folder leading either a set of .png or a .ris. It extracts the data
    and returns it as numpy multi dim array. If more than one .ris is found, returns the
    first one.'''
    
    #Check if a path was specified in the filename
    slash_index = file_name.rfind('/')
    if not slash_index == -1:
        path = file_name[0:slash_index+1]
        filesList = os.listdir(path) #Get the list of files in this path
    else:
        filesList = os.listdir() #Just get files here
        
    #Check files until we find a .png or .ris
    for f in filesList:
        if (f.endswith(".png")):
            return open_png(path, filesList)
        elif (f.endswith(".ris")):
            return ris_processing.read_ris.read_thermogram(path + f)
        
    

def open_png(path, filesList):
    ''' Expects to receive the base name of a file and finds all other files in the
    file path that share the same start of the name. Assumes the files are listed
    alphabetically in the directory.
    '''
    
    imageCube = 0;
    
    firstImageFound = False #Var to track whether this is the first image
    for f in filesList:
        print (path + f)
        if (f.endswith(".png")):
            if not firstImageFound:
                #Needs to track the first image so that the frame size can be extracted
                #Adds a dummy 0th dimension so it can be concatenated along axis = 0
                imageCube = imageio.imread(path + '/' + f)[None,:,:]
                firstImageFound = True
            else:
                #Concat by extending along the 0th axis
                #Also needs the dummy 0th axis
                imageCube = numpy.concatenate((imageCube,
                                               imageio.imread(path + '/' + f)[None,:,:]),
                                               axis = 0)
    
    #imageCube = _convert_to_u_int16(imageCube)

    return imageCube

def save_png(image, file_name):
    ''' Expects a 2D u_int16 numpy multdimensional array where
    each dimension is: [row, column]. Converts to a u_int8
    array and saves to *.png. Also accepts [frame, row, column]
    arrays, but discards all but the first frame.
    '''
    #Check that the directory exists/was created
    if not check_dir(file_name):
        return False
    
    # Convert 16-bit range to 8-bit range (imageio.imsave is incompatible with 16-bit)
    if image.ndim > 2:
        image = _convert_to_u_int8(image[0,:,:]) #Only take the first frame
    else:
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