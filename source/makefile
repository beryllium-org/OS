# I HAAAATE MAKE
SHELL = bash
all: prepperms kerncomp sync
install: prepperms kerncomp rootfs sync
compiletest: prepperms ctest

sync:
	@echo -e "\nSyncing changes.."
	@sync
	@echo -e "\nDone"
rootfs:
	@echo -e "\nUpdating the pico's rootfs:\n"
	@./copy_rootfs.sh
prepperms:
	@echo -e "Preparing script permissions..\n"
	@chmod +x ./make_kernel.sh
	@chmod +x ./make_kernel_test.sh
	@chmod +x ./clean.sh
	@chmod +x ./copy_rootfs.sh
kerncomp:
	@echo -e "Commencing kernel compilation..\n"
	@sync
	@./make_kernel.sh
ctest:
	@echo -e "Commencing kernel compile test\nNote: This should only be used to verify the kernel compiles!\n"
	@./make_kernel_test.sh
