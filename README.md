Introduction
------------

  This utility is a simple to use comand line tool to create VMs on an ESXi host from from a system running python and ssh.  vCenter is not required.  This tool is an easy way to automate building VM's from command line or from other testing or automation tools such as Bamboo, Puppet, Saltstack, or Chef.


Usage
-----

  Get help using --help option.   The defaults will be displayed in the help output.

  The only command line required paramater is the VM name (-n), all other command line arguments are optional.


  Defaults are stored in your home directory in ~/.esxi-vm.yml.   You can edit this file directly, or you can use the tool to update most the defaults by specifying --updateDefaults.

  One of the first settings to set and save as defaults is the --Host (-H), --User (-U) and --Password (-P).

  Some basic sanity checks are done on the ESXi host before creating the VM.  The --verbose (-V) option will give you a little more details in the creation process.  If an invalid Disk Stores or Network Interface is specified, the available devices will be shown in the error message. The tool will not show the list of available ISO images, and Guest OS types.  CPU, Memory, Virtual Disk sizes are based on ESXi 6.0 limitations.

  The --dry (-d) option will go through the sanity checks, but will not create the VM.  

  By default the Disk Store is set to "LeastUsed".  This will use the Disk Store with the most free space (in bytes).

  By default the ISO is set to "None".  Specify the full path to the ISO image.   If you specify just the ISO image filename (no path), the system will attempt to find the ISO image on your DataStores.

  By default the Network set set to "None". A full or partial MAC address can be specified. A partial MAC address argument would be 3 Hex pairs which would then be prepended by VMware's OEM "00:50:56".

  By default the VM is powered on. If an ISO was specified, then it will boot the ISO image.  Otherwise, the VM will attempt a PXE boot if a Network Interface was specified.  You could customize the ISO image to specify the kickstart file, or PXE boot using COBBLER, Foreman, Razor, or your favorite provisioning tool. 

  To help with automated provisioning, the script will output the full MAC address and exit code 0 on success.  You can specify --summary to get a more detailed summary of the VM that was created.


Requirements
------------

  You must enable ssh access on your ESXi server.   The VMware VIX API tools are not required.

  It's HIGHLY RECOMMENDED to use password-less authentication by copying your ssh public keys to the ESXi host, otherwise your ESXi root password could be stored in clear-text in your home directory.

  Python and paramiko is a software requirement.
  
```
yum -y install python python-paramiko
```


Command Line Args
-----------------

```
./esxi-vm-create --help
usage: esxi-vm-create [-h] [-d] [-H HOST] [-U USER] [-P PASSWORD] [-n NAME]
                      [-c CPU] [-m MEM] [-v HDISK] [-i ISO] [-N NET] [-M MAC]
                      [-S STORE] [-g GUESTOS] [-V] [--summary] [-u]

ESXi Create VM utility.

optional arguments:
  -h, --help            show this help message and exit
  -d, --dry             Enable Dry Run mode (False)
  -H HOST, --Host HOST  ESXi Host/IP (esxi)
  -U USER, --User USER  ESXi Host username (root)
  -P PASSWORD, --Password PASSWORD
                        ESXi Host password (*****)
  -n NAME, --name NAME  VM name
  -c CPU, --cpu CPU     Number of vCPUS (2)
  -m MEM, --mem MEM     Memory in GB (2)
  -v HDISK, --vdisk HDISK
                        Size of virt hdisk (12)
  -i ISO, --iso ISO     CDROM ISO Path | None (None)
  -N NET, --net NET     Network Interface | None (192.168.1)
  -M MAC, --mac MAC     MAC address
  -S STORE, --store STORE
                        vmfs Store | LeastUsed (DS_3TB_m)
  -g GUESTOS, --guestos GUESTOS
                        Guest OS. (centos-64)
  -V, --verbose         Enable Verbose mode (False)
  --summary             Display Summary (False)
  -u, --updateDefaults  Update Default VM settings stored in ~/.esxi-vm.yml

```


Example Usage
-------------

  Running the script for the first time it's recommended to specify your defaults.  (ESXi HOST, PASSWORD)

```
./esxi-vm-create -H esxi -P MySecurePassword -u
Saving new Defaults to ~/.esxi-vm.yml
```


  Create a new VM named testvm01 using all defaults from ~/.esxi-vm.yml.
```
        ./esxi-vm-create -n testvm01

        Create VM Success
        ESXi Host: esxi
        VM NAME: testvm01
        vCPU: 2
        Memory: 4GB
        VM Disk: 20GB
        DS Store: DS_4TB
        Network: None
```

  Change default number of vCPUs to 4, Memory to 8GB and vDisk size to 40GB.
```
        ./esxi-vm-create -c 4 -m 8 -s 40 -u
        Saving new Defaults to ~/.esxi-vm.yml
```

  Create a new VM named testvm02 using new defaults from ~/.esxi-vm.yml and specifying a Network interface and partial MAC.
```
./esxi-vm-create -n testvm02 -N 192.168.1 -M 01:02:03
00:50:56:01:02:03
```

  Available Network Interfaces and Available Disk Storage volumes will be listed if an invalid option is specified.

```
./esxi-vm-create -n testvm03 -N BadNet -S BadDS
ERROR: Disk Storage BadDS doesn't exist.
    Available Disk Stores: ['DS_SSD500s', 'DS_SSD500c', 'DS_SSD250', 'DS_4TB', 'DS_3TB_m']
    LeastUsed Disk Store : DS_4TB
ERROR: Virtual NIC BadNet doesn't exist.
    Available VM NICs: ['192.168.1', '192.168.0', 'VM Network test'] or 'None'
```

  Create a new VM named testvm03 using a valid Network Interface, valid Disk Storage volume, summary and verbose enabled.  Save as default.  
```
./esxi-vm-create -n testvm03 -N 192.168.1 -S DS_3TB_m --summary --verbose --updateDefaults
Saving new Defaults to ~/.esxi-vm.yml
Create testvm03.vmx file
Create testvm03.vmdk file
Register VM
Power ON VM

Create VM Success:
ESXi Host: esxi
VM NAME: testvm03
vCPU: 2
Memory: 4GB
VM Disk: 20GB
Format: thin
DS Store: DS_3TB_m
Network: 192.168.1
Guest OS: centos-64
MAC: 00:0c:29:32:63:92
00:0c:29:32:63:92
```

License
-------

Copyright (C) 2017 Jonathan Senkerik

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Support
-------
  Website : http://www.jintegrate.co

  github  : http://github.com/josenk/

