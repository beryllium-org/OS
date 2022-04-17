# I HAAAATE MAKE
SHELL = bash
all: prepperms kerncomp sync
install: prepperms kerncomp rootfs donemsg
compiletest: prepperms ctest
connection: cn

donemsg:
	@echo -e "\nSyncing changes.."
	@sync
	@echo -e "\nDone. "
rootfs:
	@echo -e "\nUpdating the pico's rootfs:\n"
	@sync
	@./scripts/copy_rootfs.sh
prepperms:
	@echo -e "Preparing script permissions..\n"
	@chmod +x ./scripts/*.sh
	@echo -e "OK"
kerncomp:
	@echo -e "\nCommencing kernel compilation..\n"
	@sync
	@time ./scripts/make_kernel.sh
ctest:
	@echo -e "Commencing kernel compile test\nNote: This should only be used to verify the kernel compiles!\n"
	@time ./scripts/make_kernel_test.sh
cn:
	@echo -n "Ensuring GNU/Screen is installed.. "
	@command -v screen >/dev/null && echo "Found" || (echo -e "Not found\nInstalling.." && ./scripts/installscreen.sh)
	@echo -n "\nRunning screen connection.."
	@./scripts/screenningg.sh
