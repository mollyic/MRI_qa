

def collect_files(layout,bids_type,sub_id=None,session=None,file_id=None):
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
    
    return imaging_data