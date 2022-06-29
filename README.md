# MRI QA Rating Tool 
The simple MRI rating tool allows users to open MRI images in nifti format (nii.gz, nii) and provide a numerical rating that describes the impact of artifact on the image quality. It is possible to resume previous rating sessions using the tool. If a previous rating session is selected, only images that are yet to have a rating will be opened for review. 

### Setup

 1. Create a directory to insert all required files 
 2. Download the python (.py) and config (.ini) files into this directory
 3. Create a sub-directory in this directory and copy the niifti format MRI images to be reviewed into here
 
###Usage 

 1. Run the script 'mri_qa-marker.py' using python in the terminal, code will depend on python version 
 Note: this step can take some time (~1 minute) as the script begins by creating a list of all the files in the specified directory with file types of either .nii or .nii.gz
```
#python v3
python3 mri_qa-marker.py

#python
python mri_qa-marker.py

```
Note: if this is the first time running the rating tool, a directory will be created titled 'mri_rating_record'. The .csv and .json files containing your ratings will be stored here. 

```
Directory 'MRI_rating_record' created! Your ratings will be stored here.
```

 2. Enter the session type 
 Enter the number corresponding to the session you wish to select.
 
 ```
 Resume a previous session? 
1 - New session
2 - Resume previous sessions
 
 ```
 3. New Session selection 
 Choosing a new session will bring up ITK-SNAP in a new window
 
 Note: do not close ITK-SNAP, after your review has been entered the current image will be closed and the next 
	image to be reviewed will automatically be opened
 
 4. Previous session selection
 Resuming a previous session will prompt you to select the session your wish to resume, enter the number corresponding to the session and press enter. ITK-SNAP will open the next image to be reviewed.
 
 ```
 Selection: 2
1. MRIrate_session-03-08-2021_162134
2. MRIrate_session-06-08-2021_150826
3. MRIrate_session-09-08-2021_190512
Enter session number to resume: 
 ```
 
 5. Entering an overall image quality rating 
 Enter the number corresponding to your overall image quality rating (e.g. 4). This field is mandatory.
 
 ```
 Enter rating for overall image quality
1. Very Poor 
2. Suboptimal 
3. Acceptable 
4. Above Average 
5. Excellent


Rating (1 to 5): 4
 ```
 
 6. Rating artifacts 
 Enter the letter corresponding to the artifact you wish to rate. It is possible to rate all, some or none of the artifacts. Simply press enter to proceed from this menu, the next image will be automatically opened once all artifact ratings are provided. 
 
 ```
 Enter letter to rate artifact or hit enter to continue. 

M - MOTION 
S - SUSCEPTIBILITY
F - FLOW/GHOSTING


Artifact: 
```

7. Ending the session 
Session will end when images are all reviewed, to end early input ctrl+C. A .json and .csv file will be automatically created when the session is ended, they will appear in the 'mri_rating_record' folder 
