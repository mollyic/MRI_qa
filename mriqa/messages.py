
"""
INPUT BIDS DIRECTORY MESSAGES:
    - messages concern identifying the files to be reviewed
"""
#Start message when review sesssion begins
START = """

MRIqa tool: input files will be filtered by search parameters.

    * Dataset: {bids_dir}
    * Output folder: {output_dir}.
    * Viewer: {viewer}
    * Review session ID: {review_id}

    Search parameters:     
"""

#Possible search parameters for BIDS folder search
SEARCH_BIDS = {'Session':'session', 'Modalities':'modalities', 
               'Participant label':'participant_label', 'Search string':'file_id'}

#Missing terminal inputs (required: bids_dir, viewer)
NO_INDIR = """

Missing mandatory argument: {missing}.
    * Values can be entered at the command line
    
    """

MAX_RATED = """

Images previously reviewed 3 times:
{img_list}

"""
RATER_RATED = """
{username} has already reviewed images:
{img_list}

"""

"""
FORMATTING MESSAGES
    - Strings for formatting script run
"""
#Formatting break string
BREAK=    "--------------------------------------------------"

#End message
END = f'\n{BREAK}\nSession Ended: all files matching criteria reviewed{BREAK}'


REVIEW_FILE = """{output_dir}/{review_id}"""


"""
REVIEW SESSION MESSAGES:
    - Messages for review inputs
"""

#Message when invalid integer entry during rating 
INPUT_ERR = f"\n{BREAK}\nInvalid entry, enter a number from 1-5"

#Overall rating score key
SCORES = '1- Unusable      2 - Suboptimal      3 - Acceptable       4 - Above Average     5 - Excellent\n'

#Artifact rating score key
ART_SCORES = '1 - Severe       2 - Moderately Severe       3 - Moderate        4 - Mild        5 - None\n'

#Message for possible rating score
PICK_SCORE ="Enter rating (1 to 5): "



