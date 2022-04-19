SHELL = bash
all: kern donemsg
kern: prepperms kerncomp
install: kern rootfs donemsg
compiletest: prepperms ctest
debug: prepperms kerncompd

donemsg:
	@echo -e "\nSyncing changes.."
	@sync
	@echo -e "\n   ---Operation completed successfully---\n\nTry running make connection"
rootfs:
	@echo -e "\nUpdating the board's rootfs:\n"
	@sync
	@./scripts/copy_rootfs.sh
prepperms:
	@echo -e "Preparing script permissions..\n"
	@chmod +x ./scripts/*.sh
	@echo -e "OK"
kerncomp:
	@echo -e "\nCommencing kernel compilation..\n"
	@sync
	@./scripts/make_kernel.sh
kerncompd:
	@echo -e "\nCommencing debug kernel compilation..\n"
	@sync
	@./scripts/make_kernel_debug.sh
ctest:
	@echo -e "Commencing kernel compile test\nNote: This should only be used to verify the kernel compiles!\n"
	@./scripts/make_kernel_test.sh
connection:
	@echo -n "Ensuring GNU/Screen is installed.. "
	@command -v screen >/dev/null && echo "Found" || (echo -e "Not found\nInstalling.." && ./scripts/installscreen.sh)
	@echo -e "\nRunning screen connection.. "
	@./scripts/screenningg.sh
