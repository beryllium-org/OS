from os import system, mkdir, listdir, uname

mpyn = f"../mpy-crosses/mpy-cross-{uname().machine}"

print(f"\nUsing mpycross: {mpyn}")

print("[1/1] Compiling source files and pin allocation tabs\n")
for filee in listdir():
    if filee.endswith(".py"):
        print(f"-> {filee[:-3]}")
        system(f"{mpyn} ./{filee} -s {filee[:-3]} -v -O4 -o /dev/null")

print()
del mpyn
