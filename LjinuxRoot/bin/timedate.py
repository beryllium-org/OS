args = ljinux.based.user_vars["argj"].split()
try:
    if args[1] == "set":
        try:
            the_time = time.struct_time(    
                    int(args[4]),
                    int(args[3]),
                    int(args[2]),
                    int(args[5]),
                    int(args[6]),
                    int(args[7]),
                    1,
                    -1,
                    -1,
            )
            rtcc.write_datetime(the_time)
        except IndexError:
            ljinux.based.error(1)
    del args
        
except IndexError:
    tt = time.localtime()
    print("Current time: ", end="")
    print(f"{tt.tm_mday}/{tt.tm_mon}/{tt.tm_year} {tt.tm_hour}:{tt.tm_min}:{tt.tm_sec}")
    del tt

