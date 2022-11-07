try:
    inpt = ljinux.based.user_vars["argj"].split()
    eqpos = inpt[1].find("=", 0)
    cmd = inpt[1][:eqpos]
    alcmd = inpt[1][eqpos + 1 :]
    del eqpos
    offs = 1
    if alcmd.startswith('"'):
        alcmd = alcmd[1:]
        while not alcmd.endswith('"'):
            offs += 1
            alcmd += " " + inpt[offs]
        del offs
        alcmd = alcmd[:-1]
    else:
        raise IndexError
    ljinux.based.alias_dict.update({cmd: alcmd})
    del cmd, alcmd, inpt
    ljinux.api.setvar("return", "0")
except IndexError:
    ljinux.based.error(1)
    ljinux.api.setvar("return", "1")
