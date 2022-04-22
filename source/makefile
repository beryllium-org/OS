SHELL = bash
all: kern donemsg
kern: prepperms kerncomp
install: kern rootfs donemsg
compiletest: prepperms ctest
debug: prepperms kerncompd
test: compiletest blacktest

donemsg:
	@echo -e "\nSyncing changes.."
	@sync
	@echo -e "\n   ---Operation completed successfully---\n\nTry running make connection"
rootfs:
	@echo -e "\nUpdating the board's rootfs:\n"
	@sync
	@../scripts/copy_rootfs.sh
prepperms:
	@echo -e "Preparing script permissions..\n"
	@chmod +x ../scripts/*.sh
	@echo -e "OK"
kerncomp:
	@echo -e "\nCommencing kernel compilation..\n"
	@sync
	@python3 ../scripts/make_kernel.py
kerncompd:
	@echo -e "\nCommencing debug kernel compilation.."
	@sync
	@python3 ../scripts/make_kernel_debug.py
ctest:
	@echo -e "\nCommencing kernel compile test\nNote: This does not update any board files.\n"
	@../scripts/make_kernel_test.sh
connection:
	@echo -n "Ensuring GNU/Screen is installed.. "
	@command -v screen >/dev/null && echo "Found" || (echo -e "Not found\nInstalling.." && ./scripts/installscreen.sh)
	@echo -e "\nRunning screen connection.. "
	@../scripts/screenningg.sh
blacktest:
	@echo -n "Commencing black compatibility test.. "
	@command -v black >/dev/null && echo -e "Found black\n" || (echo -e "Not found\nInstalling.." && ./scripts/installblack.sh)
	black --check .
	@../scripts/returncheck.sh
