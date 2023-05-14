global Exit
global Exit_code
term.write("Bye")
Exit = True
try:
    Exit_code = int(ljinux.based.user_vars["argj"].split()[1])
except IndexError:
    pass
