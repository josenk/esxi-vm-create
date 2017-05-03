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
        LOG="~/esxi-vm.log",
        isDryRun=False,
        isVerbose=False,
        HOST="esxi",
        USER="root",
        PASSWORD="",
        CPU=2,
        MEM=4,
        SIZE=20,
        DISKFORMAT="thin",
        VIRTDEV="pvscsi",
        STORE="LeastUsed",
        NET="None",
        ISO="None",
        GUESTOS="centos-64"
    )

    ConfigDataFileLocation = os.path.expanduser("~") + "/.esxi-vm.yml"

    #
    # Get ConfigData from ConfigDataFile, then merge.
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

