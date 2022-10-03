SHELL = bash

all: help
kernel: kern donemsg
install: kern rootfs donemsg
debug: prep kerncompd
w5500spi_debug: prep driver_w5500spi_debug
wifi: prep driver_wifi
w5500spi: prep driver_w5500spi

kern: prep kerncomp auto_fake_cdc
prep: modules prepperms

help:
	@cat ../other/makefile_help.txt
auto_fake_cdc:
	@python3 ../scripts/auto_fake-cdc.py
driver_wifi:
	@echo "Installing wifi driver"
	@python3 ../scripts/copy_wifi.py
	@sync
	@echo "Wifi driver done"
driver_w5500spi:
	@echo "Installing w5500 spi driver"
	@python3 ../scripts/copy_w5500spi.py
	@sync
	@echo "w5500 spi driver done"
driver_w5500spi_debug:
	@echo "Installing w5500 spi driver (debug)"
	@python3 ../scripts/copy_w5500spi.py debug
	@sync
	@echo "w5500 spi driver done"
update_modules:
	@echo "Updating git submodules from remotes.."
	@git submodule update --init --recursive --remote ..
	@echo -e "Submodules ready\n\nMake sure to git commit before procceding to make!!"
modules:
	@echo "Preparing git submodules.."
	@git submodule update --init --recursive ..
	@echo "Submodules ready"
donemsg:
	@echo -e "\nSyncing changes.."
	@sync
	@echo -e "\n   ---Operation completed successfully---\n\nTry running make connection"
rootfs:
	@echo -e "\nUpdating the board's rootfs:\n"
	@sync
	@python3 ../scripts/copy_rootfs.py
prepperms:
	@echo -e "Preparing script permissions..\n"
	@chmod +x ../scripts/*.sh
	@chmod +x ../scripts/mpy*
	@echo "OK"
kerncomp:
	@echo -e "\nCommencing kernel compilation.."
	@sync
	@python3 ../scripts/make_kernel.py
kerncompd:
	@echo -e "\nCommencing kernel compilation.. (debug)"
	@sync
	@python3 ../scripts/make_kernel.py debug
connection:
	@echo -n "Ensuring GNU/Screen is installed.."
	@command -v screen >/dev/null && echo "Found" || (echo -e "Not found\nInstalling.." && ./scripts/installscreen.sh)
	@echo -n "Ensuring user is in dialout group.."
	@../scripts/groupadd.sh
	@echo -e "\nRunning screen connection.."
	@../scripts/screenningg.sh
blacktest:
	@echo -n "Commencing black compatibility test.."
	@command -v black >/dev/null && echo -e "Found black\n" || (echo -e "Not found\nInstalling.." && ./scripts/installblack.sh)
	@black --check .
	@../scripts/returncheck.sh
ccon:
	@echo -n "Ensuring GNU/Screen is installed.."
	@command -v screen >/dev/null && echo "Found" || (echo -e "Not found\nInstalling.." && ./scripts/installscreen.sh)
	@echo -n "Ensuring user is in dialout group.."
	@../scripts/groupadd.sh
	@echo "Installing ccon to the machine.."
	@python3 ../scripts/ccon.py
	@echo -e "\nDone, now try running ccon\n"
