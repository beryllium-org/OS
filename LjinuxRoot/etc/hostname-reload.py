with open("/LjinuxRoot/etc/hostname", "r") as hs:
    lines = hs.readlines()
    ljinux.based.system_vars["HOSTNAME"] = lines[0][:-1]
    del lines
del hs
