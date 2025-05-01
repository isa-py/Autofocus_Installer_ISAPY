import os
import time

class Focuser:
    CHIP_I2C_ADDR = 0x0C
    OPT_BASE    = 0x1000
    OPT_FOCUS   = OPT_BASE | 0x01

    opts = {
        OPT_FOCUS : {
            "MIN_VALUE": 0,
            "MAX_VALUE": 1000,
            "DEF_VALUE": 0,
        },
    }

    def __init__(self, bus):
        self.bus = bus
        self.focus_value = 0

    def read(self):
        return self.focus_value

    def write(self, chip_addr, value):
        value = max(0, value)
        self.focus_value = value
        value = (value << 4) & 0x3FF0
        data1 = (value >> 8) & 0x3F
        data2 = value & 0xF0
        os.system(f"i2cset -y {self.bus} 0x{chip_addr:02X} {data1} {data2}")

    def reset(self, opt, flag=1):
        info = self.opts.get(opt)
        if info and info.get("DEF_VALUE") is not None:
            self.set(opt, info["DEF_VALUE"])

    def get(self, opt, flag=0):
        return self.read()

    def set(self, opt, value, flag=1):
        info = self.opts.get(opt)
        if info is None:
            return
        min_val = info.get("MIN_VALUE", 0)
        max_val = info.get("MAX_VALUE", 1000)
        value = min(max(value, min_val), max_val)
        self.write(self.CHIP_I2C_ADDR, value)
        print(f"[Focuser] write: {value}")