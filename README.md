# MRI Quality Assement (MRIqa) Tool 
The MRIqa rating tool allows users to iterate through nifti files based on filename criterias and provide a numerical rating to describe the scan quality.

**Features:**
- *Ongoing reviews*: previous rating sessions can be resumed to prevent duplicate ratings 
- *Database options*: option to store rating sessions in a local json file or using MongoDB
- *Multiple raters*: resuming a previous session only reviews images that are yet to have a rating for the user or have already been reviewed 3 times 

# Downloads 
### [Python installation](mriqa/docs/python.md)
Python 3.x is required to run the script, details on how to install python can be found in the hyperlinked title.

### Github download

Download script files in the terminal opened at a chosen file storage location.

```
#clone the repository to your local computer
git clone https://github.com/mollyic/MRI_qa.git
```

### Scan viewer

ITK-SNAP, fsleyes or MRview are compatible with the script, only one viewer is required.

1. ITK-SNAP: http://www.itksnap.org/pmwiki/pmwiki.php?n=Documentation.TutorialSectionInstallation
2. fsleyes: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation
3. MRview: https://mrtrix.readthedocs.io/en/3.0_rc3/installation/linux_install.html

**Note**: ITK-SNAP is the preferred viewer as, relative to the other applications, it responds the mostly rapidly within the script.


# Setup
Required packages can be installed using conda, with the provided .yml file, or via pip install.

### conda install 

**Recommended:** A conda environment helps to manage software versions and ensures they remain compatible with the rating tool. Details on installing conda can be found at https://www.anaconda.com/download. Having downloaded conda, run the following code.

```
#create environment with conda
conda env create -f MRIqa_conda.yml

#activate the conda environment
conda activate mriqa_tool
```

### pip install 
Alternatively packages can be installed in your local environment using pip.

```
#pip install
pip install pymongo getpass4 python-dotenv bids toml
```


# Databases

### .json file

By default the script will save files to a .json file in the output directory. output/ is the default directory unless specified using the argument --output_dir. 


### MongoDB
Using a MongoDB database relies on settings.env file in the mriqa/env/ folder. When you first run the script you will be prompted to enter a username, password and host address which will be stored in the mriqa/env/settings.env file.

```
MONGODB_USRNAME=<username>
MONGODB_PW=<password>
MONGODB_HOST=<password>
```

**Note:** if no value is input for <MONGODB_HOST>, the default value of 'localhost' will be used.

# Usage 

### Run
To run the script, open a terminal or command prompt in the directory where the files are stored run the main script from the terminal. By default the database is a local .json file in the output folder and its name will be augmented by the --review_id argument if it is provided.
- bids_dir: path to scans for review
- viewer: scan viewer software (itksnap/mrview/fsleyes)
- review_id (*OPTIONAL*): user inputted string used to name the review session 
- artifacts (*OPTIONAL*): option to review artifacts seperately to the overall rating (motion, susceptibility, ghosting/flow)
- mongodb (*OPTIONAL*): option to store reviews in a MongoDB database

```
python3 mriqa.py --bids_dir path/to/bids/files --viewer itksnap --review_id group_review --artifacts
#Run using MongoDB database
python3 mriqa.py --bids_dir path/to/bids/files --viewer itksnap --review_id group_review --artifacts --mongodb
```

**Note:** if this is the first time running the rating tool, an output directory containing the rating results and a work directory containing the config file will be created.


### BIDS database search
Filtering of input files is possible with the use of 4 terminal arguments. By default mriqa will only search for structural T1w, T2w and FLAIR scans in the 'anat' folder

1. **File id**: Filter input dataset by string using a space delimited list
```
python3 mriqa.py --file_id preproc
python3 mriqa.py -id preproc grappa
```
2. **Modality**: Filter input dataset by modality using a space delimited list
```
python3 mriqa.py --modalities T1w
python3 mriqa.py -m T1w FLAIR
```
3. **Session**: Filter input dataset by session ID using a space delimited list
```
python3 mriqa.py -ses 01 02
```
4. **Subject ID**: Filter input dataset by subject ID using a space delimited list
```
python3 mriqa.py --sub_id 1005
python3 mriqa.py --s 1005 4005
```  

**Note:** these filters are additive meaning any file not meeting one of these criteria will be excluded


### User config file
When you first use the script a config file will be created in the work directory (*mriqa_config.toml*) saving the review session search parameters. These settings will be loaded automatically when you run the script again. If you are resuming a session and wish to change the review parameters, the value you wish to change should be entered at in the terminal 

- **Changing settings**: changing search parameters, directory paths or string identifier in config file
```
python3 mriqa.py --bids_dir <path/to/bids/files> --file_id lowres --viewer mrview
``` 
- **Changing database**: changing the database settings in config file
```
#change to MongoDB database
python3 mriqa.py --mongodb
#revert to json database
python3 mriqa.py --json
```
- **Reviewing artifacts**: changing the artifact review settings in config file
```
#Review artifacts
python3 mriqa.py -a

#Disable review of artifacts
python3 mriqa.py -na
```

**Note:** there is no interaction between MongoDB databases and local .json files, changing to a new database will not import the reviews from the previous database


### Resume session

If there are review files in the output directory or in your MongoDB database, select the session to resume entering the corresponding number. 
 
 ```
1. MRIrate_session-03-08-2021_162134
2. MRIrate_session-06-08-2021_150826
3. MRIrate_session-09-08-2021_190512
Enter session number to resume: 
```

### Force new session

To start a new session when previous ratings exist the *'-new'* argument should be entered in the command line. This will recreate the config file from scratch meaning the mandatory arguments of *'bids_dir'* and *'viewer'* must be entered.

```
python3 mriqa.py --bids_dir path/to/bids/files --viewer itksnap -new
```

# Interface

### Reviewing overall image quality rating 
During all review sessions a numerical score between 1-5 for each scan is required.
 
 ```
Rate overall image quality rating.
    *Image: sub-0000_FLAIR.nii.gz


1- Unusable      2 - Suboptimal      3 - Acceptable       4 - Above Average     5 - Excellent

Enter rating (1 to 5): 
```

### Optional: Reviewing artifacts
If the -a argument is provided a numerical score between 1-5 for each artifact type is required.

```
Rate SUSCEPTIBILITY severity.
    *Image: sub-0000_FLAIR.nii.gz


1 - Severe       2 - Moderately Severe       3 - Moderate        4 - Mild        5 - None

Enter rating (1 to 5): 
```

**Note:** do not close your scan viewer, after your review has been entered the current image will be closed and the next image will open automatically

### Ending the session 
The session will end automatically when all files are reviewed, to end early input ctrl + C. Your reviews will be saved to the .json file or MongoDB database. Results from the MongoDB database will be automatically downloaded as a .json file with the prefix 'mongodb-import'

