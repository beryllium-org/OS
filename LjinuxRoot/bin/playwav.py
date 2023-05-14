global NoAudio
if not NoAudio:
    try:
        with open(ljinux.based.user_vars["argj"].split()[1], "rb") as data:
            wav = WaveFile(data)
            a = PWMAudioOut(board.GP15)
            term.write("Playing")
            try:
                a.play(wav)
                while a.playing:
                    time.sleep(0.2)
            except KeyboardInterrupt:
                a.stop()
            a.deinit()
            wav.deinit()
            term.write("Stopped")
    except OSError:
        ljinux.based.error(4)
else:
    term.write("No audio libraries loaded")
