# I HAAAATE MAKE
SHELL = bash
all: prepperms clean kerncomp sync
install: prepperms clean kerncomp rootfs sync
compiletest: prepperms ctest

clean:
	@echo -e "\ncleaning..\n"
	@./scripts/clean.sh
	@sync
sync:
	@echo -e "\nSyncing changes.."
	@sync
	@echo -e "\nDone"
rootfs:
	@echo -e "\nUpdating the pico's rootfs:\n"
	@./scripts/copy_rootfs.sh
prepperms:
	@echo -e "Preparing script permissions..\n"
	@chmod +x ./scripts/make_kernel.sh
	@chmod +x ./scripts/make_kernel_test.sh
	@chmod +x ./scripts/clean.sh
	@chmod +x ./scripts/copy_rootfs.sh
	@echo -e "OK"
kerncomp:
	@echo -e "\nCommencing kernel compilation..\n"
	@sync
	@./scripts/make_kernel.sh
ctest:
	@echo -e "Commencing kernel compile test\nNote: This should only be used to verify the kernel compiles!\n"
	@./scripts/make_kernel_test.sh
