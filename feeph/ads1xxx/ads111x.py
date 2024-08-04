#!/usr/bin/env python3
"""
ADS111x - Ultra-Small, Low-Power, I2C-Compatible, 860-SPS, 16-Bit ADCs
          With Internal Reference, Oscillator, and Programmable Comparator

datasheet: https://www.ti.com/lit/ds/symlink/ads1115.pdf
"""

import logging
from abc import ABC, abstractmethod

LH = logging.getLogger('feeph.ads1xxx')


class Ads111x(ABC):
    """

    """

    @abstractmethod
    def get_measurement(self) -> int:
        ...
