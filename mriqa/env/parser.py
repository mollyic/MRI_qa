from mriqa import config 
import os 
import re 
from argparse import HelpFormatter, ArgumentParser, Action

def _parse_id_strings(value):
    """
    Parse white space separated input id strings, dropping sub- prefix 
    """
    return sorted(set(re.sub(r"^sub-", "", item.strip()) for item in re.split(r"\s+", f"{value}".strip())))


class SmartFormatter(HelpFormatter):
    """
    Custom argparse formatter
    """
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()  
        return HelpFormatter._split_lines(self, text, width)
                        


def consoleOptions():
    from pathlib import Path
    from functools import partial
    
    parser = ArgumentParser(formatter_class=lambda prog: SmartFormatter(prog, max_help_position=4, indent_increment =1), 
                            description="MRIqa tool!\n  Tool to review nifti scans.\n Search parameters for BIDS files can be set using terminal arguments.", )

    class LabelAction(Action):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, _parse_id_strings(" ".join(values)))

    def _path_exists(val, parser): 
        pathway=Path(val).absolute()
        if pathway is None or not Path(pathway).exists():
            raise parser.error(f"Path does not exist: <{pathway}>.")
        return pathway

    PathExists = partial(_path_exists, parser=parser)

    parser.add_argument("--bids_dir","-d",
                        action="store",
                        type=PathExists,
                        help="R| * The root folder of a BIDS valid dataset.\n ")
    

    parser.add_argument("--viewer",
                        action="store",
                        choices=config.VIEWERS,
                        help="R| * Select nifti scan viewer.\n ")

    parser.add_argument("--file_id",
                        "-id",
                        action=LabelAction,
                        nargs="*",
                        help="R| FILE SEARCH PARAMETER:                                     Space delimited list of strings to specify input files.\n "
                        )

    parser.add_argument("-m","--modalities",
                        action="store",
                        choices=config.MODALITIES,
                        default=config.MODALITIES,
                        nargs="*",
                        help="R| * FILE SEARCH PARAMETER:                                     Filter input dataset by MRI type.\n ")    
    
    parser.add_argument("-ses",
                        action="store",
                        dest="session",
                        nargs="*",
                        type=str,
                        help="R| * FILE SEARCH PARAMETER:                                     Filter input dataset by session ID.\n ")
    
    parser.add_argument("--sub_id", "-s",
                        dest="sub_id",
                        action=LabelAction,
                        nargs="+",
                        help="R| * FILE SEARCH PARAMETER:                                     Space delimited list of subject ids or a single id.\n ")

    parser.add_argument("--output_dir",
                        action="store",
                        default=Path("output").absolute(),
                        type=Path,
                        help="R| * The directory where the output files should be stored.\n "
                        )
    
    parser.add_argument("-w", "--work_dir",
                        action="store",
                        type=Path,
                        default=Path("work").absolute(),
                        help="R| * Path where config files should be stored.\n "
                        )  

    parser.add_argument("--review_id",
                        action="store",
                        type=str,
                        help="R| * String for naming output files and config file.\n "
                        )
    
    parser.add_argument('--mongodb', '-db',
                        default=None,
                        action='store_true', 
                        help="R| * Use MongoDB instance to store output results.\n ")
    
    parser.add_argument('--json', '-j',
                        dest="mongodb",
                        action='store_false', 
                        help="R| * Disable mongodb and default to json file database.\n ")     
    
    parser.add_argument('--artifacts', '-a',
                        action='store_true', 
                        default=None,
                        help="R| * Review artifacts.\n ")
    
    parser.add_argument('--no_artifact', '-na',
                        dest="artifacts",
                        action='store_false', 
                        help="R| * Disable artifacts if previously selected in config.\n ")     
      
    parser.add_argument("--db_settings",
                        action="store",
                        type=Path,
                        default=Path(f"mriqa/env/settings.env").absolute(),
                        help="R| * Path where login settings for mongoDB database are stored.\n "
                        ) 

    parser.add_argument('--comment', '-c',
                        action='store_true', 
                        default=None,
                        help="R| * Add comment field during review.\n ")
    
    parser.add_argument('--no_comment', '-nc',
                        dest="comment",
                        action='store_false', 
                        help="R| * Disable comments if previously selected in config.\n ")     


    parser.add_argument('--new_review', '-new',
                        dest="_new_review",
                        action='store_true', 
                        help="R| * Start new review session.\n ")

    parser.add_argument("--user",
                        action="store",
                        type=str,
                        help="R| * Set username for troubleshooting (default is the system username).\n ")    
    
    parser.add_argument("--csv",
                        dest="_csv_out",
                        action="store_true",
                        #default=False,
                        help="R| * Convert database to csv file.\n ")    

    return parser

     
def parse_console(args=None, namespace=None):
    """
    Extract arguments from terminal
    """
    from mriqa.utils import collect_files
    from mriqa.config import load_toml
    from mriqa import messages
    
    parser = consoleOptions()
    args = parser.parse_args(args, namespace)
    args_dict = vars(args)
    config_file = config.session.config_file

    #Check if any argument was provided that differs from the default
    if os.path.exists(config_file) and not args_dict['_new_review']:
        toml_dict = load_toml(config_file)
        bool_args= ['mongodb', 'artifacts', 'comment']
        user_inputs = {key: args_dict[key] for key in args_dict if key not in bool_args if args_dict[key] != parser.get_default(key)}
        for key, val in user_inputs.items():
            toml_dict["session"].update({key: val})
        
        for key in bool_args:
            if isinstance(args_dict[key], bool):
                toml_dict["session"].update({key: args_dict[key]})
        config.ConsoleToConfig(toml_dict['session'])
    else: 
        missing = [key for key in ['viewer', 'bids_dir'] if not args_dict[key] if args_dict[key] is None]
        if missing:
            raise ValueError(messages.NO_INDIR.format(missing = missing))       
        config.ConsoleToConfig(args_dict)


    output_dir = config.session.output_dir
    work_dir = config.session.work_dir
    config.session.log_dir = output_dir / "logs"

    config.session.log_dir.mkdir(exist_ok=True, parents=True)
    output_dir.mkdir(exist_ok=True, parents=True)
    work_dir.mkdir(exist_ok=True, parents=True)
    
    # Force initialization of the BIDSLayout
    config.session.init()

    sub_id = config.session.layout.get_subjects()
    if config.session.sub_id is not None:
        selected_label = set(config.session.sub_id)
        missing_subjects = selected_label - set(sub_id)
        if missing_subjects:
                print("One or more subject identifiers were not found in the BIDS directory: "
                f"{', '.join(missing_subjects)}.")

        sub_id = selected_label

    config.session.sub_id = sorted(sub_id)

    # List of files to be run
    bids_filters = {
        "sub_id": config.session.sub_id,
        "session": config.session.session,
        "bids_type": config.session.modalities,
        "file_id": config.session.file_id}

    print('\n\nCSV status:')
    print(config.session._csv_out)
    if not config.session._csv_out:
        config.session.inputs = collect_files(config.session.layout, **bids_filters)

