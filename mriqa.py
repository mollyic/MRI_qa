from mriqa import messages
from mriqa import config
from mriqa.env import parse_console
from subprocess import run, check_output, Popen, DEVNULL, STDOUT
import json 
from os.path import basename as bn
from mriqa.utils import import_mongo

from signal import signal
from signal import SIGTERM, SIGKILL,SIGINT
from multiprocessing import Process, active_children
import sys

import psutil
import os
import time
import re
import pyautogui
# def handler(sig, frame):
#     """
#     Child processes respond to requiest to terrminate by terminating their child processes
#         - child process registers a function to respond to SIGTERM function
#         - Within function child process can see it's active children
#     """

#     # get all active child processes
#     #active_kids = active_children()

#     # terminate all active children
#     for child in active_children():
#         child.terminate()
#         #child.join()
#     # terminate the process
#     sys.exit(0)

 
# # function executed in a child process
# def task2(viewer, file):
#     subprocess.Popen([viewer, file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

# # function executed in a child process
# def task(viewer, file):

#     # handle sigterm
#     #signal(SIGTERM, handler)
#     # start another child process
#     #child_process =Process(target=task2, args=[viewer, file])
#     subprocess.Popen([viewer, file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
#     # block for a while
#     #child_process.start()
#     # block task until child_process completes, if necessary
#     #child_process.join()  # This line ensures that task waits for task2 to complete



# def task(viewer, file, db):
#     # Run the viewer in a subprocess, redirecting stdout and stderr to /dev/null
#     process = subprocess.Popen([viewer, file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
#     # After viewer is closed, call the review function

#     sys.stdin = open(0)
#     db.review(file)

#     process.terminate()  # SIGTERM
#     try:
#         process.wait(timeout=0.5)  # Adjust the timeout as needed
#     except subprocess.TimeoutExpired:
#         process.kill()  # SIGKILL


def main():
    from mriqa.utils import reviewer, kill_process, convert_csv

    parse_console()
    config.loggers.init()


    config.to_filename(config.session.config_file)
    config.load(config.session.config_file)

    viewer = config.session.viewer
    output_dir = config.session.output_dir
    files = config.session.inputs
    user = config.session.user
    start_message = messages.START.format(
        bids_dir=config.session.bids_dir,
        output_dir=output_dir,
        viewer=viewer,
        user=user)

    for k,v in messages.SEARCH_BIDS.items():
        if config.session.__dict__[v] is not None:
            start_message += (f'       * {k}: {config.session.__dict__[v]}\n')
            

    config.loggers.cli.log(20, msg = start_message)
    
        

    """Instantiate either dict object or mongodb database to store ratings"""
    config.collector.func_finder()      
    db = reviewer()
    user_exit = False

    if not config.session._csv_out:
        try: 
            for file in files:                        
                if not db.check(img = bn(file)):
                    continue

                #Popen.close
                #subprocess.Popen([viewer, file])#, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                # try:
                #     outs, errs = proc.communicate(timeout=0.5)
                #     os.kill(proc.pid, SIGTERM)
                # except subprocess.TimeoutExpired:
                #     #proc.kill()
                #     os.kill(proc.pid, SIGKILL)
                #     outs, errs = proc.communicate()


                #ORIGINAL
                process = Popen([viewer, file], stdout=DEVNULL, stderr=STDOUT, start_new_session=True) #, preexec_fn=os.setsid) #, start_new_session=True)
                config.session._pid = process.pid
                #os.setpgid(process.pid, process.pid)  # Set the PGID of the process to its own PID
                print(f'\nProcess PID: {process.pid}\n')
                db.review(file)
                pgrp = os.getpgid(process.pid)
                os.killpg(pgrp, SIGINT)
                
                #os.kill(int(process.pid), SIGTERM) #
                #result = run(["xdotool", "search", "--name", "ITK-SNAP"])
                #print(f'\nxdotool: {result}\n')

                #window_id = result.stdout.split()[0]
                #run(["xdotool", "windowactivate", window_id])
                #run(["xdotool", "key", "ctrl+q"])
                #pyautogui.hotkey('ctrl', 'Q')
                #kill_process(viewer)

                #Session ID
                #process = subprocess.Popen([viewer, file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, preexec_fn=os.setsid) #, start_new_session=True)
                # sid = os.getsid(process.pid)
                #subprocess.check_call(['pkill', '-s', str(sid)])

                #ALT kills
                #kill_process_and_children(process.pid)
                #kill_processes_by_attributes('itksnap')


                #MULTIPROC
                # p = Process(target=task, args=(viewer, file, db))
                # #p.daemon=True
                # p.start()
                # p.join()  # Wait for the process to complete
                # p.terminate()  # SIGTERM
                # p.kill()

                #TMUX
                # tmux_ses = bn(file).split('.')[0]
                # print(f'\n\nTmux session: {tmux_ses}')
                # #create tmux session
                # run(['tmux', 'new-session', '-d', '-s', tmux_ses])
                # print(f'Session started')

                # #tmux_command = f"tmux send-keys -t {tmux_ses} '{viewer} {file} & echo ITKSNAP PID $!' C-m"
                # #subprocess.run(tmux_command, shell=True)
                
                # #FILE TEST
                # tmux_command = f"tmux send-keys -t {tmux_ses} './run_viewer.sh {file} & echo ITKSNAP PID $!' C-m"
                # run(tmux_command, shell=True)

                # time.sleep(0.5)
                # tmux_capture_pane = f"tmux  capture-pane -p -t {tmux_ses}"
                # tmux_cmd = check_output(tmux_capture_pane, shell=True).decode('utf-8')
                # print(f'\n\nTmux out: {tmux_cmd}')

                
                # pids = re.findall(r"ITKSNAP PID (\d+)", tmux_cmd)

                # print(f'\n\nTmux itksnap pids: {pids}')
                # print(f'Tmux itksnap pid: {pids[-1]}')

                # db.review(file)
                # #CONTROL C
                # run(['tmux', 'send-keys', '-t', tmux_ses, 'C-q'])
                # #pkill
                # #run(['tmux', 'send-keys', '-t', tmux_ses, f'pkill -f {viewer}', 'C-m'])
                # #PID
                # #os.kill((pids[-1]), SIGTERM)

                # run(['tmux', 'send-keys', '-t', tmux_ses, 'echo Die you bastard', 'C-m'])


                # print(f'\n\nTmux out:')
                # print(check_output(tmux_capture_pane, shell=True).decode('utf-8'))
                # run(['tmux', 'kill-session', '-t', tmux_ses])


                # time.sleep(0.5)


        except KeyboardInterrupt:
            user_exit = True
            #run(['tmux', 'kill-session', '-t', tmux_ses])
            config.loggers.cli.log(20, messages.USR_END.format(filename = db.filename))
            pass 

        if not user_exit:
            config.loggers.cli.log(20, messages.END.format(filename = db.filename))

        if db.max_reviews or db.rater_reviewed:
            config.loggers.cli.log(20, messages.REVIEWED.format(user = user,
                                                                max_reviewed = db.max_reviews, 
                                                                user_reviewed = db.rater_reviewed))

        if not config.session.mongodb:
            with open(db.filename, "w") as f:
                json.dump(db.db, f, indent = 4, separators=(',', ': '))

        else:
            import_mongo(db.db, output_dir, db.filename)

    else:
        convert_csv(db.filename, db.new_db)

if __name__ == "__main__":
    main()

