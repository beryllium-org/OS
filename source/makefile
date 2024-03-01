SHELL = bash

all: help
install: rootfs kernel extra boot
debug: rootfs kernel_debug extra boot

kernel: prep clean_core comp strap_kern
kernel_debug: prep clean_core debug_comp strap_kern

prep: modules prepperms

help:
	@cat ../other/makefile_help.txt
update_modules:
	@echo "Updating git submodules from remotes.."
	@git submodule update --init --recursive --remote ..
	@echo -e "Submodules ready\n\nMake sure to git commit before procceding to make!!"
modules:
	@echo "Preparing git submodules.."
	@git submodule update --init --recursive ..
	@echo "Submodules ready"
rootfs:
	@echo -e "\nUpdating the board's rootfs:"
	@sync
	@python3 ../scripts/copy_rootfs.py
prepperms:
	@echo -n "Preparing script permissions.."
	@chmod +x ../scripts/*.sh
	@echo " OK"
clean_core:
	@if [ -e "core_packages/kernel.jpk" ]; then rm core_packages/kernel.jpk; fi
	@if [ -e "core_packages/jcurses.jpk" ]; then rm core_packages/jcurses.jpk; fi
	@if [ -e "core_packages/cptoml.jpk" ]; then rm core_packages/cptoml.jpk; fi
	@if [ -e "core_packages/jz.jpk" ]; then rm core_packages/jz.jpk; fi
comp:
	@echo -e "\nCommencing kernel compilation.."
	@sync
	@python3 ../scripts/make_kernel.py
debug_comp:
	@echo -e "\nCommencing kernel compilation.. (debug)"
	@sync
	@python3 ../scripts/make_kernel.py debug
extra:
	@echo -e "\nLoading extras:"
	@python3 ../scripts/make_extras.py
	@sync
clean: clean_core
	@rm -r ./build_* || true
boot:
	@echo -e "\nSetup /boot:"
	@python3 ../scripts/make_boot.py
releases:
	@echo "Creating releases archives.."
	@../scripts/make_releases.sh
strap_kern:
	@echo -e "\nStrapping kernel.."
	@python3 ../scripts/strap_kern.py
