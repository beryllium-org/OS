rename_process("dropcache")
vr("opts", be.api.xarg())
if "help" in vr("opts")["o"] or "h" in vr("opts")["o"]:
    term.write("Usage: dropcache\n\nClears all code cache.")
else:
    be.code_cache.clear()
    term.write("Cleared all code cache!")
be.api.setvar("return", "0")
