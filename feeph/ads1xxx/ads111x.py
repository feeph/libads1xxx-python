#!/usr/bin/env python3
"""
abstract base class for ADS1113, ADS1114 and ADS1115
"""

from abc import ABC, abstractmethod

from attrs import define

from feeph.ads1xxx.conversions import UNIT
from feeph.ads1xxx.settings import CLAT, CMOD, CPOL, CQUE, DOM, DRS, MUX, PGA, SSC


@define
class Ads111xConfig:
    """
    common settings for ADS1113, ADS1114 and ADS1115

    (derive from this dataclass to add device specific config options)
    """
    ssc: SSC = SSC.NO_OP
    dom: DOM = DOM.SSM
    drs: DRS = DRS.MODE4

    def as_uint16(self):
        # non-configurable values are set to their default
        value = 0b0000_0000_0000_0000
        value |= self.ssc.value
        value |= MUX.MODE0
        value |= PGA.MODE2
        value |= self.dom.value
        value |= self.drs.value
        value |= CMOD.TRD
        value |= CPOL.ALO
        value |= CLAT.NLC
        value |= CQUE.DIS
        return value


class Ads111x(ABC):

    @abstractmethod
    def reset_device_registers(self):
        ...

    @abstractmethod
    def get_singleshot_measurement(self, config: Ads111xConfig | None, unit: UNIT = UNIT.MICRO) -> int:
        ...
