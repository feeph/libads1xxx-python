#!/usr/bin/env python3
"""
ADS1013 - Ultra-Small, Low-Power, I2C-Compatible, 3.3-kSPS, 12-Bit ADCs
          With Internal Reference, Oscillator

datasheet: https://www.ti.com/lit/ds/symlink/ads1013.pdf
"""

import logging

from attrs import define

from feeph.ads1xxx.ads1x1x import Ads1x1x, Ads1x1xConfig
from feeph.ads1xxx.conversions import UNIT, convert_step_to_value
from feeph.ads1xxx.settings import CLAT, CMOD, CPOL, CQUE, DOM, DRS, MUX, PGA, SSC

LH = logging.getLogger('feeph.ads1xxx')


@define
class Ads1013Config(Ads1x1xConfig):
    # fmt: off
    ssc: SSC = SSC.NO_OP  # single-shot conversion trigger
    dom: DOM = DOM.SSM    # device operation mode
    drs: DRS = DRS.MODE4  # data rate setting
    # fmt: on

    def as_uint16(self) -> int:
        # non-configurable values are set to their default
        value = 0b0000_0000_0000_0000
        value |= self.ssc.value
        value |= MUX.MODE0.value  # no input multiplexer
        value |= PGA.MODE2.value  # no programmable gain amplifier
        value |= self.dom.value
        value |= self.drs.value
        value |= CMOD.TRD.value   # no comparator mode
        value |= CPOL.ALO.value   # no comparator polarity
        value |= CLAT.NLC.value   # no comparator latch
        value |= CQUE.DIS.value   # no comparator queue
        return value

    # technically it's possible to set the alert threshold registers but it
    # doesn't have any effect since there is no comparator which uses them

    def get_atlo(self, unit: UNIT = UNIT.MICRO) -> int:
        return convert_step_to_value(step=0x8000, unit=unit, pga=PGA.MODE2)

    def get_athi(self, unit: UNIT = UNIT.MICRO) -> int:
        return convert_step_to_value(step=0x7FFF, unit=unit, pga=PGA.MODE2)


class Ads1013(Ads1x1x):
    _has_pga = False
