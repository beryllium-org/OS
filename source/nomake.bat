@echo -e "\nCommencing kernel compilation.."
@python3 ../scripts/make_kernel.py
@echo -e "\nUpdating the board's rootfs:\n"
@python3 ../scripts/copy_rootfs.py
@echo -e "\n   ---Operation completed successfully---\n\nTry running make connection"
