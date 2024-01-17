# Setup and installation for MRIqa tool

## Databases
The MRIqa rating tool allows users to select between saving their rating scores to a local json file or to a MongoDB database.

By default the script will save files to a .json file in the output directory. output/ is the default directory unless specified using the argument --output_dir. 


### MongoDB
Using a MongoDB database relies on settings.env file in the mriqa/env/ folder. When you first run the script you will be prompted to enter a username, password and host address which will be stored in the mriqa/env/settings.env file.

```
MONGODB_USRNAME=<username>
MONGODB_PW=<password>
MONGODB_HOST=<password>
```

When running the main script you will be required to enter an argument to specify the use of the MongoDB database. These instructions can be found on the [Run MRIqa tool page](mriqa/docs/run_mriqa_tool.md) under the run with MongoDB database.

**Note:** if no value is input for <MONGODB_HOST>, the default value of 'localhost' will be used.
