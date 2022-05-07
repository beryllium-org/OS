try:
    global sdcard_fs
    if not sdcard_fs:
        remount("/", False)
    try:
        filee = open(ljinux.based.user_vars["argj"].split()[2], "w")
        gc.enable()
        gc.collect()
        gc.collect()
        socket.gc.enable()
        socket.gc.collect()
        socket.gc.collect()
        a = requests.get(ljinux.based.user_vars["argj"].split()[1])
        filee.write(a.text)
        filee.flush()
        del a
        filee.close()
        del filee
    except IndexError:
        ljinux.based.error(9)
    if not sdcard_fs:
        remount("/", True)
except RuntimeError:
    ljinux.based.error(7)
