""" Created on 11 Apr. 2018
This module provides a method to read *.ris files into a numpy
multidimensional array. Note that *.ris files are 16-bit per pixel.

<<<<<<< HEAD
@author: James Moran [jpmoran.pac@gmail.com]
"""

import re
import numpy
import struct

def _get_metadata(file):
    """ Read the metadata of the *.ris file. The metadata always appears first
    in the *.ris file and has a very specific format. Thie method extracts
    the important parameters, namely the image width and height, and number
    of frames.
    """
    # Get the file's meta data, assumes only one "description" field
    metadata = (file.readline()).decode("utf-8")
    temp = '\n'
    while '</description>' not in temp:
        temp = file.readline().decode("utf-8")
        metadata = metadata + str(temp)
        if '<metaitem name="imageWidth" value=' in str(temp):
            width = re.search('\d+', temp).group(0)
        if '<metaitem name="imageHeight" value=' in str(temp):
            height = re.search('\d+', temp).group(0)
        if '<metaitem name="numberOfFrames" value=' in str(temp):
            frames = re.search('\d+', temp).group(0)
    # The final "</ris>" is on the same line as the first data, so add it
    #  manually (it must follow the last "</description>").
    metadata = metadata + file.read(6).decode("utf-8")
    # Write start of data
    datastart = file.tell()
    return [int(width), int(height), int(frames), int(datastart)]


def get_thermogram(file, x_start = 0, width = float('inf'),
                y_start = 0, height = float('inf'),
                frame_start = 0, frame_count = float('inf')):
    """ Unpacks a .ris file into a u_int16 3D numpy matrix in the format:
    [frame, row, column]. _start arguments sets the pixel/frame to read from,
    width/height/frame_count sets how many bytes of each to read; useful to
    reduce the total data stored in memory by subsectioning the thermogram.
    """
    file.seek(0)
    # Get_Metadata returns the frame width and height of the file being examined.
    #  The width, height, and frame count specified to be examined must be less
    #  than or equal to this value.
    [width_max, height_max, frame_count_max, datastart] = _get_metadata(file)

    # If not specified, width, height, and frame count are set to infinite
    #  as the default call, so the value obtained from the metadata will
    #  always be smaller than this. The method also ensures the width and
    #  height are set to the maximum allowable values if set to greater than
    #  what is available.
    width = min(width, width_max)
    height = min(height, height_max)
    frame_count = min(frame_count, frame_count_max)

    # Ensure the start + size does not exceed the maximum. If it does, set it to
    #  the largest allowable within maximum.
    x_start = min(x_start+width,width_max)-width
    y_start = min(y_start+height,height_max)-height
    frame_start = min(frame_start+frame_count,frame_count_max)-frame_count

    # Create storage space for the thermogram
    thermogram = numpy.zeros([frame_count, height, width], dtype = numpy.uint16)

    for current_frame in range(frame_start, frame_start + frame_count):
        # Locate the frame in the file
        # The file is stored with each pixel stored as a 16-bit integer read left-to-right
        #  and top-to-bottom starting with the top left pixel. This means that the first x
        #  rows can be skipped if a size less than the frame height is specified. Same
        #  applies to the end of the file.
        for current_row in range(y_start, y_start + height):
            file.seek(datastart + (width_max*height_max*current_frame + width_max*current_row + x_start)*2) # Start of row, double because it is u_int16
            bytes_to_read = width*2 # Double because it is u_int16
            read_bytes = file.read(bytes_to_read)
            read_bytes = struct.unpack('H'*int(bytes_to_read/2),read_bytes) # Convert bytes to u_int16
            thermogram[current_frame-frame_start, current_row-y_start, :] = read_bytes

    return thermogram

def read_thermogram(file):
    ''' Encapsulates the reading process and provides a file interface.
    File is a path to a directory containing a .ris file.
    '''
    f = open(file, 'rb')
    thermogram = get_thermogram(f)
    f.close()
    return thermogram