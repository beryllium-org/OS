global NoAudio
if not NoAudio:
    try:
        with open(ljinux.based.user_vars["argj"].split()[1], "rb") as data:
            mp3 = MP3Decoder(data)
            a = PWMAudioOut(board.GP15)
            term.write("Playing")
            try:
                a.play(mp3)
                while a.playing:
                    time.sleep(0.2)
            except KeyboardInterrupt:
                a.stop()
            a.deinit()
            mp3.deinit()
            term.write("Stopped")
            ljinux.based.user_vars["return"] = "0"
    except OSError:
        ljinux.based.error(4)
        ljinux.based.user_vars["return"] = "1"
else:
    term.write("No audio libraries loaded")
    ljinux.based.user_vars["return"] = "1"
