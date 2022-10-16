try:
    dataa = None
    with open(
        ljinux.api.betterpath(ljinux.based.user_vars["argj"].split()[1]), "rb"
    ) as f:
        dataa = f.read()
    a = """
from binascii import crc32
dataa = hex(crc32(dataa))[2:]
"""
    exec(a, locals())
    ljinux.based.user_vars["return"] = str(dataa)
    del dataa
    print(ljinux.based.user_vars["return"])

except OSError:
    ljinux.based.error(4, ljinux.based.user_vars["argj"].split()[1])
    ljinux.based.user_vars["return"] = "1"

except IndexError:
    ljinux.based.error(1)
    ljinux.based.user_vars["return"] = "1"
