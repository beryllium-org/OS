rename_process("hostname-reload")
with ljinux.api.fopen("/etc/hostname", "r") as pv[get_pid()]["hs"]:
    vr("lines", vr("hs").readlines())
    ljinux.based.system_vars["HOSTNAME"] = vr("lines")[0][:-1]
