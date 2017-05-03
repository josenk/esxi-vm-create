Introduction
------------

  This utility is a simple to use comand line tool to create VMs on an ESXi host from from a system running python and ssh.  vCenter is not required.   You need to enable ssh access on your ESXi server.  It's HIGHLY RECOMMENDED to use password-less authentication by copying your ssh public keys to the ESXi host.


Command Line Args
-----------------

```
        ./esxi-vm-create -h
        usage: esxi-vm-create [-h] [-d] [-v] [-H HOST] [-U USER] [-P PASSWORD]
                      [-n NAME] [-c CPU] [-m MEM] [-s SIZE] [-i ISO] [-N NET]
                      [-S STORE] [-g GUESTOS] [-u]

        ESXi Create VM utility.

        optional arguments:
          -h, --help            show this help message and exit
          -d, --dry             Enable Dry Run mode (False)
          -v, --verbose         Enable Verbose mode (False)
          -H HOST, --Host HOST  ESXi Host (esxi)
          -U USER, --User USER  ESXi Host username (root)
          -P PASSWORD, --Password PASSWORD
                                ESXi Host password (*****)
          -n NAME, --name NAME  VM name
          -c CPU, --cpu CPU     Number of vCPUS (2)
          -m MEM, --mem MEM     Memory in GB (4)
          -s SIZE, --size SIZE  Size of virt disk (20)
          -i ISO, --iso ISO     CDROM ISO Path | None (None)
          -N NET, --net NET     Network Interface | None (None)
          -S STORE, --store STORE
                                vmfs Store | LeastUsed (DS_3TB_m)
          -g GUESTOS, --guestos GUESTOS
                                Guest OS. (centos-64)
          -u, --updateDefaults  Update Default VM settings stored in ~/.esxi-vm.yml
        
```


Examples
--------


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

  Create a new VM named testvm02 using new defaults from ~/.esxi-vm.yml and specifying a Network interface.
```
        ./esxi-vm-create -n testvm02 -N 192.168.1

       Create VM Success
       ESXi Host: esxi
       VM NAME: testvm02
       vCPU: 4
       Memory: 8GB
       VM Disk: 40GB
       DS Store: DS_4TB
       Network: 192.168.1
```

  Available Network Interfaces and Available Disk Storage volumes will be listed if an invalid entry is made.

```
        ./esxi-vm-create -n testvm03 -N BadNet -S BadDS
        ERROR: Disk Storage BadDS doesn't exist.
            Available Disk Stores: ['DS_SSD500s', 'DS_SSD500c', 'DS_SSD250', 'DS_4TB', 'DS_3TB_m']
            LeastUsed Disk Store : DS_4TB
        ERROR: Virtual NIC BadNet doesn't exist.
            Available VM NICs: ['192.168.1', '192.168.0', 'VM Network test'] or 'None'
```

  Create a new VM named testvm03 using a valid Network Interface, valid Disk Storage volume, enabled verbose and saving the settings as default.  
```
        ./esxi-vm-create -n testvm03 -N 192.168.1 -S DS_3TB_m -v -u
        Saving new Defaults to ~/.esxi-vm.yml
        Create testvm03.vmx file
        Create testvm03.vmdk file
        Register VM
        Power ON VM

        Create VM Success
        ESXi Host: esxi
        VM NAME: testvm03
        vCPU: 4
        Memory: 8GB
        VM Disk: 40GB
        Format: thin
        DS Store: DS_3TB_m
        Network: 192.168.1
        Guest OS: centos-64
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

