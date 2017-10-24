import os.path
import yaml
import datetime                   # For current Date/Time
import paramiko                   # For remote ssh
from math import log


#
#
#   Functions
#
#


def setup_config():

    #
    #   System wide defaults
    #
    ConfigData = dict(

        #   Your logfile
        LOG= os.path.expanduser("~") + "/esxi-vm.log",

        #  Enable/Disable dryrun by default
        isDryRun=False,

        #  Enable/Disable Verbose output by default
        isVerbose=False,

        #  Enable/Disable exit summary by default
        isSummary=False,

        #  ESXi host/IP, root login & password
        HOST="esxi",
        USER="root",
        PASSWORD="",

        #  Default number of vCPU's, GB Mem, & GB boot disk
        CPU=2,
        MEM=4,
        HDISK=20,

        #  Default Disk format thin, zeroedthick, eagerzeroedthick
        DISKFORMAT="thin",

        #  Virtual Disk device type
        VIRTDEV="pvscsi",

        #  Specify default Disk store to "LeastUsed"
        STORE="LeastUsed",

        #  Default Network Interface (vswitch)
        NET="None",

        #  Default ISO
        ISO="None",

        #  Default GuestOS type.  (See VMware documentation for all available options)
        GUESTOS="centos-64",

        # Extra VMX options
        VMXOPTS=""
    )

    ConfigDataFileLocation = os.path.expanduser("~") + "/.esxi-vm.yml"

    #
    # Get ConfigData from ConfigDataFile, then merge.
    #
    if os.path.exists(ConfigDataFileLocation):
        FromFileConfigData = yaml.safe_load(open(ConfigDataFileLocation))
        ConfigData.update(FromFileConfigData)

    try:
        with open(ConfigDataFileLocation, 'w') as FD:
            yaml.dump(ConfigData, FD, default_flow_style=False)
        FD.close()
    except:
        print "Unable to create/update config file " + ConfigDataFileLocation
        e = sys.exc_info()[0]
        print "The Error is " + str(e)
        sys.exit(1)
    return ConfigData

def SaveConfig(ConfigData):
    ConfigDataFileLocation = os.path.expanduser("~") + "/.esxi-vm.yml"
    try:
        with open(ConfigDataFileLocation, 'w') as FD:
            yaml.dump(ConfigData, FD, default_flow_style=False)
        FD.close()
    except:
        print "Unable to create/update config file " + ConfigDataFileLocation
        e = sys.exc_info()[0]
        print "The Error is " + str(e)
        return 1
    return 0


def theCurrDateTime():
    i = datetime.datetime.now()
    return str(i.isoformat())


unit_list = zip(['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'], [0, 0, 1, 2, 2, 2])
def float2human(num):
    """Integer to Human readable"""
    if num > 1:
        exponent = min(int(log(float(num), 1024)), len(unit_list) - 1)
        quotient = float(num) / 1024**exponent
        unit, num_decimals = unit_list[exponent]
        format_string = '{:.%sf} {}' % (num_decimals)
        return format_string.format(quotient, unit)
    if num == 0:
        return '0 bytes'
    if num == 1:
        return '1 byte'
