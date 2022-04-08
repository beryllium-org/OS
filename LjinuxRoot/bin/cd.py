try:
    chdir(ljinux.based.user_vars["argj"].split()[1])
except OSError:
    print("Error: Directory does not exist")
except IndexError:
    pass
