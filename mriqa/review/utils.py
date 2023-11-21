import signal
from mriqa.messages import INPUT_ERR, PICK_SCORE
import os



def verify_input( question ='', forced = False, n = 5, select = PICK_SCORE, err = INPUT_ERR):
    if type(n) == list:
        if len(n) == 1: 
            forced = True
        n = len(n)

    while True:
        print(question)
        answer = input(select)
        if forced:
            answer = 1
            break
        if answer.isdigit(): 
            if int(answer) in range(1, n + 1):
                break
        print(err)
    return int(answer)

def kill_process(viewer):
    """
    Kill image viewer following review
    """    
    viewer = 'itk-snap' if viewer == 'itksnap' else viewer
    
    for line in os.popen(f"ps ax | grep -i {viewer} | grep -v grep"):   # view the open applications with 'ps ax'
        pid = line.split()[0]                                           #process ID is the first column (0), isolate this item
        os.kill(int(pid), signal.SIGKILL)                               #kill process with PID, sigkill() terminates program
