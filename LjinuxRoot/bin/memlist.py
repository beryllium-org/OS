term.write(
    f"Memory allocation details:\n\n - len(locals()): {len(locals())}\n - len(globals()): {len(globals())}\n\nlocals list:\n"
)
ml = locals()
for i in ml:
    term.write(str(i))
del i, ml
term.write("\n\nglobals:\n")
gl = globals()
for i in gl:
    term.write(str(i))
del i, gl
