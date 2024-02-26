try:
    del be.based.alias_dict[be.based.user_vars["argj"].split()[1]]
    be.api.setvar("return", "0")
except KeyError:
    be.based.error(1)
    be.api.setvar("return", "1")
