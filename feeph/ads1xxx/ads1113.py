#!/usr/bin/env python3
"""
ADS111x - Ultra-Small, Low-Power, I2C-Compatible, 860-SPS, 16-Bit ADCs
          With Internal Reference, Oscillator, and Programmable Comparator

datasheet: https://www.ti.com/lit/ds/symlink/ads1115.pdf
"""

import logging

from attrs import define

from feeph.ads1xxx.ads111x import Ads111x, Ads111xConfig
from feeph.ads1xxx.settings import CLAT, CMOD, CPOL, CQUE, DOM, DRS, MUX, PGA, SSC

LH = logging.getLogger('feeph.ads1xxx')


@define
class Ads1113Config(Ads111xConfig):
    """
    The 16-bit Config register is used to control the operating mode, input
    selection, data rate, full-scale range, and comparator modes.
    """
    # fmt: off
    ssc: SSC = SSC.NO_OP  # single-shot conversion trigger
    dom: DOM = DOM.SSM    # device operation mode
    drs: DRS = DRS.MODE4  # data rate setting
    # fmt: on

    def as_uint16(self):
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


class Ads1113(Ads111x):
    """
    ADS1113 - Ultra-Small, Low-Power, I2C-Compatible, 860-SPS, 16-Bit ADCs
            With Internal Reference, Oscillator, and Programmable Comparator

    datasheet: https://www.ti.com/lit/ds/symlink/ads1113.pdf
    """
    _has_pga = False
