from sys import stdout, stdin
from supervisor import runtime
from jcurses_data import char_map
from usb_cdc import console
from time import sleep

ESCK = "\033["


class jcurses:
    def __init__(self):
        self.enabled = False  # jcurses has init'ed
        self.softquit = False  # internal bool to signal exiting
        self.reset = False  # set to true to hard reset jcurses
        self.text_stepping = (
            0  # handy variable to make multi-action keys easily parsable
        )
        self.ctx_dict = {"top_left": [1, 1], "bottom_left": [1, 1]}  # bookmarks baby, bookmarks
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
                        ESCK + "{}D".format(len(self.buf[1][insertion_pos:]) + 1)
                    )  # go back
                    del insertion_pos

    def clear(self):
        """
        Clear the whole screen & goto top
        """
        stdout.write(ESCK + "2J")
        stdout.write(ESCK + "H")

    def clear_line(self):
        """
        Clear the current line
        """
        stdout.write(ESCK + "2K")
        stdout.write(ESCK + "500D")

    def start(self):
        """
        Start the Jcurses system.
        """
        if self.enabled:
            self.stop()
        self.enabled = True
        self.dmtex_suppress = True
        self.detect_size() # don't need it as by itself, I only want it to update the bookmarks.
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
        """
        detect terminal size, returns [rows, collumns]
        """
        done = False
        while not done: # this whole ass fiasco is to combat user input during the ansi negotiation.
            try:
                strr = ""
                while not console.connected:
                    sleep(.3)
                for i in range(3):
                    self.get_hw(i)
                while not strr.endswith("R"):
                    strr += self.get_hw(3)
                strr = strr[2:-1]  # this is critical as find will break with <esc>.
                res = [int(strr[: strr.find(";")]), int(strr[strr.find(";") + 1 :])]
                # Let's also update the move bookmarks.
                self.ctx_dict["bottom_left"] = [res[0], 1]
                done = True
            except ValueError:
                pass
        # Now let's return with the result.
        del done
        return res

    def detect_pos(self):
        strr = ""
        self.get_hw(1)
        while not strr.endswith("R"):
            strr += self.get_hw(3)
        strr = strr[2:-1]  # this is critical as find will break with <esc>.
        return [int(strr[: strr.find(";")]), int(strr[strr.find(";") + 1 :])]

    def get_hw(self, act):
        if act is 0:
            # save pos & goto the end
            stdout.write(ESCK + "s" + ESCK + "500B" + ESCK + "500C")
        elif act is 1:
            # ask position
            stdout.write(ESCK + "6n")
        elif act is 2:
            # go back to original position
            stdout.write(ESCK + "u")
        elif act is 3:
            # get it
            return stdin.read(1)

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
            n = runtime.serial_bytes_available
            if n > 0:
                i = stdin.read(n)
                for s in i:
                    try:
                        charr = str(hex(ord(s)))[2:]
                        # Check for alt or process
                        if self.text_stepping is 0:
                            if charr != "1b":
                                stack.append(char_map[charr])
                            else:
                                self.text_stepping = 1

                        # Check skipped alt
                        elif self.text_stepping is 1:
                            if charr != "5b":
                                self.text_stepping = 0
                                stack.extend(["alt", char_map[charr]])
                            else:  # it's an arrow key
                                self.text_stepping = 2

                        # Arrow keys
                        else:
                            self.text_stepping = 0
                            stack.append(char_map[charr])
                    except KeyError:
                        pass
        except KeyboardInterrupt:
            stack = ["ctrlC"]
        return stack

    def program(self):
        """
        The main program.
        Depends on variables being already set.
        """
        self.softquit = segmented = False
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
                                stdout.write(ESCK + "1C")
                                self.focus -= 1
                        elif i == "down":
                            pass
                        elif i == "tab":
                            pass
                        elif self.trigger_dict["rest"] == "stack" and (
                            self.trigger_dict["rest_a"] == "common"
                            and i not in {"alt", "ctrl", "ctrlD"}
                        ):  # Arknights "PatriotExtra" theme starts playing
                            if self.focus is 0:
                                self.buf[1] += i
                                if self.trigger_dict["echo"] in {"common", "all"}:
                                    stdout.write(i)
                            else:
                                insertion_pos = (
                                    len(self.buf[1]) - self.focus
                                )  # backend insertion
                                self.buf[1] = (
                                    self.buf[1][:insertion_pos]
                                    + i
                                    + self.buf[1][insertion_pos:]
                                )
                                # frontend insertion
                                for d in self.buf[1][insertion_pos:]:
                                    stdout.write(d)
                                steps_in = len(self.buf[1][insertion_pos:])
                                for e in range(steps_in - 1):
                                    stdout.write("\010")
                                del steps_in, insertion_pos
                del tempstack
        del segmented
        return self.buf

    def termline(self):
        print(self.trigger_dict["prefix"], self.buf[1], end="")
        if self.focus > 0:
            stdout.write(ESCK + str(self.focus) + "D")

    def move(self, ctx=None, x=None, y=None):
        """
        Move to a specified coordinate or a bookmark.
        If you specified a bookmark, you can use x & y to add an offset.
        """
        if ctx is None:
            if x is not None and y is not None:
                x, y = max(1, x), max(1, y)
                stdout.write(ESCK + str(x) + ";" + str(y) + "H")
        else:
            # no try except here, errors here are the user's fault
            thectx = self.ctx_dict[ctx]
            stdout.write(ESCK + str(thectx[0]) + ";" + str(thectx[1]) + "H")
            if x is not None:
                if x + thectx[0] > 0:  # out of bounds check
                    if thectx[0] > 0:  # down
                        stdout.write(ESCK + str(thectx[0]) + "B")
                    else:  # up
                        stdout.write(ESCK + str(-thectx[0]) + "A")
            if y is not None:
                if y + thectx[1] > 0:  # out of bounds check
                    if thectx[1] > 0:  # right
                        stdout.write(ESCK + str(thectx[1]) + "C")
                    else:  # left
                        stdout.write(ESCK + str(-thectx[1]) + "D")
            del thectx

    def ctx_reg(self, namee):
        self.ctx_dict[namee] = self.detect_pos()
    
    def line(self, charr):
        self.clear_line()
        stdout.write(charr * self.detect_size()[1])
