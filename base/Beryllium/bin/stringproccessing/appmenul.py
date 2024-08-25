vr("appl", be.api.fs.listdir("/usr/share/applications"))
vr("apps", {})

# Generates a dict with all the installed applications

# The dict keys are the application pretty names.
# The dict items are lists of the following format:
# [description, executable, run_mode]

# Description is free text
# Exectuable is a path
# run_mode can be "Python", "WM" or "Shell"
# Python means it will be run as a new python process
# WM means it will run under the current window manager
# Shell means it will be run as a shell command

vr("toml_s", None)
for pv[get_pid()]["i"] in range(len(vr("appl"))):
    vr("toml_s", "/Beryllium/usr/share/applications/" + vr("appl")[vr("i")][0])
    vr("apps")[cptoml.fetch("name", toml=vr("toml_s"))] = [
        cptoml.fetch("desc", toml=vr("toml_s")),
        cptoml.fetch("exec", toml=vr("toml_s")),
        cptoml.fetch("run_mode", toml=vr("toml_s")).lower(),
    ]
vrd("toml_s")
vrd("appl")
vrp("ok")
