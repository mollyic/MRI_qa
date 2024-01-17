# MRIqa arguments dictionary

## Mandatory arguments

1. **BIDS directory**: The root folder of a BIDS valid dataset.
```
python3 mriqa.py --bids_dir path/to/bids/files
python3 mriqa.py -d path/to/bids/files
```
2. **Scan viewer**: Select nifti scan viewer (itksnap,mrview,fsleyes)
```
python3 mriqa.py --viewer fsleyes
```

### BIDS database search
Filtering of input files is possible with the use of 4 terminal arguments. By default mriqa will only search for structural T1w, T2w and FLAIR scans in the 'anat' folder.


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

**Note:** these filters are additive, meaning any file not meeting one of these criteria will be excluded

If no BIDS directories are found in the provided folder, a prompt to check the subdirectories will appear. 


```
 No BIDS directories found in path/to/parent/folder
  * Search sub-directories:

['path/to/parent/folder/bids_project1', 'path/to/parent/folder/bids_project2']

Proceed? (enter)

```

## Execution 

1. **Review ID**: String for naming output files and config file.
```
python3 mriqa.py ---review_id test_review
```
2. **Output directory**: The directory where the output files should be stored.
```
python3 mriqa.py --output_dir path/to/store/results
```
3. **Work directory**: Path where config files should be stored.
```
python3 mriqa.py --work_dir path/to/store/config/file
python3 mriqa.py -w path/to/store/config/file
```
4. **MongoDB database**: Use MongoDB instance to store output results.
```
python3 mriqa.py --mongodb
python3 mriqa.py -db

```
5. **MongoDB settings**: Path where login settings for mongoDB database are stored.
```
python3 mriqa.py --db_settings path/to/store/settings/file
```
6. **Json database**: Disable mongodb and default to json file database. Only necessary when session previously configured with MongoDB database.
```
python3 mriqa.py --json
python3 mriqa.py -j
```
7. **Convert to .csv**: Convert database to csv file.
```
python3 mriqa.py --csv
```

## Session 

1. **Start new review**: Clear the contents of the config file and start a new review session. Mandatory arguments will be required
```
python3 mriqa.py --bids_dir path/to/bids/files --viewer itksnap --new_review
python3 mriqa.py --bids_dir path/to/bids/files --viewer itksnap -new
```
2. **User**: Set username for troubleshooting (default is the system username).
```
python3 mriqa.py --user test_user
```
3. **Review artifacts**: Review artifacts during session
```
python3 mriqa.py --artifacts
python3 mriqa.py -a

```
3. **Disable artifacts**: Disable artifacts if previously selected in config.
```
python3 mriqa.py --no_artifact
python3 mriqa.py -na

```
