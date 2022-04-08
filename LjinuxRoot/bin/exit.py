global Exit
global Exit_code
print("Bye")
Exit = True
try:
    Exit_code = int(ljinux.based.user_vars["argj"].split()[1])
except IndexError:
    pass 
