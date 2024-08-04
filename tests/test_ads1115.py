#!/usr/bin/env python3
"""
test ADS1115

use simulated device:
  pdm run pytest
use hardware device:
  TEST_ADS1115_CHIP=y pdm run pytest
"""

import os
import unittest

# modules board and busio provide no type hints
import board  # type: ignore
import busio  # type: ignore
from feeph.i2c import BurstHandler, EmulatedI2C

import feeph.ads1xxx as sut  # sytem under test

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
            registers = {(register, 0x0000) for register in range(4)}
            self.i2c_bus = EmulatedI2C(state={self.i2c_adr: registers})
        self.ads1115 = sut.Ads1115(i2c_bus=self.i2c_bus)
        # restore original state after each run
        # (hardware is not stateless)
        self.ads1115.reset_device_registers()

    def tearDown(self):
        # nothing to do
        pass

    # ---------------------------------------------------------------------
    # circuit-dependent settings
    # ---------------------------------------------------------------------

    def test_default_config(self):
        self.ads1115.reset_device_registers()
        # -----------------------------------------------------------------
        with BurstHandler(i2c_bus=self.i2c_bus, i2c_adr=self.i2c_adr) as bh:
            self.assertEqual(bh.read_register(0x00, byte_count=2), 0x0000)
            self.assertEqual(bh.read_register(0x01, byte_count=2), 0x0000)
            self.assertEqual(bh.read_register(0x02, byte_count=2), 0x0000)
            self.assertEqual(bh.read_register(0x03, byte_count=2), 0x0000)
        # -----------------------------------------------------------------
