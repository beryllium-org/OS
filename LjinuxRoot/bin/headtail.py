opts = ljinux.api.xarg(ljinux.based.user_vars["argj"], False)
mod = opts["n"][opts["n"].rfind("/") + 1 :]

lines = 10 if not ("n" in opts["o"]) else int(opts["o"]["n"])

was_held = False
if term.hold_stdout:
    was_held = True
else:
    term.hold_stdout = True

try:
    with ljinux.api.fopen(opts["w"][0], "r") as f:
        content = f.readlines()
        count = len(content)
        start = 0 if mod == "head" else count - lines
        end = lines if mod == "head" else count - 1
        for item in content[start:end]:
            term.write(item, end="")
            del item
        if mod == "tail":
            term.write(content[-1])
        del content, count, start, end
        ljinux.api.setvar("return", "0")

except OSError:
    ljinux.based.error(4, filee)
    ljinux.api.setvar("return", "1")

except IndexError:
    ljinux.based.error(9)
    ljinux.api.setvar("return", "1")

if not was_held:
    term.hold_stdout = False
    term.flush_writes()

del lines, opts, mod, was_held
