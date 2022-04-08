try:
    filee = ""
    mans = listdir("/LjinuxRoot/usr/share/man")
    for i in mans:
        if i.endswith(".json") and ljinux.based.user_vars["argj"].split()[1] == i[:-5]:
            filee += "/" + i
            break
    del mans
    try:
        with open(("/LjinuxRoot/usr/share/man" + filee), "r") as f:
            man = json.load(f)
            f.close()
        print("\nNAME" + "\n\t" + man["NAME"] + "\n")
        print("SYNOPSIS" + "\n\t" + man["SYNOPSIS"] + "\n")
        print("DESCRIPTION" + "\n\t" + man["DESCRIPTION"] + "\n")
        del filee
        del man
        ljinux.based.user_vars["return"] = "0"
    except:
        dmtex(
            "Manual file could not be found / parsed for "
            + ljinux.based.user_vars["argj"].split()[1]
            + "."
        )
        ljinux.based.user_vars["return"] = "1"
except (OSError, IndexError):  # I guess no man then
    ljinux.based.error(8)
    ljinux.based.user_vars["return"] = "1" 
