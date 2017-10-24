#!/usr/bin/python


import argparse                   # Argument parser
import datetime                   # For current Date/Time
import time
import os.path                    # To check if file exists
import sys                        # For args
import re                         # For regex
import paramiko                   # For remote ssh
import yaml
import warnings

from esxi_vm_functions import *

#      Defaults and Variable setup
ConfigData = setup_config()
NAME = ""
LOG = ConfigData['LOG']
isDryRun = ConfigData['isDryRun']
isVerbose = ConfigData['isVerbose']
isSummary = ConfigData['isSummary']
HOST = ConfigData['HOST']
USER = ConfigData['USER']
PASSWORD = ConfigData['PASSWORD']
CPU = ConfigData['CPU']
MEM = ConfigData['MEM']
HDISK = int(ConfigData['HDISK'])
DISKFORMAT = ConfigData['DISKFORMAT']
VIRTDEV = ConfigData['VIRTDEV']
STORE = ConfigData['STORE']
NET = ConfigData['NET']
ISO = ConfigData['ISO']
GUESTOS = ConfigData['GUESTOS']

ErrorMessages = ""
CheckHasErrors = False
DSPATH=""
DSSTORE=""

#
#      Process Arguments
#
parser = argparse.ArgumentParser(description='ESXi Create VM utility.')

parser.add_argument("-H", "--Host", dest='HOST', type=str, help="ESXi Host/IP  (" + str(HOST) + ")")
parser.add_argument("-U", "--User", dest='USER', type=str, help="ESXi Host username  (" + str(USER) + ")")
parser.add_argument("-P", "--Password", dest='PASSWORD', type=str, help="ESXi Host password  (*****)")
parser.add_argument("-n", "--name", dest='NAME', type=str, help="VM name")
parser.add_argument('-V', '--verbose', dest='isVerbosearg', action='store_true', help="Enable Verbose mode  (" + str(isVerbose) + ")")
parser.add_argument('--summary', dest='isSummaryarg', action='store_true', help="Display Summary  (" + str(isSummary) + ")")


args = parser.parse_args()

if args.isVerbosearg:
    isVerbose = True
if args.isSummaryarg:
    isSummary = True
if args.HOST:
   HOST=args.HOST
if args.USER:
    USER=args.USER
if args.PASSWORD:
    PASSWORD=args.PASSWORD
if args.NAME:
    NAME=args.NAME

#
#      main()
#
LogOutput = '{'
LogOutput += '"datetime":"' + str(theCurrDateTime()) + '",'

if NAME == "":
    print "ERROR: Missing required option --name"
    sys.exit(1)

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PASSWORD)

    (stdin, stdout, stderr) = ssh.exec_command("esxcli system version get |grep Version")
    type(stdin)
    if re.match("Version", str(stdout.readlines())) is not None:
        print "Unable to determine if this is a ESXi Host: %s, username: %s" % (HOST, USER)
        sys.exit(1)
except:
    print "The Error is " + str(sys.exc_info()[0])
    print "Unable to access ESXi Host: %s, username: %s" % (HOST, USER)
    sys.exit(1)

#
#      Check if VM exists
#
VMID = -1
try:
    (stdin, stdout, stderr) = ssh.exec_command("vim-cmd vmsvc/getallvms")
    type(stdin)
    for line in stdout.readlines():
        splitLine = line.split()
        if NAME == splitLine[1]:
            VMID = splitLine[0]
            JNK = line.split('[')[1]
            STORE = JNK.split(']')[0]
            VMDIR = splitLine[3]

    if VMID == -1:
        print "Warning: VM " + NAME + " doesn't exists."
        ErrorMessages += " VM " + NAME + " doesn't exists."
        CheckHasErrors = True
        CheckHasWarnings = True
except:
        print "The Error is " + str(sys.exc_info()[0])
        sys.exit(1)

#  Get List of Volumes, 
try:
    (stdin, stdout, stderr) = ssh.exec_command("esxcli storage filesystem list |grep '/vmfs/volumes/.*true  VMFS' |sort -nk7")
    type(stdin)
    VOLUMES = {}
    for line in stdout.readlines():
        splitLine = line.split()
        VOLUMES[splitLine[0]] = splitLine[1]
except:
    print "The Error is " + str(sys.exc_info()[0])
    sys.exit(1)


#  Convert STORE to path and visa-versa
V = []
for Path in VOLUMES:
    V.append(VOLUMES[Path])
    if STORE == Path or STORE == VOLUMES[Path]:
        DSPATH = Path
        DSSTORE = VOLUMES[Path]


if CheckHasErrors:
    Result = "Errors"
else:
    Result = "Success"

if not CheckHasErrors:
    try:

        CurrentState = ""
        CurrentStateCounter = 0
        while CurrentState != "off":
            if isVerbose:
                print "Get state VM"
            (stdin, stdout, stderr) = ssh.exec_command("vim-cmd vmsvc/power.getstate " + str(VMID))
            type(stdin)
            lines = str(stdout.readlines()) + str(stderr.readlines())
            if isVerbose:
                print "power.getstate: " + lines
            if re.search("Powered off", lines):
                CurrentState = "off"

            # Power off VM
            if isVerbose:
                print "Power OFF VM"
            (stdin, stdout, stderr) = ssh.exec_command("vim-cmd vmsvc/power.off " + str(VMID) + " ||echo")
            type(stdin)
            lines = str(stdout.readlines()) + str(stderr.readlines())
            if isVerbose:
                print "power.off: " + str(lines)

            CurrentStateCounter += 1
            if CurrentStateCounter >10:
                break
            time.sleep(1)

        # destroy VM
        if isVerbose:
            print "Destroy VM"
        (stdin, stdout, stderr) = ssh.exec_command("vim-cmd vmsvc/destroy " + str(VMID))
        type(stdin)
        lines = str(stdout.readlines()) + str(stderr.readlines())
        if isVerbose:
            print "destroy: " + str(lines)

    except:
        print "There was an error destroying the VM."
        ErrorMessages += " There was an error destroying the VM."
        CheckHasErrors = True
        Result = "Fail"

#      Print Summary

#
#   The output log string
LogOutput += '"Host":"' + HOST + '",'
LogOutput += '"Name":"' + NAME + '",'
LogOutput += '"Store Used":"' + DSPATH + '",'
LogOutput += '"Verbose":"' + str(isVerbose) + '",'
if ErrorMessages != "":
    LogOutput += '"Error Message":"' + ErrorMessages + '",'
LogOutput += '"Result":"' + Result + '",'
LogOutput += '"Completion Time":"' + str(theCurrDateTime()) + '"'
LogOutput += '}\n'
try:
    with open(LOG, "a+w") as FD:
        FD.write(LogOutput)
except:
    print "Error writing to log file: " + LOG

if isSummary:
    if isVerbose:
        print "ESXi Host: " + HOST
    print "VM NAME: " + NAME
    print "Path: " + DSSTORE 
else:
    pass

if CheckHasErrors and not CheckHasWarnings:
    print "Failed"
    sys.exit(1)
else:
    print "Success"
    sys.exit(0)


