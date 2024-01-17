# Run MRIqa Tool 
To run the script, open a terminal or command prompt in the directory where the files are stored run the main script from the terminal. By default results will be stored to a .json file, to use a MongoDB database follow [these instructions](##running-mriqa-tool-with-mongodb).


## First Run
An output directory containing the rating results and a work directory containing the config file will be created. It is possible to specify the location of these output folders in the terminal.

Details about the arguments can be found in the [MRIqa arguments section](mriqa/docs/arguments_dict.md) or by using the *help* argument.

```
python3 mriqa.py --help
```

### Mandatory arguments
- bids_dir: The root folder of a BIDS valid dataset
- viewer: Select nifti scan viewer(itksnap/mrview/fsleyes)

### Recommended arguments
- review_id: user inputted string used to name the review session (date and time automatically appended)
- sub_id: space-delimited subject IDs 
- modalities: space-delimited modalities e.g. T2map (Default: T1w  T2map  FLAIR and T2w)

### Importing subject IDs from a text file
To import a text file of subject IDs as the input to the --sub_id argument. In the terminal window where you plan to run the main MRIqa script, enter the following bash commands.

```
#Create SUB_FILE variable in your terminal that contains the file name
SUB_FILE=/path/to/text_file/mriqa_subjects.txt

#Create variable (SUBS) that contains text file contents (skipping header line and using space delimiter)
mapfile -d ' ' -t SUBS < <(tail -n +2 $SUB_FILE)

#Check the variable contains the subject IDs
echo ${SUBS[@]}
```

### Run MRIqa
```
#Option 1: run using only mandatory arguments
python3 mriqa.py --bids_dir path/to/bids/files --viewer itksnap 

#Option 2: run using recommended arguments
python3 mriqa.py --bids_dir path/to/bids/files --viewer itksnap --review_id group_review --sub-id 1000 2000

#Option 3: run using recommended arguments and importing subjects from text file
python3 mriqa.py --bids_dir path/to/bids/files --viewer itksnap --review_id group_review --sub-id ${SUBS[@]}
```

Skip to the [MRIqa tool interface section](#mriqa-tool-interface) if your settings are properly configured.

**Note**: When you first use the script a config file will be created in the work directory (*mriqa_config.toml*) saving the review session search parameters.

## Resuming a session
### Continue with review settings
Having previously run a session, there is no need to specify any arguments if you wish to continue with the same review sessions with the same search parameters.

```
python3 mriqa.py
```

### Update review settings
If you are resuming a session and wish to change the review parameters, the value you wish to change should be entered at in the terminal. Any arguments you do not change will be sourced from the config file. 

All possible arguments can be found be found in the [MRIqa arguments section](mriqa/docs/arguments_dict.md) or by using the *help* argument.

```
#Change BIDS modality 
python3 mriqa.py -m T1w FLAIR
```

Your previous reviews will appear in terminal, enter the index of the session to resume. 
 
 ```
1. MRIrate_session-03-08-2021_162134
2. MRIrate_session-06-08-2021_150826
3. MRIrate_session-09-08-2021_190512
Enter session number to resume: 
```

## Force new session
To start a new session when previous ratings exist the *'-new'* argument should be entered in the command line. This will recreate the config file from scratch meaning the mandatory arguments of *'bids_dir'* and *'viewer'* must be entered.

```
python3 mriqa.py --bids_dir path/to/bids/files --viewer itksnap -new
```



# *Optional:* Reviewing artifacts
Option to choose whether to review artifact types in the session enter, default is no artifacts review.
```
#Review artifacts
python3 mriqa.py -a

#Disable review of artifacts
python3 mriqa.py -na
```


# *Optional:* Running MRIqa tool with MongoDB
To save the ratings results to a MongoDB database include the argument *mongodb* in the terminal. Note there is no communication between the MongoDB database files and the local json files.

Ensure you have setup the settings.env file using [these instructions](mriqa/docs/databases.md).

```
python3 mriqa.py --bids_dir path/to/bids/files --viewer itksnap --review_id group_review --mongodb
```


## Changing databases
Change between database types using the arguments below. Note the default is .json, the *json* argument should only be used when switching back from MongoDB.
```
#change to MongoDB database
python3 mriqa.py --mongodb
#revert to json database
python3 mriqa.py --json


```
**Note:** there is no interaction between MongoDB databases and local .json files, changing to a new database will not import the reviews from the previous database


# MRIqa tool interface

For each scan the viewer will open and you will be prompted to enter a review scores. 

**Note:** Do not close your scan viewer during the review session, after your review has been entered the current image will be closed and the next image will open automatically

### Reviewing overall image quality rating 
During all review sessions a numerical score between 1-5 for each scan is required.
 
 ```
Rate overall image quality rating.
    *Image: sub-0000_FLAIR.nii.gz


1- Unusable      2 - Suboptimal      3 - Acceptable       4 - Above Average     5 - Excellent

Enter rating (1 to 5): 
```

### Optional: Reviewing artifacts
If you chose to review artifacts during the session, you will be prompted to enter a score for 3 argument types. 

```
Rate SUSCEPTIBILITY severity.
    *Image: sub-0000_FLAIR.nii.gz


1 - Severe       2 - Moderately Severe       3 - Moderate        4 - Mild        5 - None

Enter rating (1 to 5): 
```

**Note**: You can skip reviewing particular artifacts by hitting enter instead of a numerical score.

### Ending the session 
The session will end automatically when all files are reviewed, to end early input ctrl + C. 

Eeviews will be saved to the .json file or MongoDB database. Results from the MongoDB database will be automatically downloaded as a .json file with the prefix 'mongodb-import'


### Optional: convert database to csv file
Enter the --csv option in the terminal to convert a chosen data base to a csv files. Note the databases presented will be contingent on the chosen database type i.e. if MongoDB is the setting in the config file only MongoDB databases will be displayed. Entering the database terminal argument will change which ratings sessions are shown (e.g. python mriqa.py --csv --json)

```
1. MRIqa_study1_20231123_13:11:14.json
3. MRIqa_IQM_audit_20231127_16:29:52.json

Enter session number: 1

--------------------------------------------------
Converted .json to .csv:
     * MRIqa_study1_20231123_13:11:14.json
--------------------------------------------------
```


