try:
    exec(
        "ljinux.io.ledset(({}, {}, {}))".format(
            ljinux.based.user_vars["argj"].split()[1],
            ljinux.based.user_vars["argj"].split()[2],
            ljinux.based.user_vars["argj"].split()[3],
        )
    )  # casting not needed since exec takes str
    ljinux.based.user_vars["return"] = "0"
except IndexError:
    try:
        ljinux.io.ledset(int(ljinux.based.user_vars["argj"].split()[1]))
    except IndexError:
        ljinux.based.error()
        ljinux.based.user_vars["return"] = "1"
