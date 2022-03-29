from sys import stdout, stdin
from supervisor import runtime


class jcurses:
    def __init__(self):
        self.enabled = False  # jcurses has init'ed
        self.softquit = False  # internal bool to signal exiting
        self.reset = False  # set to true to hard reset jcurses
        self.text_stepping = (
            0  # handy variable to make multi-action keys easily parsable
        )
        self.ctx_dict = {"zero": [1, 1]}  # bookmarks baby, bookmarks
        self.trigger_dict = None
        self.dmtex_suppress = False
        self.context = []
        self.buf = [0, ""]
        self.focus = 0
        """
            trigger_dict : What to do when what key along with other intructions.
            
            trigger_dict values:
                "inp_type": Can be: prompt / line / multiline / graphical, prompt needs a "prefix"
                "*any value from char_map*": exit the program with the value as an exit code.
                    For instance: "enter": 1. The program will exit when enter is pressed with exit code 1.
                "rest": what to do with the rest of keys, type string, can be "stack" / "ignore"
                "rest_a": allowed keys to be parsed with "rest", not neccessary if rest is set to ignore.
                    Valid values: "all" / "lettersnumbers" / "numbers" / "letters" / "common".
                "echo": Can be "all" / "common" / "none".
            """

    char_map = {  # you need to add 0x
        "61": "a",  # smol letters
        "62": "b",
        "63": "c",
        "64": "d",
        "65": "e",
        "66": "f",
        "67": "g",
        "68": "h",
        "69": "i",
        "6a": "j",
        "6b": "k",
        "6c": "l",
        "6d": "m",
        "6e": "n",
        "6f": "o",
        "70": "p",
        "71": "q",
        "72": "r",
        "73": "s",
        "74": "t",
        "75": "u",
        "76": "v",
        "77": "w",
        "78": "x",
        "79": "y",
        "7a": "z",
        "41": "A",  # capital letters
        "42": "B",
        "43": "C",
        "44": "D",
        "45": "E",
        "46": "F",
        "47": "G",
        "48": "H",
        "49": "I",
        "4a": "J",
        "4b": "K",
        "4c": "L",
        "4d": "M",
        "4e": "N",
        "4f": "O",
        "50": "P",
        "51": "Q",
        "52": "R",
        "53": "S",
        "54": "T",
        "55": "U",
        "56": "V",
        "57": "W",
        "58": "X",
        "59": "Y",
        "5a": "Z",
        "31": "1",  # numbers
        "32": "2",
        "33": "3",
        "34": "4",
        "35": "5",
        "36": "6",
        "37": "7",
        "38": "8",
        "39": "9",
        "30": "0",
        "60": "`",  # from here on out it's random chars I captured
        "2d": "-",
        "5f": "_",
        "3d": "=",
        "2b": "+",
        "5b": "[",
        "5d": "]",
        "5c": "\\",  # Never gonna give you up
        "2f": "/",  # Never gonna let you down
        "2e": ".",  # Never gonna run around and desert you
        "2c": ",",  # Never gonna make you cry
        "27": "'",  # Never gonna say goodbye
        "3b": ";",  # Never gonna tell a lie and hurt you
        "7b": "{",
        "7d": "}",
        "22": '"',
        "3a": ":",
        "7c": "|",
        "3f": "?",
        "3e": ">",
        "3c": "<",
        "1b": "alt",
        "20": " ",
        "a": "enter",
        "9": "tab",
        "7e": "~",
        "4": "ctrlD",
        "21": "!",
        "40": "@",
        "23": "#",
        "24": "$",
        "25": "%",
        "5e": "^",
        "26": "&",
        "2a": "*",
        "28": "(",
        "29": ")",
        "7f": "bck",
        "ctrlC": "ctrlC",  # needed
    }

    def backspace(self, n=1):
        for i in range(n):
            if len(self.buf[1]) - self.focus > 0:
                if self.focus == 0:
                    self.buf[1] = self.buf[1][:-1]
                    stdout.write("\010 \010")
                else:
                    stdout.write("\010")
                    insertion_pos = len(self.buf[1]) - self.focus - 1
                    self.buf[1] = (
                        self.buf[1][:insertion_pos] + self.buf[1][insertion_pos + 1 :]
                    )  # backend insertion
                    stdout.write(self.buf[1][insertion_pos:])  # frontend insertion
                    stdout.write(
                        " \x1b[{}D".format(len(self.buf[1][insertion_pos:]) + 1)
                    )  # go back
                    del insertion_pos

    def setout(self, cx, tx):
        """
        Used to set the text after a given point
        cx, is the x to consider as the start
        tx, is the text to put after that
        """
        pass

    def clear(self):
        """
        Clear the whole screen & goto top
        """
        stdout.write("\033[2J")
        stdout.write("\033[H")

    def clear_line(self):
        """
        Clear the current line
        """
        stdout.write("\033[2K")
        stdout.write("\033[500D")

    def start(self):
        """
        Start the Jcurses system.
        """
        if self.enabled:
            self.stop()
        self.enabled = True
        self.dmtex_suppress = True
        self.clear()

    def stop(self):
        """
        Stop the Jcurses system & reset to the default state.
        """
        self.clear(self)
        self.dmtex_suppress = False
        self.enabled = False
        self.softquit = False
        self.reset = False
        self.text_stepping = 0
        self.ctx_dict = {"zero": [1, 1]}
        self.trigger_dict = None
        self.dmtex_suppress = False

    def detect_size(self):
        strr = ""
        self.get_hw(0)
        self.get_hw(1)
        self.get_hw(2)
        while not strr.endswith("R"):
            strr += self.get_hw(3)
        strr = strr[2:-1]  # this is critical as find will break with <esc>.
        return [int(strr[: strr.find(";")]), int(strr[strr.find(";") + 1 :])]

    def detect_pos(self):
        strr = ""
        self.get_hw(1)
        while not strr.endswith("R"):
            strr += self.get_hw(3)
        strr = strr[2:-1]  # this is critical as find will break with <esc>.
        return [int(strr[: strr.find(";")]), int(strr[strr.find(";") + 1 :])]

    def get_hw(self, act):
        if act is 0:  # clear & to the end
            self.clear()
            stdout.write("\033[500B")  # down & forward, to go to the end
            stdout.write("\033[500C")
        elif act is 1:  # ask position
            stdout.write("\033[6n")  # get ending position
        elif act is 2:  # go back to top
            self.clear()
        elif act is 3:  # get pos
            return stdin.read(1)

    def train_mode(self):  # get the chars you inputted
        try:
            while True:
                a = self.register_char()
                if a != []:
                    for i in a:
                        print(i)
        except KeyboardInterrupt:
            return

    def register_char(self):
        """
        Complete all-in-one input character registration function.
        Returns list of input.
        Usually it's a list of one item, but if too much is inputted at once
        (for example, you are pasting text)
        it will all come in one nice bundle. This is to improve performance & compatibility with advanced keyboard features.

        You need to loop this in a while true.
        """
        stack = []
        try:
            n = runtime.serial_bytes_available  # do we have anythin?
            if n > 0:  # we do
                i = stdin.read(n)
                for s in i:
                    try:
                        charr = str(hex(ord(s)))[
                            2:
                        ]  # I tried to fix this 4 times. Watch this number go up. - lol I made it longer 19/3/22
                        if (
                            charr != "1b" and self.text_stepping is 0
                        ):  # if it's not an alt, or if we were proccessing something
                            stack.append(self.char_map[charr])
                        elif (
                            self.text_stepping is 0
                        ):  # skipping over the alt, dw it's not lost
                            self.text_stepping = 1
                        elif (
                            self.text_stepping is 1
                        ):  # we have passed the alt key, time to check it
                            if charr != "5b":  # not an arrow key
                                self.text_stepping = 0
                                stack.append("alt")
                                stack.append(self.char_map[charr])
                            else:  # it's an arrow key
                                self.text_stepping = 2
                        elif self.text_stepping is 2:  # time to get the arrow key
                            res = ""
                            if charr == "41":
                                res = "up"
                            elif charr == "42":
                                res = "down"
                            elif charr == "43":
                                res = "right"
                            elif charr == "44":
                                res = "left"
                            self.text_stepping = 0
                            stack.append(res)
                            del res
                    except KeyError:
                        pass
                    except KeyboardInterrupt:
                        stack.append("ctrlC")
        except KeyboardInterrupt:
            stack.append("ctrlC")  # yes this has to be done twice.
        return stack

    def program(self):
        """
        The main program.
        Depends on variables being already set.
        """
        self.softquit = False
        segmented = False
        self.buf[0] = 0
        if self.trigger_dict["inp_type"] == "prompt":  # a terminal prompt
            self.termline()
            while not self.softquit:
                tempstack = self.register_char()
                if len(tempstack) > 0:
                    for i in tempstack:
                        if i == "alt":
                            pass
                        elif segmented:
                            pass
                        elif i in self.trigger_dict:
                            self.buf[0] = self.trigger_dict[i]
                            self.softquit = True
                        elif i == "bck":
                            self.backspace()
                        elif i == "up":
                            pass
                        elif i == "left":
                            if len(self.buf[1]) > self.focus:
                                stdout.write("\010")
                                self.focus += 1
                        elif i == "right":
                            if self.focus > 0:
                                stdout.write("\x1b[1C")
                                self.focus -= 1
                        elif i == "down":
                            pass
                        elif i == "tab":
                            pass
                        elif self.trigger_dict["rest"] == "stack" and (
                            self.trigger_dict["rest_a"] == "common"
                            and i != "alt"
                            and i != "ctrl"
                            and i != "ctrlD"
                        ):  # Arknights "PatriotExtra" theme starts playing
                            if self.focus is 0:
                                self.buf[1] += i
                                if (
                                    self.trigger_dict["echo"] == "common"
                                    or self.trigger_dict["echo"] == "all"
                                ):
                                    stdout.write(i)
                            else:
                                insertion_pos = len(self.buf[1]) - self.focus
                                self.buf[1] = (
                                    self.buf[1][:insertion_pos]
                                    + i
                                    + self.buf[1][insertion_pos:]
                                )  # backend insertion
                                steps_in = 0
                                for d in self.buf[1][
                                    insertion_pos:
                                ]:  # frontend insertion
                                    stdout.write(d)
                                    steps_in += 1
                                for e in range(steps_in - 1):
                                    stdout.write("\010")
                                del steps_in
                                del insertion_pos
                del tempstack
        del segmented
        return self.buf

    def termline(self):
        self.clear_line()
        print(self.trigger_dict["prefix"] + " " + self.buf[1], end="")
        if self.focus > 0:
            stdout.write("\x1b[{}D".format(self.focus))

    def gotoo(self, ctx, number=0):
        pass

    def ctx_reg(self, namee):
        self.ctx_dict[namee] = [
            0,
            0,
        ]  # addfahsdjhfasdfsadgfshdgfshdavfasjkdfvsdjakafvdhkvhjvfkashdvjfshvkhv
