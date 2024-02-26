from os import urandom

be.api.setvar("return", str(int.from_bytes(urandom(3), "big")))
del urandom
if not be.based.silent:
    term.write(be.api.getvar("return"))
