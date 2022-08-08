# MRI QA Rating Tool 
The simple MRI rating tool allows users to open MRI images in nifti format (nii.gz, nii) and provide a numerical rating that describes the impact of artifact on the image quality. It is possible to resume previous rating sessions using the tool. If a previous rating session is selected, only images that are yet to have a rating will be opened for review. 

# Setup

 1. Create a directory and download the python (.py) and config (.ini) files into this directory
 2. Open the file 'rating-tool_config.ini' and enter the filepath for the directory containing the nifti files to be reviewed, subdirectories will be located using the grep wildcard function
 
# Usage 

### 1. Run the script 
Run the script 'mri_qa-marker.py' using python in the terminal, code will depend on python version 

**Note:** this step can take some time (~1 minute) as the script begins by creating a list of all the files in the specified directory with file types of either .nii or .nii.gz
```
#python v3
python3 mri_qa-marker.py

#python
python mri_qa-marker.py
```
**Note:** if this is the first time running the rating tool, a directory will be created titled 'mri_rating_record'. The .csv and .json files containing your ratings will be stored here. 


