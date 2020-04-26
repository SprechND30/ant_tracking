#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Nathaniel Sprecher
"""

import numpy as np
import scipy.io as sio
import csv
from absl import flags
from absl import app
FLAGS = flags.FLAGS

# Define some flags
flags.DEFINE_string('root_path', None, 'Root path to video, frames, and csv')
flags.DEFINE_string('output_filename', None, 'Name of the output file. Be sure to include ".mat"')
flags.DEFINE_integer('frame_width', 1920, 'Width of frames')
flags.DEFINE_integer('frame_height', 1080, 'Height of frames')
flags.DEFINE_integer('first_vid_id', 0, 'ID number of the first video included')
flags.DEFINE_integer('last_vid_id', 0, 'ID number of the last video included')
flags.DEFINE_integer('max_trackids', 50, 'Maximum number of objects in the same frame')


def main(argv):
    print("Initializing...\n")
        
    root_path = FLAGS.root_path
    out_file = FLAGS.output_filename
    frame_w = FLAGS.frame_width
    frame_h = FLAGS.frame_height
    total_num_vids = FLAGS.last_vid_id - FLAGS.first_vid_id + 1
    MAX_TRACKIDS = FLAGS.max_trackids
    imdb = {}

    imdb['id'] =  np.zeros(total_num_vids) # IDs for videos (int array)
    imdb['path'] = np.zeros((total_num_vids,), dtype=np.object) # Paths to videos (list of strings)
    imdb['nframes'] = np.zeros(total_num_vids) # Number of frames per vid (int array)
    imdb['n_valid_objects'] = np.zeros(total_num_vids) # (int array)
    imdb['valid_trackids'] = np.zeros((MAX_TRACKIDS, total_num_vids)) # (2D int array (ids per vids (row: ids, col: videos)))
    
    # Make a numpy array of objects then fill it with empty
    imdb['valid_per_trackid'] = np.zeros((MAX_TRACKIDS, total_num_vids), dtype=np.object) # (2D cell array (row: ids, col: videos))
    i=0
    while i<MAX_TRACKIDS:
        j=0
        while j<total_num_vids:
            imdb['valid_per_trackid'][i][j] = np.empty( shape=(0, 0) )
            j = j+1
        i = i+1
        
    imdb['total_valid_objects'] = np.zeros(1); # Number of objects overall in the IMDB
    imdb['objects'] = np.zeros((total_num_vids,), dtype=np.object) # Where the majic happens! (cell array! (row: stuff-in-vid, col: videos)) 
    
    frameNum = 0
    vidNum = 0
    
    
    # FOR EACH VIDEO
    while vidNum < len(imdb['id']):
        print("Video "+str(vidNum)+":\n")
        # Build dict for this video
        vid_obj = []
        
        
        # Open and save CSV file as list 
        csvArr = []
        csv_name = root_path+'bbox_info/Ant_'+str(vidNum)+'.csv'
        i = 0
        with open(csv_name, encoding='utf-8-sig') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                csvArr.append([])
                csvArr[i].append(float(row[0]))
                csvArr[i].append(float(row[1]))
                csvArr[i].append(float(row[2]))
                csvArr[i].append(float(row[3]))
                csvArr[i].append(row[4])
                #print("\tCSV row "+str(i)+": "+str(csvArr[i]))
                i = i+1
            
        startFrame = int(csvArr[0][4].split('.')[0])
        endFrame = int(csvArr[len(csvArr)-1][4].split('.')[0])
        print("\tStart frame = "+str(startFrame)+" and end frame = "+str(endFrame))
        
        # Update IMDB for this vid
        imdb['id'][vidNum] = vidNum # Adds this video's ID (vidNum)
        imdb['path'][vidNum]=(root_path+'videos/Ant_'+str(vidNum)+'.MP4') # Adds this video's path
        imdb['nframes'][vidNum] = (endFrame-startFrame) # Adds number of frames for this video (int array)
        #imdb['n_valid_objects'][vidNum] = 1 # 1, I think (int array) Might need to be hardcoded
        
    
        # FOR EACH FRAME
        frameNum=startFrame
        while frameNum < endFrame:
            
            print("\tFrame "+str(frameNum)+"\n")
            line = frameNum - startFrame
            vid_obj.append({'frame_path': [], 'track_id': [], 'extent': [], 'frame_sz': [], 'class': [], 'valid': True})
            
            
            # CSV: xmin, ymin, xmax, ymax, imageName
            frame = csvArr[line]
            vid_obj[line]['track_id'] = [0]
            vid_obj[line]['class'] = [1]
            vid_obj[line]['frame_sz'] = [frame_w, frame_h]
            vid_obj[line]['extent'] = [frame[0], frame[1], frame[2], frame[3]]
            #vid_obj[line]['valid'] = True
            vid_obj[line]['frame_path'] = frame[4]; 
            
            
            # Now, I'd be lying if I said I FULLY understand this part, but I DO know it needs to be here...
            if(vid_obj[line]['valid']):
                # Update count of valid objects and trackids (??)
                imdb['n_valid_objects'][vidNum] = imdb['n_valid_objects'][vidNum] + 1;
                imdb['valid_trackids'][vid_obj[line]['track_id'][0]][vidNum] = imdb['valid_trackids'][vid_obj[line]['track_id'][0]][vidNum] + 1;
                # Save list of valid objects per trackid for easy random choice pairs
                imdb['valid_per_trackid'][vid_obj[line]['track_id'][0]][vidNum] = np.append(imdb['valid_per_trackid'][vid_obj[line]['track_id'][0]][vidNum], line);
        
            frameNum = frameNum + 1
            
         
        imdb['objects'][vidNum] = (vid_obj);
        #print(str(imdb['objects']))
        imdb['total_valid_objects'][0] = imdb['total_valid_objects'][0] + imdb['n_valid_objects'][vidNum]
        print('Found '+str(imdb['n_valid_objects'][vidNum])+' valid objects in '+str(imdb['nframes'][vidNum])+' frames\n\n');
        vidNum = vidNum + 1
        
    
    # WRITE IMDB FILE
    print("Writing IMDB to .mat file...")
    sio.savemat(out_file, imdb)
        
        
if __name__ == "__main__":
    app.run(main)