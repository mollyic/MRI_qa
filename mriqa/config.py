from pathlib import Path
from configparser import ConfigParser as cp
from datetime import datetime
import getpass
import os
import logging

MODALITIES = ("T1w", "T2w", "FLAIR", 'T2map')
VIEWERS = ('itksnap', 'mrview', 'fsleyes') 
ARTIFACTS = ['susceptibility', 'motion', 'flow_ghosting']


class _Config:
    """"
    Config manager
    - update and retrieve values from config file 
    """
    

    def __init__(self):
        raise RuntimeError("Config class not for instantiation")
    
    @classmethod    #class method: associated with class not instance; access class via cls to modify attributes 
    def load(cls, settings):
        """
        Update the object with parsed arguments
        """
        for key,val in settings.items():                #settings are inputted arguments
            if val is None:               
                continue
            if key in cls._paths:
                setattr(cls, key, Path(val).absolute())
                continue
            if hasattr(cls,key):                            #if the class has the attribute sets the value
                setattr(cls, key, val)                  
        try:
            cls.init()
        except AttributeError:
            pass

    @classmethod
    def get(cls):
        """Return defined settings."""
        out = {}
        for k, v in cls.__dict__.items():
            if k.startswith("_") or v is None:
                continue
            if callable(getattr(cls, k)):
                continue
            if k in cls._paths:
                v = str(v)
            out[k] = v
        return out
   
    @classmethod    #class method: associated with class not instance; access class via cls to modify attributes 
    def func_finder(cls):
        from mriqa.utils import _MongoDB, _JsonDB
        
        """
        Update the functions depending on the db instance
        """
        if session.mongodb:
            db_class = _MongoDB
        else:
            db_class = _JsonDB

        setattr(cls, '_db', db_class._db)                  
        setattr(cls, '_review', db_class._review)                  
        setattr(cls, '_check', db_class._check)                   
        try:
            cls.init()
        except AttributeError:
            pass
    
class session(_Config):
    user = getpass.getuser()
    """Rater name to be stored"""

    bids_dir = None
    """An existing path to the dataset, which must be BIDS-compliant."""
    output_dir = None
    """Path to output files"""
    work_dir = Path("work").absolute()
    """Path to a working directory where intermediate results will be available."""
    log_dir=None
    mongodb = False
    """Optional use of mongodb"""
    db_settings = Path(f"mriqa/env/settings.env").absolute()
    """MongoDB login settings file"""
    viewer= None
    """Nifti file viewer"""
    _new_review = False
    """Start a new review session"""
    artifacts= False
    """Boolean: option to review artifacts or not"""
    comment= False
    """Option to add comment field entry during review"""
    review_id = f"{user}"
    """Identifying string for the review session config and output files"""
    inputs = None
    """List of files to be viewed with mriqa."""
    config_file = os.path.join(work_dir, 'mriqa_config.toml')
    """
    Bids search parameters
    """
    modalities = None
    """Filter input dataset by MRI type."""
    sub_id = None
    """List of subject ids that are to be preprocessed."""  
    file_id = None
    """Filter input dataset by string """
    session = None
    """Filter input dataset by session identifier."""
    _csv_out = None
    """Option to output csv file"""

    _pid = None
    _layout = None
    _paths = ("bids_dir","output_dir","work_dir", 'config_file', "log_dir", 'db_settings')
    @classmethod
    def init(cls):
        """Create a new BIDS Layout accessible with :attr:`~session.layout`."""
        if cls._layout is None:
            import re
            from bids.layout.index import BIDSLayoutIndexer
            from bids.layout import BIDSLayout

            ignore_paths = [
                # Ignore folders at the top if they don't start with /sub-<label>/ and 2nd folder isn't anat
                re.compile(r"^(?!/sub-[a-zA-Z0-9]+)"),
                # Ignore all files, except for the supported modalities
                re.compile(r"^.+(?<!(_T1w|_T2w|LAIR|2map))\.(json|nii|nii\.gz)$"),]

            if cls.sub_id:
                # If we know participant labels, ignore all other
                ignore_paths[0] = re.compile(r"^(?!/sub-("+ "|".join(cls.sub_id)+ r"))")

            _indexer = BIDSLayoutIndexer(validate=False,ignore=ignore_paths)
            cls._layout = BIDSLayout(str(cls.bids_dir),indexer=_indexer)

        cls.layout = cls._layout

class collector(_Config):
    #set functions here 
    _db = None
    _check = None
    _review = None

class loggers:
    cli = logging.getLogger("cli")
    log_time = datetime.now().strftime("%Y%m%d_%H%M%S")


    @classmethod
    def init(cls):
        """Command-line interface logging."""

        _log_file = f"{session.log_dir}/review-{session.review_id}_{cls.log_time}.log"
        _formatter = logging.Formatter('%(message)s')

        if not cls.cli.handlers:
            cls.cli.setLevel(logging.DEBUG)
            # console handler 
            console_handler = logging.StreamHandler()       #send the LogRecord to the required output destination
            console_handler.setLevel(logging.INFO)         #set log level           
            console_handler.setFormatter(_formatter)    #set format of log 

            #log file handler 
            file_handler = logging.FileHandler(_log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(_formatter)

            # add handlers to logger
            cls.cli.addHandler(console_handler)
            cls.cli.addHandler(file_handler)
    
    @classmethod
    def getLogger(cls, name):
        """Create a new logger with class and."""
        return getattr(cls, name)

def ConsoleToConfig(settings):
    """Update the config file with inputted arguments """
    session.load(settings)


class UserDict(cp):        #inherits from ConfigParser/ subclass of ConfigParser
    def dictverter(self):
        ini_dict=dict(self._sections)
        for key in ini_dict:
            ini_dict = dict(self._defaults, **ini_dict[key])
        return ini_dict


def dumps():
    """Format config into toml."""
    from toml import dumps
    
    return dumps({"session": session.get()})

def to_filename(filename):
    """Write settings to file."""
    filename = Path(filename)
    filename.parent.mkdir(exist_ok=True, parents=True)
    filename.write_text(dumps())

def load_toml(filename):
    """Load settings from a TOML file"""
    from toml import loads
    return loads(Path(filename).read_text())

def load(filename):
    """Load settings from file."""
    import sys
    settings = load_toml(filename)
    for sectionname, configs in settings.items():
        section = getattr(sys.modules[__name__], sectionname)
        section.load(configs)