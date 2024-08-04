#!/usr/bin/env python3
"""
abstract base class for ADS1113, ADS1114 and ADS1115
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

    @abstractmethod
    def reset_device_registers(self):
        ...
