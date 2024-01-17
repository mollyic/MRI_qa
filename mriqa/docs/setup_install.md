# Setup and installation for MRIqa tool

## Downloads 
#### [Python installation](./python.md)
Python 3.x is required to run the script, details on how to install python can be found in the hyperlinked title.

#### Github download

Download script files in the terminal opened at a chosen file storage location.

```
#clone the repository to your local computer
git clone https://github.com/mollyic/MRI_qa.git
```

#### Scan viewer download

ITK-SNAP, fsleyes or MRview are compatible with the script, only one viewer is required.

1. ITK-SNAP: http://www.itksnap.org/pmwiki/pmwiki.php?n=Documentation.TutorialSectionInstallation
2. fsleyes: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation
3. MRview: https://mrtrix.readthedocs.io/en/3.0_rc3/installation/linux_install.html

**Note**: ITK-SNAP is the preferred viewer as, relative to the other applications, it responds the mostly rapidly within the script.


## Setup
Required packages can be installed using a virtual environment, conda, with the provided .yml file, or via a local pip install.

#### virtual environment install 

**Recommended:** A virtual environment helps to manage software versions and ensures they remain compatible with the rating tool. 

```
#pip install virtual environment
pip install virtualenv

#create environment selecting python version 3 or later
virtualenv -p /usr/bin/python3 mriqa_tool

#activate the virtual environment
source mriqa_tool/bin/activate

#download python packages to virtual environment
pip install pymongo getpass4 python-dotenv bids toml nibabel
```

#### conda install 

**Recommended:** A conda environment helps to manage software versions and ensures they remain compatible with the rating tool. Details on installing conda can be found at https://www.anaconda.com/download. Having downloaded conda, run the following code.

```
#create environment with conda
conda env create -f MRIqa_conda.yml

#activate the conda environment
conda activate mriqa_tool
```


### local pip install 
To simply install packages locally run the following command in the terminal.

```
#pip install
pip install pymongo getpass4 python-dotenv bids toml nibabel
```
