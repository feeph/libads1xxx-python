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
class Ads1114Config(Ads111xConfig):
    """
    The 16-bit Config register is used to control the operating mode, input
    selection, data rate, full-scale range, and comparator modes.
    """
    # fmt: off
    ssc:  SSC = SSC.NO_OP   # single-shot conversion trigger
    pga:  PGA  = PGA.MODE2  # programmable gain amplifier
    dom:  DOM = DOM.SSM     # device operation mode
    drs:  DRS = DRS.MODE4   # data rate setting
    cmod: CMOD = CMOD.TRD   # comparator mode
    cpol: CPOL = CPOL.ALO   # comparator polarity
    clat: CLAT = CLAT.NLC   # comparator latch
    cque: CQUE = CQUE.DIS   # comparator queue
    # fmt: on

    def as_uint16(self):
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


class Ads1114(Ads111x):
    """
    ADS1113 - Ultra-Small, Low-Power, I2C-Compatible, 860-SPS, 16-Bit ADCs
            With Internal Reference, Oscillator, and Programmable Comparator

    datasheet: https://www.ti.com/lit/ds/symlink/ads1114.pdf
    """
    _has_pga = True
