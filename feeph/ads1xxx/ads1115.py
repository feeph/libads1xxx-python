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

from feeph.ads1xxx.ads111x import Ads111x

LH = logging.getLogger('feeph.ads1xxx')


@define
class Ads1115Config:
    """
    The 16-bit Config register is used to control the operating mode, input
    selection, data rate, full-scale range, and comparator modes.
    """
    # fmt: off
    OSSA:     int  # 0b#..._...._...._.... status or single shot start
    IMUX:     int  # 0b.###_...._...._.... input multiplexer configuration
    PGA:      int  # 0b...._###._...._.... programmable gain amplifier
    MODE:     int  # 0b...._...#_...._.... operating mode
    DR:       int  # 0b...._...._###._.... data rate
    COMP_MOD: int  # 0b...._...._...#_.... comparator mode
    COMP_POL: int  # 0b...._...._...._#... comparator polarity
    COMP_LAT: int  # 0b...._...._...._.#.. latching comparator
    COMP_QUE: int  # 0b...._...._...._..## comparator queue & disable
    # fmt: on


DEFAULTS = {
    0x01: 0x8583,
    0x02: 0x8000,
    0x03: 0x7FFF,
}


class Ads1115(Ads111x):
    # 0x00 - conversion register (2 bytes, ro, default: 0x0000)
    # 0x01 - config register     (2 bytes, rw, default: 0x8583)
    # 0x10 - lo_thresh register  (2 bytes, rw, default: 0x0080)
    # 0x11 - hi_thresh register  (2 bytes, rw, default: 0xFF7F)

    def __init__(self, i2c_bus: busio.I2C):
        self._i2c_bus = i2c_bus
        self._i2c_adr = 0x48  # the I²C bus address is hardcoded

    def get_config(self) -> Ads1115Config:
        with BurstHandler(i2c_bus=self._i2c_bus, i2c_adr=self._i2c_adr) as bh:
            value = bh.read_register(0x01, byte_count=2)
        params = {
            "OSSA":     value & 0b1000_0000_0000_0000,
            "IMUX":     value & 0b0111_0000_0000_0000,
            "PGA":      value & 0b0000_1110_0000_0000,
            "MODE":     value & 0b0000_0001_0000_0000,
            "DR":       value & 0b0000_0000_1110_0000,
            "COMP_MOD": value & 0b0000_0000_0001_0000,
            "COMP_POL": value & 0b0000_0000_0000_1000,
            "COMP_LAT": value & 0b0000_0000_0000_0100,
            "COMP_QUE": value & 0b0000_0000_0000_0011,
        }
        return Ads1115Config(**params)

    def set_config(self, config: Ads1115Config):
        value = 0b0000_0000_0000_0000
        value &= config.OSSA
        value &= config.IMUX
        value &= config.PGA
        value &= config.MODE
        value &= config.DR
        value &= config.COMP_MOD
        value &= config.COMP_POL
        value &= config.COMP_LAT
        value &= config.COMP_QUE
        with BurstHandler(i2c_bus=self._i2c_bus, i2c_adr=self._i2c_adr) as bh:
            bh.write_register(0x01, value, byte_count=2)

    def reset_device_registers(self):
        with BurstHandler(i2c_bus=self._i2c_bus, i2c_adr=self._i2c_adr) as bh:
            for register, value in DEFAULTS.items():
                bh.write_register(register, value, byte_count=2)

    # ---------------------------------------------------------------------

    def get_measurement(self) -> int:
        return 0

    # ---------------------------------------------------------------------
