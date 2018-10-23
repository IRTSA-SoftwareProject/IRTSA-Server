''' Created on 18 Sep. 2018, last edited 23 Oct. 2018
Stabilised a thermogram and returns a stabilised u_int16 3D numpy multdimensional array
@author: Jayden Rautman, edited by James Moran [jpmoran.pac@gmail.com]
'''

import cv2
import imageio
import numpy as np
from . import file_io_thermal

def stabilise_image(thermogram, frames_to_process = -1, start_frame = -1, global_motion = False):
    ''' Stabilises an input video as a 3D numpy array. Can use global motion to maintain a 
    single dimension of movement; useful for implementing DPPT.
     
    Expects a thermogram as a 3D numpy multdimensional array where
    each dimension is: [frame, row, column]. 
    Frames_to_process sets the numbers of frames to use in FFT analysis, uses all frames
    by default.
    Frame_start is the first frame to process.
    Return_phase controls what phase will be returned, 0 is always a blank map;
    should almost always be 1.
    Global_motion indicates whether global motion should be used
    Returns an array in the format: [frame_index, row, column]
    '''
        
    #Store original frames_to_process, as it is changed later in the code
    _frames_to_process = frames_to_process
 
    #CV requires frames to be 8 bit map any numpy array to 8bit
    framesU8 = file_io_thermal._convert_to_u_int8(thermogram)
   
    #read the shape of the images
    height, width = thermogram[0].shape
    
    #set a transform matrix
    transformed_frames = [np.identity(3)]
    
    #create a global motion matrix if specified
    if global_motion:
        #create a translation matrix, this will remove everything except the translation of the t'form
        translation_matrix = np.array([[0,0,1],[0,0,1]])
        
        #initialise global transform as nonetype
        global_transform = None;  
             
        while (global_transform is None):
            #translation and frames_to_process arrays which will be applied to get the global translation per frame
            frames_to_process_matrix = np.array([[1, frames_to_process, frames_to_process], [frames_to_process, 1, frames_to_process]])
            #used to find global motion, will instead take frame sizes
            #find global transformation
            #find points (good Features) on the final and current frames and map them
            global_previous_points = cv2.goodFeaturesToTrack(framesU8[frames_to_process-1], 100, 0.1, 1);
            global_current_points, global_status, _ = cv2.calcOpticalFlowPyrLK(framesU8[0], framesU8[frames_to_process-1], global_previous_points, np.array([]))
            global_previous_points, global_current_points = map(lambda corners: corners[global_status.ravel().astype(bool)], [global_previous_points, global_current_points])
            global_transform = cv2.estimateRigidTransform(global_previous_points, global_current_points, False)
            
            #if global transform does not occur, take the 10 off the frames_to_process
            frames_to_process = int(round(frames_to_process - (frames_to_process * 0.1)));
            
    
        #if global transform can be found, create global transform matrix and reset frames_to_process
        frames_to_process_transform_matrix = np.divide(global_transform,frames_to_process_matrix)
        global_transform_matrix = np.multiply(frames_to_process_transform_matrix,translation_matrix)
        frames_to_process = _frames_to_process 
   
    #initialise frame 1
    i = start_frame + 1 #+1 because tracking must start from the second frame
    while i < (start_frame + frames_to_process):

        #get current frame (uint8)
        current_frame = framesU8[i]
        #find points (good Features) on the previous and current frames and map them
        previous_points = cv2.goodFeaturesToTrack(current_frame, 100, 0.1, 1);
        current_points, status, _ = cv2.calcOpticalFlowPyrLK(framesU8[i-1], current_frame, previous_points, np.array([]))
        previous_points, current_points = map(lambda corners: corners[status.ravel().astype(bool)], [previous_points, current_points])
        transform = cv2.estimateRigidTransform(previous_points, current_points, False)
        
        if global_motion:
            #take out the global transformation from the current transform
            transform = np.subtract(transform,global_transform_matrix)            
        
        #append the transform onto the transforms.
        if transform is not None:
            transform = np.append(transform, [[0, 0, 1]], axis=0)
        if transform is None:
            transform = transformed_frames[-1]
        transformed_frames.append(transform)
        i = i+1
        
    #create a stabilised frames array and apply the transform to each frame in the image.
    stabilised_frames = []
    final_transform = np.identity(3)
    thermogram = thermogram[start_frame:start_frame+frames_to_process, :, :]
    for frame, transform, index in zip(thermogram, transformed_frames, range(len(thermogram))):
        transform = transform.dot(final_transform)
        if index % frames_to_process == 0:
            transform = np.identity(3)
        final_transform = transform
        inverse_transform = cv2.invertAffineTransform(transform[:2])
        stabilised_frames.append(cv2.warpAffine(frame, inverse_transform, (width, height)))
        
    stabilisedFrames = np.stack(stabilised_frames,axis=0)    
    
    #return the new stabilised image
    return stabilisedFrames
    
