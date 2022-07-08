try:
    inpt = ljinux.based.user_vars["argj"].split()[1]
    eqpos = inpt.find("=", 0)
    cmd = inpt[:eqpos]
    alcmd = inpt[eqpos + 1 :]
    del inpt, eqpos
    offs = 1
    if alcmd.startswith('"'):
        alcmd = alcmd[1:]
        while not alcmd.endswith('"'):
            offs += 1
            alcmd += " " + ljinux.based.user_vars["argj"].split()[offs]
        del offs
        alcmd = alcmd[:-1]
    else:
        raise IndexError
    ljinux.based.alias_dict.update({cmd: alcmd})
    del cmd, alcmd
    ljinux.based.user_vars["return"] = "0"
except IndexError:
    ljinux.based.error(1)
    ljinux.based.user_vars["return"] = "1"
