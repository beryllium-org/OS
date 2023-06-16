if "network" in ljinux.modules and ljinux.modules["network"].connected == True:
    try:
        ljinux.modules["network"].timeset()
    except:
        dmtex("Could not sync time.")
