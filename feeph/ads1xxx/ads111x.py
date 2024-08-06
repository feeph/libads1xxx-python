#!/usr/bin/env python3
"""
abstract base class for ADS1113, ADS1114 and ADS1115
"""

import logging
from abc import ABC, abstractmethod

# module busio provides no type hints
import busio  # type: ignore
from feeph.i2c import BurstHandler

from feeph.ads1xxx.conversions import UNIT, convert_step_to_microvolts
from feeph.ads1xxx.settings import DOM, PGA, SSC

LH = logging.getLogger('feeph.ads1xxx')


DEFAULTS = {
    0x00: None,    # conversion register (2 bytes, ro)
    0x01: 0x8583,  # config register     (2 bytes, rw)
    0x02: 0x8000,  # lo_thresh register  (2 bytes, rw)
    0x03: 0x7FFF,  # hi_thresh register  (2 bytes, rw)
}


class Ads111xConfig(ABC):

    @abstractmethod
    def as_uint16(self):
        ...


class Ads111x:
    _has_pga = False

    def __init__(self, i2c_bus: busio.I2C):
        self._i2c_bus = i2c_bus
        self._i2c_adr = 0x48  # the I²C bus address is hardcoded

    def reset_device_registers(self):
        with BurstHandler(i2c_bus=self._i2c_bus, i2c_adr=self._i2c_adr) as bh:
            for register, value in DEFAULTS.items():
                if value is None:
                    continue
                bh.write_register(register, value, byte_count=2)

    def get_singleshot_measurement(self, config: Ads111xConfig | None = None, unit: UNIT = UNIT.MICRO) -> int:
        with BurstHandler(i2c_bus=self._i2c_bus, i2c_adr=self._i2c_adr) as bh:
            if config is None:
                config_uint = bh.read_register(0x01, byte_count=2)
            else:
                config_uint = config.as_uint16()
            LH.warning("1: config_uint = 0x%08x", config_uint)
            if config_uint & DOM.SSM.value:
                bh.write_register(0x01, config_uint | SSC.START.value, byte_count=2)
                LH.warning("2: config_uint = 0x%08x", config_uint | SSC.START.value)
                # TODO wait until measurement is ready
                # (0b0..._...._...._.... -> 0b1..._...._...._....)
                step = bh.read_register(0x00, byte_count=2)
                if unit == UNIT.MICRO:
                    if self._has_pga:
                        pga_setting = config_uint & 0b0000_1110_0000_0000
                        for pga_mode in PGA:
                            if pga_setting == pga_mode.value:
                                return convert_step_to_microvolts(step, pga_mode)
                        else:
                            raise RuntimeError('unable to identify PGA mode ({config_uint:08X})')
                    else:
                        # ADS1113 has a fixed voltage range of ±2.048V
                        return convert_step_to_microvolts(step, PGA.MODE2)
                else:
                    return step
            else:
                raise RuntimeError("device is configured for continuous conversion")
