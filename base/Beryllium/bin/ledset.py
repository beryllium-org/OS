try:
    exec(
        "be.io.ledset(({}, {}, {}))".format(
            be.based.user_vars["argj"].split()[1],
            be.based.user_vars["argj"].split()[2],
            be.based.user_vars["argj"].split()[3],
        )
    )
    be.api.setvar("return", "0")
except IndexError:
    try:
        be.io.ledset(int(be.based.user_vars["argj"].split()[1]))
        be.api.setvar("return", "0")
    except IndexError:
        be.based.error(1)
        be.api.setvar("return", "1")
