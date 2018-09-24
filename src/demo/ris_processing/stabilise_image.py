''' Created on 18 Sep. 2018
Stabilised a thermogram and returns a stabilised u_int16 3D numpy multdimensional array
@author: Jayden Rautman
'''

import cv2
import os
import imageio
from skimage.io import imread
import numpy as np

def stabilise_image(thermogram):
    ''' Expects a thermogram as a u_int16 3D numpy multdimensional array where
    each dimension is: [frame, row, column]. 
    '''
    
    ##set the frequency for the image, that is how often the image will reset.
    frequency_r = 100
    
    #frames = imread('0.gif')
    frames = thermogram
    #make frames 8bit to find features
    framesU8 = np.uint8(np.floor(np.real(frames)/np.max(frames)*255))
   
    #read the shape of the images
    height, width = frames[0].shape
    
    #set a transform matrix
    transformed_frames = [np.identity(3)]
    
    #initialise frame 1
    i = 1
    
    while i < len(frames):

        #get current frame
        current_frame = framesU8[i]
        #find points (good Features) on the previous and current frames and map them
        previous_points = cv2.goodFeaturesToTrack(current_frame, 100, 0.1, 1);
        current_points, status, _ = cv2.calcOpticalFlowPyrLK(framesU8[i-1], current_frame, previous_points, np.array([]))
        previous_points, current_points = map(lambda corners: corners[status.ravel().astype(bool)], [previous_points, current_points])
        transform = cv2.estimateRigidTransform(previous_points, current_points, False)
        
        #append the transform onto the tranforms.
        if transform is not None:
            transform = np.append(transform, [[0, 0, 1]], axis=0)
        if transform is None:
            transform = transforms[i-1]
        transformed_frames.append(transform)
        i = i+1
        
    #create a stabilised frames array and apply the transform to each frame in the image.
    stabilised_frames = []
    final_transform = np.identity(3)
    #stabilizedFrames = frames[0];
    for frame, transform, index in zip(frames, transformed_frames, range(len(frames))):
        transform = transform.dot(final_transform)
        if index % frequency_r == 0:
            transform = np.identity(3)
        final_transform = transform
        inverse_transform = cv2.invertAffineTransform(transform[:2])
        stabilised_frames.append(cv2.warpAffine(frame, inverse_transform, (width, height)))
        
    stabilisedFrames = np.stack(stabilised_frames,axis=0)    
        
    #return the new stabilised image
    return stabilisedFrames
    
