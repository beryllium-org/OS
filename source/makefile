SHELL = bash

all: help
install: wsltest modules rootfs kernel extra drivers boot wslclean
debug: wsltest modules rootfs kernel_debug extra drivers boot wslclean

kernel: prep clean_core comp strap_kern
kernel_debug: prep clean_core debug_comp strap_kern

prep: modules prepperms

help:
	@cat ../other/makefile_help.txt
update_modules:
	@echo "Updating git submodules from remotes.."
	@git submodule update --init --recursive --remote ..
	@echo -e "Submodules ready\n\nMake sure to git commit before procceding to make!!"
remove_all_modules:
	@echo "Removing all github submodules.."
	@git submodule deinit --all --force
modules:
	@echo "Preparing git submodules.."
	@git submodule update --init --recursive ..
	@echo "Submodules ready"
rootfs:
	@echo -e "\nUpdating the board's coreutils and base packages:"
	@python3 ../scripts/gen_base.py
	@python3 ../scripts/gen_coreutils.py
	@python3 ../scripts/copy_rootfs.py
	@sync
prepperms:
	@echo -n "Preparing script permissions.."
	@chmod +x ../scripts/*.sh
	@echo " OK"
clean_core:
	@if [ -e "core_packages/kernel.jpk" ]; then rm core_packages/kernel.jpk; fi
	@if [ -e "core_packages/jcurses.jpk" ]; then rm core_packages/jcurses.jpk; fi
	@if [ -e "core_packages/cptoml.jpk" ]; then rm core_packages/cptoml.jpk; fi
	@if [ -e "core_packages/jz.jpk" ]; then rm core_packages/jz.jpk; fi
	@if [ -e "core_packages/manual.jpk" ]; then rm core_packages/manual.jpk; fi
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
drivers:
	@echo -e "\nLoading drivers:"
	@python3 ../scripts/make_drivers.py
	@sync
clean: clean_core
	@find .. -type d -name "build_*" -exec rm -r {} +
full_clean: clean
	@find .. -type f -name "mpy-cross*" -exec rm {} +
	@if [ -e "release" ]; then rm -r release; fi
boot:
	@echo -e "\nSetup /boot:"
	@python3 ../scripts/make_boot.py
releases: modules
	@echo "Creating releases archives.."
	@../scripts/make_releases.sh
strap_kern:
	@echo -e "\nStrapping kernel.."
	@python3 ../scripts/strap_kern.py
wsltest:
	@python3 ../scripts/wslmount.py
wslclean:
	@python3 ../scripts/wslrmsetter.py
