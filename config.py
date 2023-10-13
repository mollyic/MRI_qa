from pathlib import Path
from configparser import ConfigParser as cp
import getpass
from datetime import datetime
import re
import os 

ERR_STRING = "Invalid entry, enter a number from 1-5\n--------------------------------------"


class _Config:
    """"
    Config manager
    - update and retrieve values from config file 
    """
    

    def __init__(self):
        raise RuntimeError("Config class not for instantiation")
    
    @classmethod    #class method: associated with class not instance; access class via cls to modify attributes 
    def load(cls, settings, init =True):
        """
        Update the object with parsed arguments
        """
        _pivotalPaths = ("output_dir", "input_images")
        for key,val in settings.items():                #settings are inputted arguments
            if val is None:               
                continue
            if key in _pivotalPaths:                #known paths set to posix Path
                setattr(cls, key, Path(val).absolute())   #set the named attribute of object to the value
            if hasattr(cls,key):                        #if the class has the attribute sets the value
                setattr(cls, key, val)                  
        if init:
            try:
                cls.init()
            except AttributeError:
                pass
    
    @classmethod 
    def get(cls):
        """
        Retrieve
        """
        out = {}
        for key,val in cls.__dict__.items():
            if val:     
                continue
            if key in cls._pivotalPaths:
                val = str(val)                          #convert path to string
            out[key] = val
        return out
    
class session(_Config):
    """Setting instantiated settings"""
    user = getpass.getuser()
    """Session details"""
    time_str = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")     
    """Date for naming csv or database"""
    output_dir = Path("ratingDB").absolute()
    """Path to outputed files"""
    user_env = Path(f"environ/user.ini").absolute()
    """ini file with session specific values"""
    db_settings = Path(f"environ/settings.env").absolute()
    

class preferences(_Config):
    """Rater name to be stored"""
    string = None
    """Regex string for finding files"""
    viewer= None
    """Nifti file viewer"""
    input_images = None
    """Nifti file location"""
    mongodb = False
    """Optional use of mongodb"""
    artifacts= False
    """Boolean: option to review artifacts or not"""
    seshid = None
    """Identifying string for the review session"""
    re_params = None
    """Regex string to find files"""
    input_params = None
    """Regex string to find files"""

def ConsoleToConfig(settings):
    """
    Update the config file with inputted arguments 
    """
    session.load(settings)
    preferences.load(settings)

class UserDict(cp):        #inherits from ConfigParser: subclass of ConfigParser
    def dictverter(self):
        ini_dict=dict(self._sections)
        for key in ini_dict:
            ini_dict = dict(self._defaults, **ini_dict[key])
        return ini_dict
