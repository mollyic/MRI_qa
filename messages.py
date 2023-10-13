"""
All questions available in script for easy formatting
"""

VIEWERS = ['itksnap', 'mrview', 'fsleyes'] 
MSGS = {
    'session':"\033c\n1 - New session \n2 - Resume previous sessions: continue reviewing files\n",
    'viewer':"Enter image viewer index:\n1 - ITK-SNAP\n2 - MRView\n3 - FSLeyes\n",
    'location':"Folders to review:\n1 - ANAT folder\n2 - All folders\n\n", 
    'choice_note':("Results will be filtered by both folder and file choice.").upper(), 
    'end':'\nAll files matching criteria reviewed\n\n+----------------------------+\n\nSession Ended\n\n+----------------------------+'
}
