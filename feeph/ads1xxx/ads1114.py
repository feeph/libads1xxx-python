#!/usr/bin/env python3
"""
ADS1114 - Ultra-Small, Low-Power, I2C-Compatible, 860-SPS, 16-Bit ADCs
          With Internal Reference, Oscillator, and Programmable Comparator

datasheet: https://www.ti.com/lit/ds/symlink/ads1114.pdf
"""

import logging

from attrs import define

from feeph.ads1xxx.ads1x1x import Ads1x1x, Ads1x1xConfig
from feeph.ads1xxx.conversions import UNIT, convert_step_to_value, convert_value_to_step
from feeph.ads1xxx.settings import CLAT, CMOD, CPOL, CQUE, DOM, DRS, MUX, PGA, SSC

LH = logging.getLogger('feeph.ads1xxx')


@define
class Ads1114Config(Ads1x1xConfig):
    # fmt: off
    ssc:  SSC = SSC.NO_OP   # single-shot conversion trigger
    pga:  PGA  = PGA.MODE2  # programmable gain amplifier
    dom:  DOM = DOM.SSM     # device operation mode
    drs:  DRS = DRS.MODE4   # data rate setting
    cmod: CMOD = CMOD.TRD   # comparator mode
    cpol: CPOL = CPOL.ALO   # comparator polarity
    clat: CLAT = CLAT.NLC   # comparator latch
    cque: CQUE = CQUE.DIS   # comparator queue
    atlo: int = 0x8000      # alert threshold low (-32768)
    athi: int = 0x7FFF      # alert threshold high (32767)
    # fmt: on

    def as_uint16(self) -> int:
        value = 0b0000_0000_0000_0000
        value |= self.ssc.value
        value |= MUX.MODE0.value  # no input multiplexer
        value |= self.pga.value
        value |= self.dom.value
        value |= self.drs.value
        value |= self.cmod.value
        value |= self.cpol.value
        value |= self.clat.value
        value |= self.cque.value
        return value

    def get_atlo(self, unit: UNIT = UNIT.MICRO) -> int:
        return convert_step_to_value(step=self.atlo, unit=unit, pga=self.pga)

    def set_atlo(self, value: int, unit: UNIT = UNIT.MICRO) -> bool:
        try:
            self.atlo = convert_value_to_step(value=value, unit=unit, pga=self.pga)
            return True
        except ValueError:
            return False

    def get_athi(self, unit: UNIT = UNIT.MICRO) -> int:
        return convert_step_to_value(step=self.athi, unit=unit, pga=self.pga)

    def set_athi(self, value: int, unit: UNIT = UNIT.MICRO) -> bool:
        try:
            self.athi = convert_value_to_step(value=value, unit=unit, pga=self.pga)
            return True
        except ValueError:
            return False


class Ads1114(Ads1x1x):
    _has_pga = True
