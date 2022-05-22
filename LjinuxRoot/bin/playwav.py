global NoAudio
if not NoAudio:
    try:
        with open(ljinux.based.user_vars["argj"].split()[1], "rb") as data:
            wav = WaveFile(data)
            a = PWMAudioOut(board.GP15)
            print("Playing")
            try:
                a.play(wav)
                while a.playing:
                    time.sleep(0.2)
            except KeyboardInterrupt:
                a.stop()
            a.deinit()
            wav.deinit()
            print("Stopped")
    except OSError:
        ljinux.based.error(4)
else:
    print("No audio libraries loaded")
