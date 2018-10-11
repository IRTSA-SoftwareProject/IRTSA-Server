''' Created on 18 Sep. 2018
Stabilised a thermogram and returns a stabilised u_int16 3D numpy multdimensional array
@author: Jayden Rautman
'''

import cv2
import imageio
import numpy as np

def stabilise_image(thermogram,frequency = -1):
    ''' Expects a thermogram as a 3D numpy multdimensional array where
    each dimension is: [frame, row, column]. 
    '''
    
    #if the input frequency is -1, set the frequency to the full range.
    if frequency == -1:
        frequency = thermogram.shape[0]
    
    #CV requires frames to be 8 bit map any numpy array to 8bit
    framesU8 = np.uint8(np.floor(np.real(thermogram)/np.max(thermogram)*255))
   
    #read the shape of the images
    height, width = thermogram[0].shape
    
    #set a transform matrix
    transformed_frames = [np.identity(3)]
    
    #if frequency is the whole span, create a global motion matrix
    if frequency == thermogram.shape[0]:
        #create a translation matrix, this will remove everything except the translation of the t'form
        translation_matrix = np.array([[0,0,1],[0,0,1]])
        
        #initialise global transform as nonetype
        global_transform = None;  
             
        while (global_transform is None):
            #translation and frequency arrays which will be applied to get the global translation per frame
            frequency_matrix = np.array([[1, frequency, frequency], [frequency, 1, frequency]])
            #used to find global motion, will instead take frame sizes
            #find global transformation
            #find points (good Features) on the final and current frames and map them
            global_previous_points = cv2.goodFeaturesToTrack(framesU8[frequency-1], 100, 0.1, 1);
            global_current_points, global_status, _ = cv2.calcOpticalFlowPyrLK(framesU8[0], framesU8[frequency-1], global_previous_points, np.array([]))
            global_previous_points, global_current_points = map(lambda corners: corners[global_status.ravel().astype(bool)], [global_previous_points, global_current_points])
            global_transform = cv2.estimateRigidTransform(global_previous_points, global_current_points, False)
            
            #if global transform does not occur, take the 10 off the frequency
            frequency = int(round(frequency - (frequency * 0.1)));
            
    
        #if global transform can be found, create global transform matrix and reset frequency
        frequency_transform_matrix = np.divide(global_transform,frequency_matrix)
        global_transform_matrix = np.multiply(frequency_transform_matrix,translation_matrix)
        frequency = thermogram.shape[0]
   
    #initialise frame 1
    i = 1
     
    while i < len(thermogram):

        #get current frame (uint8)
        current_frame = framesU8[i]
        #find points (good Features) on the previous and current frames and map them
        previous_points = cv2.goodFeaturesToTrack(current_frame, 100, 0.1, 1);
        current_points, status, _ = cv2.calcOpticalFlowPyrLK(framesU8[i-1], current_frame, previous_points, np.array([]))
        previous_points, current_points = map(lambda corners: corners[status.ravel().astype(bool)], [previous_points, current_points])
        transform = cv2.estimateRigidTransform(previous_points, current_points, False)
        
        if frequency == thermogram.shape[0]:
            #take out the global transformation from the current transform
            transform = np.subtract(transform,global_transform_matrix)            
        
        #append the transform onto the transforms.
        if transform is not None:
            transform = np.append(transform, [[0, 0, 1]], axis=0)
        if transform is None:
            transform = transformed_frames[i-1]
        transformed_frames.append(transform)
        i = i+1
        
    #create a stabilised frames array and apply the transform to each frame in the image.
    stabilised_frames = []
    final_transform = np.identity(3)
    for frame, transform, index in zip(thermogram, transformed_frames, range(len(thermogram))):
        transform = transform.dot(final_transform)
        if index % frequency == 0:
            transform = np.identity(3)
        final_transform = transform
        inverse_transform = cv2.invertAffineTransform(transform[:2])
        stabilised_frames.append(cv2.warpAffine(frame, inverse_transform, (width, height)))
        
    stabilisedFrames = np.stack(stabilised_frames,axis=0)    
        
    #return the new stabilised image
    return stabilisedFrames
    
