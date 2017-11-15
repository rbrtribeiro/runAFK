import subprocess
import sys
import time
from time import sleep

#usage: nohup python runAFK.py <minutes in idle> <full command string> &
#command output will in cwd, file command<timeid>.log


def kill(ps):        
    print "Killing process " + str(ps.pid)
    ps.terminate()
    ps.kill()
    ps.communicate()


def run(command): 
    outputFile = "command" + str(int(round(time.time() * 1000))) + ".log"
    command = str(command).split()
    with open(outputFile, 'w') as output_f:
        ps = subprocess.Popen(command, stdout=output_f,stderr=output_f)
    return ps


def getIdleTimeSec():
    ps = subprocess.Popen(["xprintidle"], stdout=subprocess.PIPE , stderr=subprocess.PIPE)
    idletime = long(ps.communicate()[0])/1000 
    return idletime


idleThresholdMinutes = float(sys.argv[1])
command = sys.argv[2]

try:
    running = False
    while True:
        idleTime = getIdleTimeSec()
        if idleTime > idleThresholdMinutes*60:
            if not running:
                ps = run(command)
                print "Running command, PID: " + str(ps.pid)
                running = True
        else:
            if running:
                kill(ps)
                running = False
        sleep(3)
finally:
    if running: kill(ps)
    print "Gracefull exit"
    

