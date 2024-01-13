rename_process("m5x-camera")
import espcamera

vr("opts", ljinux.api.xarg())

vr(
    "dev",
    cptoml.fetch("device", toml=ljinux.api.betterpath("/etc/camera.d/config.toml")),
)

if "init" in vr("opts")["o"] or "i" in vr("opts")["o"]:
    if vr("dev") not in ljinux.devices:
        if "mode" in vr("opts")["o"] or "m" in vr("opts")["o"]:
            if "mode" in vr("opts")["o"]:
                vr("mode", vr("opts")["o"]["mode"])
            else:
                vr("mode", vr("opts")["o"]["m"])
        else:
            vr(
                "mode",
                cptoml.fetch(
                    "default_preset",
                    toml=ljinux.api.betterpath("/etc/camera.d/config.toml"),
                ),
            )
        vr("pr", ljinux.api.betterpath("/etc/camera.d/presets/" + vr("mode") + ".toml"))
        exec(
            'vr("px", espcamera.PixelFormat.'
            + cptoml.fetch(
                "pixel_format",
                toml=ljinux.api.betterpath(vr("pr")),
            )
            + ")"
        )
        exec(
            'vr("fr", espcamera.FrameSize.'
            + cptoml.fetch(
                "frame_size",
                toml=ljinux.api.betterpath(vr("pr")),
            )
            + ")"
        )
        vr(
            "qual",
            cptoml.fetch(
                "jpeg_quality",
                toml=ljinux.api.betterpath(vr("pr")),
            ),
        )
        ljinux.devices[vr("dev")] = espcamera.Camera(
            data_pins=board.D,
            pixel_clock_pin=board.PCLK,
            vsync_pin=board.VSYNC,
            href_pin=board.HREF,
            i2c=board.SSCB_I2C(),
            external_clock_pin=board.XCLK,
            external_clock_frequency=20_000_000,
            powerdown_pin=None,
            reset_pin=board.RESET,
            pixel_format=vr("px"),
            frame_size=vr("fr"),
            jpeg_quality=vr("qual"),
            framebuffer_count=1,
            grab_mode=espcamera.GrabMode.LATEST,
        )
        term.write('Initializing camera on mode "' + vr("mode") + '"')
        ljinux.devices[vr("dev")].vflip = True
        ljinux.devices[vr("dev")].denoise = cptoml.fetch(
            "denoise",
            toml=ljinux.api.betterpath(vr("pr")),
        )
        ljinux.devices[vr("dev")].awb_gain = True
        sleep(0.5)
        ljinux.devices[vr("dev")].take()
        term.write("Initialized!")
    else:
        term.write("Camera already initialized.")

if "capture" in vr("opts")["o"] or "c" in vr("opts")["o"]:
    if vr("dev") not in ljinux.devices:
        term.write("Camera not initialized.")
    else:
        vr("photo_data", ljinux.devices[vr("dev")].take(0.4))
        vr("ql", ljinux.devices[vr("dev")].quality)
        while not isinstance(vr("photo_data"), memoryview):
            if ljinux.devices[vr("dev")].quality < 20:
                ljinux.devices[vr("dev")].quality += 1
            vr("photo_data", ljinux.devices[vr("dev")].take(0.4))
        term.write(
            'Snapped! Quality={}\nSaving to "'.format(
                ljinux.devices[vr("dev")].quality
            ),
            end="",
        )
        ljinux.devices[vr("dev")].quality = vr("ql")
        vr("tt", time.localtime())
        vr("pic_name", "M5X-")
        if vr("tt").tm_mday < 10:
            vrp("pic_name", "0")
        vrp("pic_name", str(vr("tt").tm_mday) + "-")
        if vr("tt").tm_mon < 10:
            vrp("pic_name", "0")
        vrp("pic_name", str(vr("tt").tm_mon) + "-" + str(vr("tt").tm_year) + "-")
        if vr("tt").tm_hour < 10:
            vrp("pic_name", "0")
        vrp("pic_name", str(vr("tt").tm_hour) + "-")
        if vr("tt").tm_min < 10:
            vrp("pic_name", "0")
        vrp("pic_name", str(vr("tt").tm_min) + "-")
        if vr("tt").tm_sec < 10:
            vrp("pic_name", "0")
        vrp("pic_name", str(vr("tt").tm_sec) + ".jpeg")
        term.write(vr("pic_name") + '"...')
        if "dry-run" not in vr("opts")["o"]:
            with ljinux.api.fopen(vr("pic_name"), "wb") as pv[get_pid()]["f"]:
                vr("f").write(vr("photo_data"))
        term.write("Saved!")

# if "serve" in vr("opts")["o"] or "s" in vr("opts")["o"]:
#    if vr("dev") not in ljinux.devices:
#        term.write("Camera not initialized.")
#    else:
#
#
#
#    term.write(
#        "Starting RTSP Camera server on "
#        + str(ipconf["ip"])
#        + ":80"
#    )
#    webserver = HTTPServer(ljinux.modules["network"]._pool)
#    @webserver.route("/capture", "POST")
#    def base(request):
#        ljinux.io.ledset(3)
#        vr("res", "FAIL: Invalid form.")
#        vr("raw", request.raw_request.decode("UTF-8").split())
#        vr("data_pos", vr("raw").find('{"'))
#        if vr("data_pos") != -1:
#            import json
#            vr("data", loads(" ".join(vr("raw")[vr("pos"):])))
#            term.write("Got: " + str(vr("data")))
#            vr("res", "ok")
#            del json
#        return HTTPResponse(body=vr("res"))
#
#    @webserver.route("/")
#    def base(request):
#        ljinux.io.ledset(3)
#        return HTTPResponse(body=vr("res"))
#
#    ipconf = ljinux.modules["network"].get_ipconf()
#    term.write("Started. Press Ctrl + C to stop.")
#    webserver.start(
#        host=str(ipconf["ip"]),
#        port=80,
#    )
#    while not term.is_interrupted():
#        try:
#            webserver.poll()
#        except KeyboardInterrupt:
#            term.write("Exiting")
#        except Exception as err:
#            term.write(f"Error: {err}")

if "deinit" in vr("opts")["o"] or "d" in vr("opts")["o"]:
    if vr("dev") not in ljinux.devices:
        term.write("Camera not initialized.")
    else:
        ljinux.devices[vr("dev")].deinit()
        del ljinux.devices[vr("dev")], espcamera

if not len(vr("opts")["o"]) or "h" in vr("opts")["o"] or "help" in vr("opts")["o"]:
    term.write("help menu here")
