import board
import digitalio
import microcontroller
import sys
import os

try:
    import wifi
except ImportError:
    pass

print("\x1b[2J\x1b[3J\x1b[HWelcome to the ljinux REPL environment!")
