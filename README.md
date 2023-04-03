# MRI Image Quality Assement Tool 
The simple MRI rating tool allows users to iterate through nifti files based on a filename criteria and provide a numerical rating that describes the scan quality. It is possible to resume previous rating sessions using the tool. If a previous rating session is selected, only images that are yet to have a rating will be opened for review and all images can be viewed a maximum of 3 times.

# Installations 

## Python

### Windows & Mac 
Here are the steps to install Python and add it to your system's PATH:

- Download that latest official version of Python https://www.python.org/downloads/.
- Choose the appropriate installer for your operating system (Windows: Windows x86-64 executable installer, macOS: macOS 64-bit installer)
- Run the installer, ensuring that you select "Add Python to PATH" during the installation
- After the installation has finisihed, open a terminal window and enter "python" to test that it is callable from the terminal 


# Linux:

Open a terminal window and install Python by running the following commands:


```
sudo apt update
sudo apt install python3
```

Verify that Python has been installed correctly by entering the following command:


```
python3 --version
```

Add Python to your PATH by opening the ~/.bashrc file in your home directory:

```
nano ~/.bashrc
```

Add the following line to the end of the file:

```
export PATH=$PATH:/usr/bin/python3
```


Save the changes and exit the editor and reload your bashrc file so the changes take effect: 

```
source ~/.bashrc
```

Test that python was successfully installed by calling python in the terminal:
```
python3
```

# Setup

The rating script requires some additional packages to run: pymongo, configparser, getpass, subprocess, datetime, re, and dotenv. After ensuring that Python 3.x is installed successfully, you will need to install the required packages for the script to run. You can do this by opening a terminal or command prompt and running the following command:

```
pip install pymongo configparser getpass subprocess datetime re python-dotenv
```

To run the script, you will need to have the necessary files. These files are:

    mri_rater.py
    mriqa_marker_objects_20230130.py
    rating_config.ini
    settings.env

Place all these files in the same directory.

# Credentials

Before running the script, you will need to set the MongoDB credentials in the settings.env file. The file should look like this:

```
MONGO_DB_USRNAME=<username>
MONGO_DB_PW=<password>
```
Replace <username> and <password> with the appropriate values for your MongoDB instance.

# Usage 
To run the script, open a terminal or command prompt and navigate to the directory where the files are stored. You can review all files or a single subject, and you can set the search parameters and review parameters in the rating_config.ini file. Then run the following command:

**Note**: the script requires a scan viewer to be installed on your system (itksnap, fsleyes, MRview)

    
```
python mri_qa-marker.py
```
   
**Note:** if this is the first time running the rating tool, a directory will be created titled 'mri_rating_record'. The .csv and .json files containing your ratings will be stored here. 

```
Directory 'MRI_rating_record' created! Your ratings will be stored here.
```
Follow the prompts to begin a new session or resume a previous session. 
  
 ```
 Resume a previous session? 
1 - New session
2 - Resume previous sessions
 ```
### 3. New Session selection 
 Choosing a new session will bring up ITK-SNAP in a new window
 
**Note:** do not close ITK-SNAP, after your review has been entered the current image will be closed and the next image to be reviewed will automatically be opened
 
### 4. Previous session selection
Resuming a previous session will prompt you to select the session your wish to resume, enter the number corresponding to the session and press enter. ITK-SNAP will open the next image to be reviewed.
 
 ```
 Selection: 2
1. MRIrate_session-03-08-2021_162134
2. MRIrate_session-06-08-2021_150826
3. MRIrate_session-09-08-2021_190512
Enter session number to resume: 
 ```
 
 ### 5. Check image label 
 Check that the filename, printed in the terminal, matches the acquisition type of the scan displayed in ITK-SNAP. If they match, simply press enter. Otherwise enter the correct filename and press enter. This feature is intended to be useful for filenames that contain the acquisition type in the filename (e.g. BIDS format filenames).
 
 **Note:** entering a corrected file name will not change the name of the original file. The value you enter will simply appear in the final output files with the ratings.
 
 ```
File: example_FLAIR.nii

Press enter for a correctly labelled file (T1,T2, FLAIR).
Otherwise type the correct label:
 ```
 
### 6. Entering an overall image quality rating 
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


### 7. Ending the session 
The session will end automatically when all files are reviewed, to end early input ctrl + C. A .json and .csv file will be automatically created when the session is ended, they will appear in the 'mri_rating_record' folder 

```
Two files generated (.csv, .json): MRI_rating_record/MRIrate_session-29-06-2022_16:34:19
```
