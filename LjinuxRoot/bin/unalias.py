try:
    del ljinux.based.alias_dict[ljinux.based.user_vars["argj"].split()[1]]
    ljinux.api.setvar("return", "0")
except KeyError:
    ljinux.based.error(1)
    ljinux.api.setvar("return", "1")
