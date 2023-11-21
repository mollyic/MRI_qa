from mriqa import config 
import os 
import re 

def _parse_id_strings(value):
    """
    Parse white space separated input id strings, dropping sub- prefix of participant labels

    """
    return sorted(set(re.sub(r"^sub-", "", item.strip()) for item in re.split(r"\s+", f"{value}".strip())))



def consoleOptions():
    from argparse import ArgumentParser
    from pathlib import Path
    from functools import partial
    from argparse import Action
    
    parser = ArgumentParser(
        description=f"""MRIqa tool! 
                        Tool to review nifti scans. Most settings are configured during execution. \
                        Optional configurations can be selected via command line arguments below.""")

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
                        required=False,
                        type=PathExists,
                        help="The root folder of a BIDS valid dataset")
    
    parser.add_argument('--mongodb', '-db',
                        action='store_true', 
                        help="Choice to use MongoDB instance to store output results.")
     
    parser.add_argument('--artifacts', '-a',
                        action='store_true', 
                        help="Choice to review artifacts.")
    
    parser.add_argument("--output_dir",
                        action="store",
                        default=Path("output").absolute(),
                        type=Path,
                        help="The directory where the output files should be stored."
                        )
    
    parser.add_argument("-w", "--work-dir",
                        action="store",
                        type=Path,
                        default=Path("work").absolute(),
                        help="Path where config files should be stored."
                        )  
      
    parser.add_argument("--db_settings",
                        action="store",
                        type=Path,
                        default=Path(f"mriqa/environ/settings.env").absolute(),
                        help="Path where login settings for mongoDB database are stored."
                        ) 

    parser.add_argument("-m","--modalities",
                        action="store",
                        choices=config.MODALITIES,
                        default=config.MODALITIES,
                        nargs="*",
                        help="Filter input dataset by MRI type.")
    
    parser.add_argument("--viewer",
                        action="store",
                        choices=config.VIEWERS,
                        help="Select nifti scan viewer")

    parser.add_argument('--new_review', '-new',
                        dest="_new_review",
                        action='store_true', 
                        help="Choice to start new review session.")
        
    parser.add_argument("--review_id",
                        action="store",
                        type=str,
                        help="String for naming output files and config file"
                        )
    
    parser.add_argument("--session","-s",
                        action="store",
                        dest="session",
                        nargs="*",
                        type=str,
                        help="Filter input dataset by session ID.")
    
    parser.add_argument("--participant_label", "-p",
                        dest="participant_label",
                        action=LabelAction,
                        nargs="+",
                        help="A space delimited list of participant identifiers or a single identifier (the sub- prefix can be removed).")

    parser.add_argument("--file_id",
                        "-id",
                        action=LabelAction,
                        nargs="*",
                        help="A space delimited list of strings used to identify relevant files."
                        )
    parser.add_argument( "-v","--verbose",
        dest="_log_level",
        action="store",
        default=int(20),
        choices=config.LOG_LVL,
        help="Increases log verbosity, threshold by information severity: CRITICAL = 50, ERROR = 40,\
            WARNING = 30, INFO: 20, DEBUG: 10"    )
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
        
        console_input = {key:args_dict[key] for key in args_dict if parser.get_default(key) is None if args_dict[key] is not None}
        console_default = {key:args_dict[key] for key in args_dict if parser.get_default(key) is not None if args_dict[key] != parser.get_default(key)}
        update_dict = {**console_input, **console_default}

        for key, val in update_dict.items():
            toml_dict["session"].update({key: val})
        config.ConsoleToConfig(toml_dict['session'])
    else: 
        missing = [key for key in ['viewer', 'bids_dir'] if not args_dict[key] if args_dict[key] is None]
        if missing:
            raise ValueError(messages.NO_INDIR.format(missing = missing))       
        config.ConsoleToConfig(args_dict)

    output_dir = config.session.output_dir
    work_dir = config.session.work_dir

    output_dir.mkdir(exist_ok=True, parents=True)
    work_dir.mkdir(exist_ok=True, parents=True)
    
    # Force initialization of the BIDSLayout
    config.session.init()

    participant_label = config.session.layout.get_subjects()
    if config.session.participant_label is not None:
        selected_label = set(config.session.participant_label)
        missing_subjects = selected_label - set(participant_label)
        if missing_subjects:
                print("One or more participant labels were not found in the BIDS directory: "
                f"{', '.join(missing_subjects)}.")

        participant_label = selected_label

    config.session.participant_label = sorted(participant_label)

    # List of files to be run
    bids_filters = {
        "participant_label": config.session.participant_label,
        "session": config.session.session,
        "bids_type": config.session.modalities,
        "file_id": config.session.file_id}

    config.session.inputs = collect_files(config.session.layout, **bids_filters)

