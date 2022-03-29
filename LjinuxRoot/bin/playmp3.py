global NoAudio
if not NoAudio:
    try:
        with open(ljinux.based.user_vars["argj"].split()[1], "rb") as data:
            mp3 = MP3Decoder(data)
            a = PWMAudioOut(board.GP15)
            print("Playing")
            try:
                a.play(mp3)
                while a.playing:
                    time.sleep(0.2)
                    if ljinux.io.buttone.value:
                        if a.playing:
                            a.pause()
                            print("Paused")
                            time.sleep(0.5)
                            while a.paused:
                                if (
                                    ljinux.io.buttonl.value
                                    and ljinux.io.buttonr.value
                                    and not ljinux.io.buttone.value
                                ):
                                    a.stop()
                                elif ljinux.io.buttone.value:
                                    a.resume()
                                    print("Resumed")
                                    time.sleep(0.5)
                                else:
                                    time.sleep(0.1)
            except KeyboardInterrupt:
                a.stop()
            a.deinit()
            mp3.deinit()
            print("Stopped")
            ljinux.based.user_vars["return"] = "0"
    except OSError:
        ljinux.based.error(4)
        ljinux.based.user_vars["return"] = "1"
else:
    print("No audio libraries loaded")
    ljinux.based.user_vars["return"] = "1"
