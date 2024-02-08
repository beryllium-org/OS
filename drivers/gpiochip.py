import board
import digitalio
import analogio
import touchio
import pwmio
import busio


class gpiochip:
    def __init__(self):
        self._pins = []

        for i in dir(board):
            if (i[0] != "_") and (i != "board_id"):
                self._pins.append(i)

    @property
    def pins(self) -> list:
        return self._pins.copy()

    def is_free(self, pin_name) -> bool:
        if isinstance(pin_name, str):
            try:
                tmpin = digitalio.DigitalInOut(getattr(board, pin_name))
                tmpin.deinit()
                return True
            except:
                return False
        else:
            try:
                tmpin = digitalio.DigitalInOut(pin_name)
                tmpin.deinit()
                return True
            except:
                return False

    def pin(self, pin_name: str, force: bool = False):
        try:
            pin = getattr(board, pin_name)
            if force or self.is_free(pin):
                return pin
        except:
            pass
        return None

    def input(self, pin_name: str):
        pin = self.pin(pin_name)
        if pin is not None:
            dig = digitalio.DigitalInOut(pin)
            try:
                dig.switch_to_input()
                return dig
            except:
                dig.deinit()
        return None

    def output(self, pin_name: str):
        pin = self.pin(pin_name)
        if pin is not None:
            dig = digitalio.DigitalInOut(pin)
            try:
                dig.switch_to_output()
                return dig
            except:
                dig.deinit()
        return None

    def adc(self, pin_name: str):
        pin = self.pin(pin_name)
        if pin is not None:
            try:
                return analogio.AnalogIn(pin)
            except:
                pass
        return None

    def touch(self, pin_name: str):
        pin = self.pin(pin_name)
        if pin is not None:
            try:
                return touchio.TouchIn(pin)
            except:
                pass
        return None

    def pwm(
        self,
        pin_name: str,
        frequency: int = 500,
        duty_cycle: int = 0,
    ):
        pin = self.pin(pin_name)
        if pin is not None:
            try:
                return pwmio.PWMOut(pin, frequency=frequency, duty_cycle=duty_cycle)
            except:
                pass
        return None

    def uart(
        self,
        pin_tx: str,
        pin_rx: str,
        baudate: int = 115200,
        bits: int = 8,
        parity=None,
        stop: int = 1,
    ):
        ptx = self.pin(pin_tx)
        rtx = self.pin(pin_rx)
        if ptx is not None and rtx is not None and ptx != rtx:
            return busio.UART(
                ptx, rtx, baudrate=baudate, bits=bits, parity=parity, stop=stop
            )
        return None

    def i2c(
        self, pin_scl: str, pin_sda: str, frequency: int = 100000, timeout: int = 255
    ):
        pcl = self.pin(pin_scl)
        pda = self.pin(pin_sda)
        if pcl is not None and pda is not None and pcl != pda:
            try:
                return busio.I2C(pcl, pda, frequency=frequency, timeout=timeout)
            except:
                pass
        return None
