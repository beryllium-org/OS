try:
    exec(
        "ljinux.io.ledset(({}, {}, {}))".format(
            ljinux.based.user_vars["argj"].split()[1],
            ljinux.based.user_vars["argj"].split()[2],
            ljinux.based.user_vars["argj"].split()[3],
        )
    )
    ljinux.api.setvar("return", "0")
except IndexError:
    try:
        ljinux.io.ledset(int(ljinux.based.user_vars["argj"].split()[1]))
        ljinux.api.setvar("return", "0")
    except IndexError:
        ljinux.based.error(1)
        ljinux.api.setvar("return", "1")
