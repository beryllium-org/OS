# Reload the stored hostname
with be.api.fs.open("/etc/hostname", "r") as pv[get_pid()]["hs"]:
    vr("lines", vr("hs").readlines())
    be.based.system_vars["HOSTNAME"] = vr("lines")[0][:-1]
