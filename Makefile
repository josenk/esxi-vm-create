all:
	@echo "make install"

install:
	install -m 755  ./esxi-vm-create /usr/local/bin/
	install -m 755  ./esxi-vm-destroy /usr/local/bin/
	install -m 755  ./esxi_vm_functions.py /usr/local/bin/
	@echo "Install Success."

uninstall:
	rm -fr /usr/local/bin/esxi-vm-create
	rm -fr /usr/local/bin/esxi-vm-destroy
	rm -fr /usr/local/bin/esxi_vm_functions.py
	rm -fr /usr/local/bin/esxi_vm_functions.pyc
