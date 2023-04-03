# MRI Image Quality Assement Tool 
The simple MRI rating tool allows users to open MRI images in nifti format (nii.gz, nii) and provide a numerical rating that describes the impact of artifact on the image quality. It is possible to resume previous rating sessions using the tool. If a previous rating session is selected, only images that are yet to have a rating will be opened for review.

# Installations 

Here are the steps to install Python and add it to your system's PATH:

    Go to the official Python website at https://www.python.org/downloads/.
    Click on the "Download" button for the latest version of Python.
    Choose the appropriate installer for your system. For Windows, choose the "Windows x86-64 executable installer" if you have a 64-bit system, or the "Windows x86 executable installer" if you have a 32-bit system. For macOS, choose the "macOS 64-bit installer" for the latest version of Python.
    Run the installer and follow the prompts to complete the installation process. When asked, make sure to select the option to "Add Python to PATH" so that Python can be easily accessed from the command prompt.
    Once the installation is complete, open a new command prompt (Windows) or terminal (macOS/Linux) and type "python" to confirm that Python is installed and running. You should see the Python version number and a command prompt (">>>").

That's it! You now have Python installed on your system and can start using it to run scripts and applications.

# install Python and add it to your path on Linux:

    Open a terminal window on your Linux system.

    Update the package index:

    sql

sudo apt update

Install Python by running the following command:

sudo apt install python3

This will install Python 3.x version. If you want to install Python 2.x version, you can run the following command:

sudo apt install python

Verify that Python has been installed correctly by running the following command:

css

python3 --version

This should display the version of Python installed on your system.

Next, you need to add Python to your PATH. This will allow you to run Python commands from anywhere on your system.

Open the ~/.bashrc file in a text editor:

bash

nano ~/.bashrc

Add the following line to the end of the file:

ruby

export PATH=$PATH:/usr/bin/python3

This line adds the Python executable to your PATH.

Save the changes and exit the editor by pressing Ctrl+X, followed by Y and Enter.

Finally, reload the bashrc file for the changes to take effect:

bash

    source ~/.bashrc

That's it! Python is now installed on your Linux system and added to your PATH. You can test it by opening a new terminal window and running the following command:

python3

This should open the Python interpreter.

# Setup

To use this script, you will need to have Python 3.x installed, along with the required packages. These packages are pymongo, configparser, getpass, subprocess, datetime, re, and dotenv. The instructions below will walk you through the installation process and how to run the script.
Install Python 3.x

If you don't already have Python installed, you will need to install it first. You can download the latest version of Python from the official website: https://www.python.org/downloads/.

Once you've downloaded the installer for your operating system, run it and follow the prompts to install Python.
Install required packages

After installing Python, you will need to install the required packages for the script to run. You can do this by opening a terminal or command prompt and running the following command:

pip install pymongo configparser getpass subprocess datetime re python-dotenv

This will install all the necessary packages.
Run the script

To run the script, you will need to have the necessary files. These files are:

    mri_rater.py
    mriqa_marker_objects_20230130.py
    rating_config.ini
    settings.env

Place all these files in the same directory.

Before running the script, you will need to set the MongoDB credentials in the settings.env file. The file should look like this:

makefile

MONGO_DB_USRNAME=<username>
MONGO_DB_PW=<password>

Replace <username> and <password> with the appropriate values for your MongoDB instance.

To run the script, open a terminal or command prompt and navigate to the directory where the files are stored. Then run the following command:

python mri_rater.py

This will start the script. Follow the prompts to begin a new session or resume a previous session. You can review all files or a single subject, and you can set the search parameters and review parameters in the rating_config.ini file.

Note that the script requires a scan viewer to be installed on your system. You can set the path to the scan viewer in the rating_config.ini file.

 
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

```
Directory 'MRI_rating_record' created! Your ratings will be stored here.
```

### 2. Enter the session type 
 Enter the number corresponding to the session you wish to select.
 
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

### 7. Rating artifacts 
Enter the letter corresponding to the artifact you wish to rate (upper and lower case accepted). It is possible to rate all, some or none of the artifacts. Simply press enter to proceed from this menu.
 
 ```
 Enter letter to rate artifact or hit enter to continue. 

M - MOTION 
S - SUSCEPTIBILITY
F - FLOW/GHOSTING


Artifact: 
```

You will then be prompted to enter your rating for the artifact type. Once your rating is entered you will be returned to the artifact selection menu. The next image will be automatically opened once all artifact ratings are provided. 
 
 ```
Artifact: f
1 - Severe, 2 - Moderately Severe, 3 - Moderate, 4 - Mild, 5 - None
Rating: 3
```

### 8. Ending the session 
The session will end automatically when all files are reviewed, to end early input ctrl + C. A .json and .csv file will be automatically created when the session is ended, they will appear in the 'mri_rating_record' folder 

```
Two files generated (.csv, .json): MRI_rating_record/MRIrate_session-29-06-2022_16:34:19
```
