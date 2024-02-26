rename_process("camera")
import espcamera

vr("opts", be.api.xarg())

vr(
    "dev",
    cptoml.fetch("device", toml=be.api.betterpath("/etc/camera.d/config.toml")),
)

if "init" in vr("opts")["o"] or "i" in vr("opts")["o"]:
    be.api.setvar("return", "1")
    if vr("dev") not in be.devices:
        vr("conft", be.api.betterpath("/etc/camera.d/config.toml"))
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
                    toml=vr("conft"),
                ),
            )
        vr("pr", be.api.betterpath("/etc/camera.d/presets/" + vr("mode") + ".toml"))
        exec(
            'vr("px", espcamera.PixelFormat.'
            + cptoml.fetch(
                "pixel_format",
                toml=be.api.betterpath(vr("pr")),
            )
            + ")"
        )
        exec(
            'vr("fr", espcamera.FrameSize.'
            + cptoml.fetch(
                "frame_size",
                toml=be.api.betterpath(vr("pr")),
            )
            + ")"
        )
        vr(
            "qual",
            cptoml.fetch(
                "jpeg_quality",
                toml=be.api.betterpath(vr("pr")),
            ),
        )
        vr(
            "data_pins",
            cptoml.fetch(
                "data_pins",
                toml=vr("conft"),
            ),
        )
        vr(
            "pixel_clock_pin",
            cptoml.fetch(
                "pixel_clock_pin",
                toml=vr("conft"),
            ),
        )
        vr(
            "vsync_pin",
            cptoml.fetch(
                "vsync_pin",
                toml=vr("conft"),
            ),
        )
        vr(
            "href_pin",
            cptoml.fetch(
                "href_pin",
                toml=vr("conft"),
            ),
        )
        vr(
            "i2c",
            cptoml.fetch(
                "i2c",
                toml=vr("conft"),
            ),
        )
        vr(
            "external_clock_pin",
            cptoml.fetch(
                "external_clock_pin",
                toml=vr("conft"),
            ),
        )
        vr(
            "external_clock_frequency",
            cptoml.fetch(
                "external_clock_frequency",
                toml=vr("conft"),
            ),
        )
        vr(
            "powerdown_pin",
            cptoml.fetch(
                "powerdown_pin",
                toml=vr("conft"),
            ),
        )
        vr(
            "reset_pin",
            cptoml.fetch(
                "reset_pin",
                toml=vr("conft"),
            ),
        )
        be.devices[vr("dev")] = []
        be.devices[vr("dev")].append(
            espcamera.Camera(
                data_pins=be.devices["gpiochip"][0].pin(vr("data_pins"), force=True),
                pixel_clock_pin=be.devices["gpiochip"][0].pin(
                    vr("pixel_clock_pin"), force=True
                ),
                vsync_pin=be.devices["gpiochip"][0].pin(vr("vsync_pin"), force=True),
                href_pin=be.devices["gpiochip"][0].pin(vr("href_pin"), force=True),
                i2c=be.devices["gpiochip"][0].pin(vr("i2c"), force=True)(),
                external_clock_pin=be.devices["gpiochip"][0].pin(
                    vr("external_clock_pin"), force=True
                ),
                external_clock_frequency=vr("external_clock_frequency"),
                powerdown_pin=be.devices["gpiochip"][0].pin(
                    vr("powerdown_pin"), force=True
                ),
                reset_pin=be.devices["gpiochip"][0].pin(vr("reset_pin"), force=True),
                pixel_format=vr("px"),
                frame_size=vr("fr"),
                jpeg_quality=vr("qual"),
                framebuffer_count=1,
                grab_mode=espcamera.GrabMode.LATEST,
            )
        )
        term.write('Initializing camera on mode "' + vr("mode") + '"')
        be.devices[vr("dev")][0].vflip = True
        be.devices[vr("dev")][0].denoise = cptoml.fetch(
            "denoise",
            toml=be.api.betterpath(vr("pr")),
        )
        be.devices[vr("dev")][0].awb_gain = True
        sleep(0.5)
        be.devices[vr("dev")][0].take()
        term.write("Initialized!")
        be.api.setvar("return", "0")
    else:
        term.write("Camera already initialized.")

if "capture" in vr("opts")["o"] or "c" in vr("opts")["o"]:
    be.api.setvar("return", "1")
    if vr("dev") not in be.devices:
        term.write("Camera not initialized.")
    else:
        vr("photo_data", be.devices[vr("dev")][0].take(0.4))
        vr("ql", be.devices[vr("dev")][0].quality)
        while not isinstance(vr("photo_data"), memoryview):
            if be.devices[vr("dev")][0].quality < 20:
                be.devices[vr("dev")][0].quality += 1
            vr("photo_data", be.devices[vr("dev")][0].take(0.4))
        term.write(
            'Snapped! Quality={}\nSaving to "'.format(be.devices[vr("dev")][0].quality),
            end="",
        )
        be.devices[vr("dev")][0].quality = vr("ql")
        vr("tt", time.localtime())
        vr(
            "branding",
            cptoml.fetch(
                "branding",
                toml=be.api.betterpath("/etc/camera.d/config.toml"),
            ),
        )
        vr("pic_name", vr("branding") + "-")
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
            with be.api.fopen(vr("pic_name"), "wb") as pv[get_pid()]["f"]:
                vr("f").write(vr("photo_data"))
        term.write("Saved!")
        be.api.setvar("return", "0")

if "deinit" in vr("opts")["o"] or "d" in vr("opts")["o"]:
    be.api.setvar("return", "1")
    if vr("dev") not in be.devices:
        term.write("Camera not initialized!")
    else:
        be.devices[vr("dev")][0].deinit()
        be.devices[vr("dev")].pop()
        if not len(be.devices[vr("dev")]):
            del be.devices[vr("dev")], espcamera
        term.write("Camera deinitialized successfully.")
        be.api.setvar("return", "0")

if not len(vr("opts")["o"]) or "h" in vr("opts")["o"] or "help" in vr("opts")["o"]:
    be.based.run("cat /usr/share/help/camera.txt")
    be.api.setvar("return", "0")
