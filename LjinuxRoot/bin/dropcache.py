rename_process("dropcache")
vr("opts", ljinux.api.xarg())
if "help" in vr("opts")["o"] or "-h" in vr("opts")["o"]:
    term.write("Usage: dropcache\n\nClears all code cache.")
else:
    ljinux.code_cache.clear()
    term.write("Cleared all code cache!")
ljinux.api.setvar("return", "0")
