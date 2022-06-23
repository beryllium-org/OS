try:
    exec(
        "ljinux.io.ledset(({}, {}, {}))".format(
            ljinux.based.user_vars["argj"].split()[1],
            ljinux.based.user_vars["argj"].split()[2],
            ljinux.based.user_vars["argj"].split()[3],
        )
    )
    ljinux.based.user_vars["return"] = "0"
except IndexError:
    try:
        ljinux.io.ledset(ljinux.based.user_vars["argj"].split()[1])
    except IndexError:
        ljinux.based.error()
        ljinux.based.user_vars["return"] = "1"
