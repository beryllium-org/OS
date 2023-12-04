rename_process("m5x-camera")
import espcamera

vr("opts", ljinux.api.xarg())

if "init" in vr("opts")["o"] or "i" in vr("opts")["o"]:
    if "ov3660" not in ljinux.devices:
        vr("mode", None)
        if "mode" in vr("opts")["o"]:
            vr("mode", vr("opts")["o"]["mode"])
        else:
            vr("mode", vr("opts")["o"]["m"])
        if vr("mode") in ["h", "high"]:
            ljinux.devices["ov3660"] = espcamera.Camera(
                data_pins=board.D,
                pixel_clock_pin=board.PCLK,
                vsync_pin=board.VSYNC,
                href_pin=board.HREF,
                i2c=board.SSCB_I2C(),
                external_clock_pin=board.XCLK,
                external_clock_frequency=20_000_000,
                powerdown_pin=None,
                reset_pin=board.RESET,
                pixel_format=espcamera.PixelFormat.JPEG,
                frame_size=espcamera.FrameSize.QXGA,
                jpeg_quality=2,
                framebuffer_count=1,
                grab_mode=espcamera.GrabMode.LATEST,
            )
            term.write('Initializing camera on mode "high"')
        else:
            ljinux.devices["ov3660"] = espcamera.Camera(
                data_pins=board.D,
                pixel_clock_pin=board.PCLK,
                vsync_pin=board.VSYNC,
                href_pin=board.HREF,
                i2c=board.SSCB_I2C(),
                external_clock_pin=board.XCLK,
                external_clock_frequency=20_000_000,
                powerdown_pin=None,
                reset_pin=board.RESET,
                pixel_format=espcamera.PixelFormat.JPEG,
                frame_size=espcamera.FrameSize.VGA,
                jpeg_quality=6,
                framebuffer_count=1,
                grab_mode=espcamera.GrabMode.LATEST,
            )
            term.write('Initializing camera on mode "low"')
        ljinux.devices["ov3660"].vflip = True
        sleep(2)
        term.write("Initialized!")
    else:
        term.write("Camera already initialized.")

if "capture" in vr("opts")["o"] or "c" in vr("opts")["o"]:
    vr("photo_data", ljinux.devices["ov3660"].take())
    term.write('Snapped!\nSaving to "', end="")
    vr("tt", time.localtime())
    vr("pic_name", "M5X-")
    if vr("tt").tm_mday < 10:
        vrp("pic_name", "0")
    vrp("pic_name", str(vr("tt").tm_mday) + "-")
    if vr("tt").tm_mon < 10:
        vrp("pic_name", "0")
    vrp("pic_name", str(vr("tt").tm_mon) + "-" + str(vr("tt").tm_year) + "-")
    if vr("tt").tm_sec < 10:
        vrp("pic_name", "0")
    vrp("pic_name", str(vr("tt").tm_sec) + ".jpeg")
    term.write(vr("pic_name") + '"...')
    with ljinux.api.fopen(vr("pic_name"), "wb") as pv[get_pid()]["f"]:
        vr("f").write(vr("photo_data"))
    term.write("Saved!")

# if "serve" in vr("opts")["o"] or "s" in vr("opts")["o"]:
#    if "ov3660" not in ljinux.devices:
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
    if "ov3660" not in ljinux.devices:
        term.write("Camera not initialized.")
    else:
        ljinux.devices["ov3660"].deinit()
        del ljinux.devices["ov3660"], espcamera

if not len(vr("opts")["o"]) or "h" in vr("opts")["o"] or "help" in vr("opts")["o"]:
    term.write("help menu here")
