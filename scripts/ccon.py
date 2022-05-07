from os import system, listdir, uname

if uname().sysname == "Darwin":
    pass
elif uname().sysname == "Linux":
    commd = "sudo cp ../scripts/screenningg.sh /bin/ccon"
else:
    print("Error: Unkown platform")
    exit(1)

print(f'Running: "{commd}"')
system(commd)
del commd
