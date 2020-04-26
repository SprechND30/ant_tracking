#Preprocessing Ant Datasets for CFNets

This preprocessing program takes CSV file(s) with frame and bounding box information and outputs an IMDB video MatLab structure. It works with multiple videos and their info or one individual video. 

###Input

To prepare the dataset for preprocessing, the CSVs with the bounding box information must be in a directory called `bbox_info` and called `Ant_VIDNUM.csv`, where `VIDNUM` is the video number. For example, the first video's CSV should be called `bbox_info/Ant_0.csv`, and so on. The CSV for a particular video should contain rows representing individual frames and five columns: the four points on the bounding box for a particular frame and the name of the frame's file. In this case, as per the datasets already on the desktop, the files are assumed to be in `.jpg` format and have the frame number as the first part of its name. For example, the 512th frame in a video would be called `512.jpg`. 

###Running

####Flags

The program has two flags that _must_ be set, and a few more that can be set. 

- The first mandatory flag is the root directory: `--root_path MY_ROOT/`, where `MY_ROOT` is the name of the root directory for the datasets, with a '/' on the end. The CSVs should be in the `MY_ROOT/bbox_info/Ant_VIDNUM.csv`. The videos in question should be in a directory called `MY_ROOT/videos`, and follow the same naming convention as their corresponding CSVs: the first video should be called `MY_ROOT/videos/Ant_0.mp4`, and so on. 
- The second flag that must be set is `--output_filename`. Its function is pretty self-explanatory. It specifies the name of the outputted `.mat` file. Be sure to include '.mat' at the end of the file name!
- If the user decide what subset of his or her videos end up in the final IMDB by setting the `--first_vid_id` and `--last_vid_id` flags. By default, both are set to 0, which means that the IMDB will only include the first video (Ant_0.mp4/Ant_0.csv). These can be changed to control what continuous set of videos goes into the outputted MatLab structure.
- Other flags that can be set are the frame width and height, called `--frame_width` and `--frame_height`, respectively. They are set to 1920 and 1080 by default, but can be changed at the user's discretion. 
- The final flag needn't be set for the purposes of the Ant Tracking datasets; it only becomes relevant if there is more than one object being tracked in the same frame.

#### Run

The program requires _SciPy_ and _Abseil_ to be installed. It can be run with:

```bash
$ Python cfPreproc.py --root_path MY_ROOT/
```

### Output

The program will output a single `.mat` file, containing the IMDB (a MatLab structure). This structure acts as input for the CFNets algorithm.

It has several fields. When loaded into MatLab, it will look something like this:

```matlab
% NUM_VIDS = number of videos in the structure
% MAX_NUM_OBJ = 50, by default. Maximum number of objects in a frame. Not relevant for our datasets.
IMDB = 

	struct with fields:
		
			id:										[1xNUM_VIDS int]
			path:									{1xNUM_VIDS cell}
			nframes:							[1xNUM_VIDS int]
			n_valid_objects:			[1xNUM_VIDS int]
			valid_trackids:				[MAX_NUM_OBJ×NUM_VIDS double]
			valid_per_trackid:		{MAX_NUM_OBJ×NUM_VIDS cell}
			total_valid_objects:	[1x1 int]
			objects:							{1xNUM_VIDS cell}
```

- `id` is a row matrix that contains the IDs for the videos (0-NUM_VIDS).
- `path` is a cell array that contains the paths for each of those videos.
- `nframes` is another row matrix that holds the total number of frames for each video.
- `n_valid_objects`, `valid_trackids`, `valid_per_trackid`, and `total_valid_objects` have to do with the tracking IDs for the objects being tracked and the frames with that object in them. They are less relevant for our purposes and are filled in by the preprocessing program.
- `objects` is a cell array containing a column for each video. Each column is itself a cell array containing that video's particular __object structures__. An object, in this case, is a single bounding box in a single frame. They are represented by MatLab structures, and contain the following fields:
  -  `frame_path`: the file name of the frame's `.jpg`
  -  `track_id`: this particular object's track ID, in our case 0
  - `extent`: a 1x4 matrix containing the _xmin_, _ymin_, _xmax_, and _ymax_ values for the bounding box.
  - `frame_sz`: the frame's resolution.
  - `class`: what kind of object is being tracked. In our case, "ant" corresponds to 1.
  - `valid`: whether or not this object is valid for tracking. The Siamese preprocessing program that this program was based off of sets valid to `True` no matter what, so the field's purpose is a little unclear.