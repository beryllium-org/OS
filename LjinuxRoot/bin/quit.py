rename_process("quit")
vr("Exit", True, pid=0)
try:
    vr("Exit_code", int(ljinux.based.user_vars["argj"].split()[1]), pid=0)
except IndexError:
    pass
