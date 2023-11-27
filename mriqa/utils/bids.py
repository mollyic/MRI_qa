

def collect_files(layout, bids_type, sub_id=None,session=None,file_id=None):
    from bids.utils import listify
    import re
    """Get files in dataset"""

    basequery = {
        "subject": sub_id,
        "session": session,
        "datatype": "anat",
        "return_type": "file",
        "suffix": listify(bids_type),
        "extension": ["nii", "nii.gz"],
    }

    # Filter empty lists, strings, zero runs, and Nones
    basequery = {k: v for k, v in basequery.items() if v}
    
    bids_data = layout.get(**basequery)
    imaging_data = [file for file in bids_data if all(re.search(pattern, file) for pattern in file_id)] if file_id else bids_data    
    
    #Check subdirectories if no nifti
    if not imaging_data: 
        import os
        from mriqa import config, messages
        import glob
        import random
        
        parent_dir = config.session.bids_dir 

        folds = [os.path.join(layout.root, fold) for fold in os.listdir(layout.root) if glob.glob(f'{layout.root}/{fold}/**/*.nii*', recursive=True)]
        config.loggers.cli.log(30, f"\n No BIDS directories found in {config.session.bids_dir}.\n  * Search sub-directories:\n\n{folds}")

        check_subdirs = input("\nProceed? (enter else any key to quit)")
        if len(check_subdirs.lower()) >=1:
            config.loggers.cli.log(30, f'\n{messages.BREAK}\nExiting, no BIDS directories found.\n{messages.BREAK}\n')
            quit()
            
        for fold in folds:
           config.session._layout = None     
           config.session.bids_dir = fold
           config.session.init()
           bids_data = config.session.layout.get(**basequery)
           imaging_data += [file for file in bids_data if all(re.search(pattern, file) for pattern in file_id)] if file_id else bids_data
        
        random.shuffle(imaging_data)
        config.session.bids_dir = parent_dir


    return imaging_data