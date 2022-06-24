try:
    time.sleep(int(ljinux.based.user_vars["argj"].split()[1]))
except IndexError:
    time.sleep(1)
ljinux.based.user_vars["return"] = "0"
