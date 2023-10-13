
import config 
import os 
import re 

ERR_STRING = "Invalid entry, enter a number from 1-5\n--------------------------------------"

def consoleOptions():
    from argparse import ArgumentParser
    from pathlib import Path
    parser = ArgumentParser(
        description=f"""MRIqa tool! 
                        Tool to review nifti scans. Most settings are configured during execution. \
                        Optional configurations can be selected via command line arguments below.""")
    
    def AbsPath(val): 
        pathway=Path(val).absolute()
        if not os.path.exists(pathway) and not os.path.isdir(pathway):
            print(f'\n\nPath: {pathway}\nThe path provided does not contain any output files.\n\n')
            raise ()
        return pathway
    #local
    parser.add_argument('--mongodb', '-db',
                        action='store_true', 
                        required=False) 
    #review artifacts
    parser.add_argument('--artifacts', '-a',
                        action='store_true', 
                        required=False) 
    parser.add_argument('--output_dir', '-o', type=AbsPath,
                        action='store', 
                        required=False) 
    return parser


def parse_console(args=None, namespace=None):
    parser = consoleOptions()
    args = parser.parse_args(args, namespace)
    config.ConsoleToConfig(vars(args))

def parse_usrenv():
    usr_env = config.UserDict()
    usr_env.read(config.session.user_env)
    config_dict = usr_env.dictverter()
    config.ConsoleToConfig(config_dict)

    print(f'\nArtifacts: {config.preferences.artifacts}')
    print(f'mongodb: {config.preferences.mongodb}')
    print(f'output_dir: {config.session.output_dir}')
    print(f'input_images: {config.preferences.input_images}')
    print(f're_params: {config.preferences.re_params}')
    print(f'input_params: {config.preferences.input_params}')
    print(f'viewer: {config.preferences.viewer}')
    print(f'seshid: {config.preferences.seshid}')

