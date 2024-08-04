#!/usr/bin/env python3
"""
test ADS1115

use simulated device:
  pdm run pytest
use hardware device:
  TEST_ADS1115_CHIP=y pdm run pytest
"""

import os
import time
import unittest

# modules board and busio provide no type hints
import board  # type: ignore
import busio  # type: ignore
from feeph.i2c import BurstHandler, EmulatedI2C

import feeph.ads1xxx as sut  # sytem under test
from feeph.ads1xxx.ads1115 import DEFAULTS

if os.environ.get('TEST_ADS1115_CHIP', 'n') == 'y':
    HAS_HARDWARE = True
else:
    HAS_HARDWARE = False


class TestAds1115(unittest.TestCase):

    def setUp(self):
        self.i2c_adr = 0x48
        if HAS_HARDWARE:
            self.i2c_bus = busio.I2C(scl=board.SCL, sda=board.SDA)
        else:
            state = {
                self.i2c_adr: {
                    0x00: 0x0000,
                    0x01: 0x0000,
                    0x02: 0x0000,
                    0x03: 0x0000,
                }
            }
            state[self.i2c_adr].update(DEFAULTS)
            self.i2c_bus = EmulatedI2C(state=state)
        self.ads1115 = sut.Ads1115(i2c_bus=self.i2c_bus)

    def tearDown(self):
        # restore original state after each run
        # (hardware is not stateless)
        self.ads1115.reset_device_registers()

    # ---------------------------------------------------------------------

    def test_default_config(self):
        with BurstHandler(i2c_bus=self.i2c_bus, i2c_adr=self.i2c_adr) as bh:
            bh.write_register(0x01, 0x0083, byte_count=2)
            bh.write_register(0x02, 0xA000, byte_count=2)
            bh.write_register(0x03, 0x5FFF, byte_count=2)
        # -----------------------------------------------------------------
        self.ads1115.reset_device_registers()
        time.sleep(0.001)  # wait for single-shot conversion to finish
        # -----------------------------------------------------------------
        with BurstHandler(i2c_bus=self.i2c_bus, i2c_adr=self.i2c_adr) as bh:
            # single-shot conversion completed (0x8583) or in progress (0x0583)
            self.assertIn(bh.read_register(0x01, byte_count=2), [0x8583, 0x0583])
            # threshold range: -32768 (0x8000) ≤ x ≤ 32767 (0x7FFF)
            self.assertEqual(bh.read_register(0x02, byte_count=2), 0x8000)
            self.assertEqual(bh.read_register(0x03, byte_count=2), 0x7FFF)
