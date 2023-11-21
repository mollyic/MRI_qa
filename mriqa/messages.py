
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
END = f'\n\n{BREAK}\nSession Ended: all files matching criteria reviewed\n{BREAK}\n\nRating database updated\n\n'


REVIEW_FILE = """{output_dir}/MRIqa_{review_id}_{date}"""


"""
REVIEW SESSION MESSAGES:
    - Messages for review inputs
"""

#Messages when invalid integer entry
RATE_ERR = f"\n{BREAK}\nInvalid entry, enter a number from 1-5"
SES_ERR = "Invalid session, try again:\n"

#Overall rating score key

OVERALL_MSG= BREAK + "\n\nRate overall image quality rating.\n    *Image: {img}"
SCORES = """

1- Unusable      2 - Suboptimal      3 - Acceptable       4 - Above Average     5 - Excellent\n"""

#Artifact rating score key

ART_MSG = BREAK +'\n\nRate {artifact} severity.\n    *Image: {img}'
ART_SCORES = """

1 - Severe       2 - Moderately Severe       3 - Moderate        4 - Mild        5 - None\n"""

#Message for possible rating score
PICK_SCORE ="Enter rating (1 to 5): "
PICK_SES ="Enter session number to resume: "

