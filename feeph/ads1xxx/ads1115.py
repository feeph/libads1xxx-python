#!/usr/bin/env python3
"""
ADS111x - Ultra-Small, Low-Power, I2C-Compatible, 860-SPS, 16-Bit ADCs
          With Internal Reference, Oscillator, and Programmable Comparator

datasheet: https://www.ti.com/lit/ds/symlink/ads1115.pdf
"""

import logging

# module busio provides no type hints
import busio  # type: ignore
from attrs import define
from feeph.i2c import BurstHandler

from feeph.ads1xxx.ads111x import Ads111x, Ads111xConfig
from feeph.ads1xxx.conversions import UNIT, convert_step_to_microvolts
from feeph.ads1xxx.settings import CLAT, CMOD, CPOL, CQUE, DOM, MUX, PGA, SSC

LH = logging.getLogger('feeph.ads1xxx')


@define
class Ads1115Config(Ads111xConfig):
    """
    The 16-bit Config register is used to control the operating mode, input
    selection, data rate, full-scale range, and comparator modes.
    """
    # fmt: off
    mux:  MUX  = MUX.MODE0
    pga:  PGA  = PGA.MODE2
    cmod: CMOD = CMOD.TRD
    cpol: CPOL = CPOL.ALO
    clat: CLAT = CLAT.NLC
    cque: CQUE = CQUE.DIS
    # fmt: on

    def as_uint16(self):
        value = 0b0000_0000_0000_0000
        value |= self.ssc.value
        value |= self.mux.value
        value |= self.pga.value
        value |= self.dom.value
        value |= self.drs.value
        value |= self.cmod.value
        value |= self.cpol.value
        value |= self.clat.value
        value |= self.cque.value
        return value


DEFAULTS = {
    0x00: None,    # conversion register (2 bytes, ro)
    0x01: 0x8583,  # config register     (2 bytes, rw)
    0x02: 0x8000,  # lo_thresh register  (2 bytes, rw)
    0x03: 0x7FFF,  # hi_thresh register  (2 bytes, rw)
}


class Ads1115(Ads111x):

    def __init__(self, i2c_bus: busio.I2C):
        self._i2c_bus = i2c_bus
        self._i2c_adr = 0x48  # the I²C bus address is hardcoded

    def reset_device_registers(self):
        with BurstHandler(i2c_bus=self._i2c_bus, i2c_adr=self._i2c_adr) as bh:
            for register, value in DEFAULTS.items():
                if value is None:
                    continue
                bh.write_register(register, value, byte_count=2)

    def get_singleshot_measurement(self, config: Ads111xConfig | Ads1115Config | None = None, unit: UNIT = UNIT.MICRO) -> int:
        with BurstHandler(i2c_bus=self._i2c_bus, i2c_adr=self._i2c_adr) as bh:
            if config is None:
                config_uint = bh.read_register(0x01, byte_count=2)
            else:
                config_uint = config.as_uint16()
            if config_uint & DOM.SSM.value:
                bh.write_register(0x01, config_uint | SSC.START.value, byte_count=2)
                # TODO wait until measurement is ready
                # (0b0..._...._...._.... -> 0b1..._...._...._....)
                step = bh.read_register(0x00, byte_count=2)
                if unit == UNIT.MICRO:
                    if isinstance(config, Ads1115):
                        # ADS1114 and ADS1115 have a programmable gain
                        # amplifier
                        return convert_step_to_microvolts(step, config.pga)
                    else:
                        # ADS1113 has a fixed voltage range of ±2.048V
                        return convert_step_to_microvolts(step, PGA.MODE2)
                else:
                    return step
            else:
                raise RuntimeError("device is configured for continuous conversion")
