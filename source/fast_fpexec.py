def fast_fpexec(filee):
    try:
        try:
            with open(filee, "r") as f:
                a = f.read()
                f.close()
                del f
        except OSError:
            print("fast_fpexec: File not found")
            return
        exec(a)
        del a
    except Exception as err:
        print(
            "Traceback (most recent call last):\n\t"
            + str(type(err))[8:-2]
            + ": "
            + str(err)
        )
        del err
