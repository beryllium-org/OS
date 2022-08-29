if "network" in ljinux.modules and ljinux.modules["network"].connected == True:
    # init
    globals()["adafruit_httpserver"] = __import__("adafruit_httpserver")
    server = adafruit_httpserver.HTTPServer(ljinux.modules["network"]._pool)

    # fetch data
    ipconf = ljinux.modules["network"].get_ipconf()
    webconf = []
    try:
        with open(ljinux.based.fn.betterpath("/etc/njinx/njinx.conf"), "r") as f:
            webconf = json.load(f)
    except Exception as Err:
        pass
    try:
        print(
            "Now serving "
            + webconf["path"]
            + " at "
            + str(ipconf["ip"])
            + ":"
            + str(webconf["port"])
        )

        # prepare admin
        if webconf["admin"]:

            @server.route("/admin")
            def base(request):
                return adafruit_httpserver.HTTPResponse(
                    filename=ljinux.based.fn.betterpath("/var/www/admin/index.html")
                )

        # post route

        exec(
            '@server.route("/post", "POST")\n'
            + "def base(request):\n"
            + " ljinux.io.ledset(3)\n"
            + ' raw = request.raw_request.decode("utf8").split()\n'
            + " data = dict()\n"
            + " form_dat_pos = 0\n"
            + ' host = "None"\n'
            + " hp = 0\n"
            + ' res = "OK"\n'
            + " try:\n"
            + "  while True:\n"
            + '   if raw[hp] == "Host:":\n'
            + "    host = raw[hp+1]\n"
            + "    break\n"
            + "   hp += 1\n"
            + " except IndexError:\n"
            + "  pass\n"
            + " try:\n"
            + "  while True:\n"
            + '   if raw[form_dat_pos] == "form-data;":\n'
            + "    break\n"
            + "   form_dat_pos += 1\n"
            + " except IndexError:\n"
            + "  form_dat_pos = None\n"
            + " current = form_dat_pos + 1\n"
            + " if form_dat_pos is not None:\n"
            + "  try:\n"
            + "   while True:\n"
            + '    if raw[current].startswith("name="):\n'
            + "     data.update({raw[current][6:-1]: raw[current+1]})\n"
            + "     current += 2\n"
            + "    elif current is len(raw):\n"
            + "     break\n"
            + "    else:\n"
            + "     current += 1\n"
            + "  except IndexError:\n"
            + "   pass\n"
            + " else:\n"
            + '  res = "FAIL"\n'
            + " del raw, current, form_dat_pos\n"
            + ' passwd = "'
            + ljinux.based.fn.betterpath(webconf["password"])
            + '"\n'
            + " try:\n"
            + '  operation = data["operation"]\n'
            + "  print("
            + '"HTTP POST from " + host + " '
            + 'with operation \\"" + operation + "\\"")\n'
            + "  del operation\n"
            + " except KeyError:\n"
            + '  print("Operation instruction not found")\n'
            + " del data, passwd\n"
            + " ljinux.io.ledset(1)\n"
            + " return adafruit_httpserver.HTTPResponse(body=res)"
        )

        # prepare root routing
        exec(
            '@server.route("/")\n'
            + "def base(request):\n"
            + '    return adafruit_httpserver.HTTPResponse(filename="'
            + ljinux.based.fn.betterpath(webconf["path"])
            + '/index.html")'
        )

        # eternal servitude
        print("Started. Press Ctrl + C to stop.")
        ljinux.io.ledset(1)
        ljinux.based.user_vars["return"] = "0"  # admin may edit it

        try:
            server.serve_forever(
                host=str(ipconf["ip"]),
                root=ljinux.based.fn.betterpath(webconf["path"]),
                port=webconf["port"],
            )
        except KeyboardInterrupt:
            pass
    except Exception as err:
        print("Error: Njinx configuration file is invalid. Abort.")
        ljinux.based.user_vars["return"] = "1"
        print(str(err))

    # cleanup
    print("Cleaning up..")
    ljinux.modules["network"].resetsock()
    del globals()["adafruit_httpserver"], server, ipconf
else:
    ljinux.based.error(5)
    ljinux.based.user_vars["return"] = "1"
