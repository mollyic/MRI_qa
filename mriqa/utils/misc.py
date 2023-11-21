import signal
from mriqa import messages, config
import os

def verify_input(sessions = None, n = 5, msg=None, score= None):

    msg = msg if not sessions else sessions
    score = score if not sessions else ''
    error = messages.RATE_ERR if not sessions else messages.SES_ERR
    choice = messages.PICK_SCORE if not sessions else messages.PICK_SES

    while True:
        config.loggers.cli.log(30,  msg)
        config.loggers.cli.log(30,  score)

        answer = input(choice)
        if answer.isdigit(): 
            if int(answer) in range(1, n + 1):
                break
        config.loggers.cli.log(30, error)
    return int(answer)

def kill_process(viewer):
    """
    Kill image viewer following review
    """    
    viewer = 'itk-snap' if viewer == 'itksnap' else viewer
    
    for line in os.popen(f"ps ax | grep -i {viewer} | grep -v grep"):   # view the open applications with 'ps ax'
        pid = line.split()[0]                                           #process ID is the first column (0), isolate this item
        os.kill(int(pid), signal.SIGKILL)                               #kill process with PID, sigkill() terminates program
