try:
    ljinux.io.ledset(int(ljinux.based.user_vars["argj"].split()[1]))
    ljinux.based.user_vars["return"] = "0"
except IndexError:
    ljinux.based.error()
    ljinux.based.user_vars["return"] = "1"
