from os import urandom

ljinux.api.setvar("return", str(int.from_bytes(urandom(3), "big")))
del urandom
if not ljinux.based.silent:
    term.write(ljinux.api.getvar("return"))
