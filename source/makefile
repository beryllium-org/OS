SHELL = bash

all: help
install: kernel rootfs extra

kernel: prep comp
kernel_debug: prep debug_comp

#w5500spi: prep driver_w5500spi
#w5500spi_debug: prep driver_w5500spi_debug

prep: modules prepperms

help:
	@cat ../other/makefile_help.txt
#driver_w5500spi:
#	@echo -e "\nInstalling w5500 spi driver"
#	@python3 ../scripts/copy_w5500spi.py
#	@sync
#	@echo "w5500 spi driver done"
#driver_w5500spi_debug:
#	@echo -e "\nInstalling w5500 spi driver (debug)"
#	@python3 ../scripts/copy_w5500spi.py debug
#	@sync
#	@echo "w5500 spi driver done"
update_modules:
	@echo "Updating git submodules from remotes.."
	@git submodule update --init --recursive --remote ..
	@echo -e "Submodules ready\n\nMake sure to git commit before procceding to make!!"
modules:
	@echo "Preparing git submodules.."
	@git submodule update --init --recursive ..
	@echo "Submodules ready"
rootfs:
	@echo -e "\nUpdating the board's rootfs:\n"
	@sync
	@python3 ../scripts/copy_rootfs.py
prepperms:
	@echo -n "Preparing script permissions.."
	@chmod +x ../scripts/*.sh
	@echo " OK"
comp:
	@echo -e "\nCommencing kernel compilation.."
	@sync
	@python3 ../scripts/make_kernel.py
debug_comp:
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
extra:
	@python3 ../scripts/make_extras.py
	@sync
clean:
	@rm -r ./build_*
