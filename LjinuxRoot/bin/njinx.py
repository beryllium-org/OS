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
    except:
        print("Error: Njinx configuration file is invalid. Abort.")

    # cleanup
    print("Cleaning up..")
    ljinux.modules["network"].resetsock()
    del globals()["adafruit_httpserver"], server, ipconf
else:
    ljinux.based.error(5)
    ljinux.based.user_vars["return"] = "1"
