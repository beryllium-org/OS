stdout.write("\033]0;")
for i in ljinux.based.user_vars["argj"].split()[1:]:
    stdout.write(i + " ")
    del i
stdout.write("\007")
