# MRI Quality Assement (MRIqa) Tool 
The MRIqa rating tool allows users to iterate through nifti files based on filename criterias and provide a numerical rating to describe the scan quality.

**Features:**
- *Ongoing reviews*: previous rating sessions can be resumed to prevent duplicate ratings 
- *Database options*: option to store rating sessions in a local json file or using mongodb
- *Multiple raters*: resuming a previous session only reviews images that are yet to have a rating for the user or have already been reviewed 3 times 

# Downloads 
### [Python installation](mriqa/docs/python.md)
Python 3.x is required to run the script successfully, details on how to install python can be found in the link above.

### Github download

Download script files in the terminal opened at a chosen file storage location.

```
#clone the repository to your local computer
git clone https://github.com/mollyic/MRI_qa.git
```

## Scan viewer

ITK-SNAP, fsleyes or MRview are compatible with the script, only one viewer is required to run the script. They can be downloaded using the links below. 

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
pip install pymongo getpass4 python-dotenv

#pip3 install 
pip3 install pymongo getpass4 python-dotenv
```



# Optional: MongoDB database

By default the script will save files to a .json file and. However there is the option to store the files using MongoDB. Before running the script, you will need to set the MongoDB credentials in the settings.env file in the mriqa/env/ folder. The file should look like this:

```
MONGO_DB_USRNAME=<username>
MONGO_DB_PW=<password>
```
Replace <username> and <password> with the appropriate values for your MongoDB instance.


# Usage 
To run the script, open a terminal or command prompt in the directory where the files are stored run the main script from the terminal.

    
```
python3 MRIqa_tool.py
```
   
**Note:** if this is the first time running the rating tool, a directory will be created titled 'ratingDB'. The .json files containing your ratings will be stored here. 


## MongoDB usage 

If you wish to run the script using MongoDB the argument '-db' should be entered on the command line.

```
python3 MRIqa_tool.py -db
```


# Reviewing

Follow the prompts to begin a new session or resume a previous session. 

```
 Resume a previous session? 
1 - New session
2 - Resume previous sessions
 ``` 
**Note:** Resuming a previous session will prompt you to select the session to resume as shown below, enter the number corresponding to the session and press enter. 
 
 ```

1. MRIrate_session-03-08-2021_162134
2. MRIrate_session-06-08-2021_150826
3. MRIrate_session-09-08-2021_190512
Enter session number to resume: 

 ```

**Note:** do not close your scan viewer, after your review has been entered the current image will be closed and the next image to be reviewed will automatically be opened

## Review parameters 

Upon beginning a review session you will be prompted to set your review parameters:
    1. Input file location 
    2. Search parameters (e.g. modality-wise)
    3. Nifti file viewer choice

These settings will be stored for your next review session. You will have the option to change preset parameters each time you begin a review. 
 
## Reviewing overall image quality rating 
During all review sessions you will enter a numerical score between 1-5 for the image quality as is displayed below.
 
 ```
 Enter overall image quality rating:
1. Very Poor    2. Suboptimal   3. Acceptable   4. Above Average    5. Excellent

Rating (1 to 5): 
 ```

### Optional: Reviewing artifacts
There is an option to review artifacts (Motion, susceptibilty, ghosting/flow). This required the '-a' argument to be supplied when running the main script. 

```
python3 MRIqa_tool.py -a
```


## Ending the session 
The session will end automatically when all files are reviewed, to end early input ctrl + C. Your reviews will be saved to the existing or new .json file appear in the 'reviweDB' folder 

