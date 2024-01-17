# MRI Quality Assement (MRIqa) Tool 
The MRIqa rating tool allows users to iterate through nifti files based on filename criterias and provide a numerical rating to describe the scan quality.

**Features:**
- *Ongoing reviews*: previous rating sessions can be resumed to prevent duplicate ratings 
- *Database options*: option to store rating sessions in a local json file or using MongoDB
- *Multiple raters*: resuming a previous session only reviews images that are yet to have a rating for the user or have already been reviewed 3 times 


## [Setup and installation for MRIqa tool](mriqa/docs/setup_install.md)
Setup environment and download necessary packages to run the tool 
## [Running the MRIqa tool](mriqa/docs/run_mriqa_tool.md)
Run and configure to tool to review scans
## [Selecting the correct database](mriqa/docs/databases.md)
Configure the chosen database (MongoDB or local json file)
## [View MRIqa tool argument dictionary](mriqa/docs/arguments_dict.md)
See all possible configuration arguments for the tool