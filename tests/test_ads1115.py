#!/usr/bin/env python3
"""
test Ads1115

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
from feeph.ads1xxx.ads1x1x import DEFAULTS
from feeph.ads1xxx.conversions import UNIT

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
            registers = DEFAULTS.copy()
            for register, default_value in registers.items():
                if default_value is None:
                    registers[register] = 0x0000
            self.i2c_bus = EmulatedI2C(state={self.i2c_adr: registers})
        self.ads1115 = sut.Ads1115(i2c_bus=self.i2c_bus)

    def tearDown(self):
        # restore original state after each run
        # (hardware is not stateless)
        self.ads1115.reset_device_registers()

    # ---------------------------------------------------------------------

    def test_reset(self):
        with BurstHandler(i2c_bus=self.i2c_bus, i2c_adr=self.i2c_adr) as bh:
            # change writeable registers to non-default values
            bh.write_register(0x01, 0x0083, byte_count=2)
            bh.write_register(0x02, 0xA000, byte_count=2)
            bh.write_register(0x03, 0x5FFF, byte_count=2)
        # -----------------------------------------------------------------
        self.ads1115.reset_device_registers()
        # -----------------------------------------------------------------
        with BurstHandler(i2c_bus=self.i2c_bus, i2c_adr=self.i2c_adr) as bh:
            # single-shot conversion completed (0x8583) or in progress (0x0583)
            self.assertIn(bh.read_register(0x01, byte_count=2), [0x8583, 0x0583])
            # threshold range: -32768 (0x8000) ≤ x ≤ 32767 (0x7FFF)
            self.assertEqual(bh.read_register(0x02, byte_count=2), 0x8000)
            self.assertEqual(bh.read_register(0x03, byte_count=2), 0x7FFF)

    # ---------------------------------------------------------------------

    @unittest.skipIf(HAS_HARDWARE, "unpredictable result on real hardware")
    def test_ssc_measurement_default(self):
        self.i2c_bus._state[0x48][0x00] = 0x1234
        # -----------------------------------------------------------------
        computed = self.ads1115.get_ssc_measurement(unit=UNIT.STEPS)
        expected = 0x1234
        # -----------------------------------------------------------------
        self.assertEqual(expected, computed)

    @unittest.skipIf(HAS_HARDWARE, "unpredictable result on real hardware")
    def test_ssc_measurement_in_microvolts(self):
        self.i2c_bus._state[0x48][0x00] = 0x0001
        # -----------------------------------------------------------------
        computed = self.ads1115.get_ssc_measurement()
        expected = 63  # microvolts
        # -----------------------------------------------------------------
        self.assertEqual(expected, computed)

    def test_ssc_measurement_with_config(self):
        config = sut.Ads1115Config()
        self.ads1115.get_ssc_measurement(config=config)
        # -----------------------------------------------------------------
        with BurstHandler(i2c_bus=self.i2c_bus, i2c_adr=self.i2c_adr) as bh:
            computed = bh.read_register(0x01, byte_count=2)
        expected = [0x0583, 0x8583]
        # -----------------------------------------------------------------
        self.assertIn(computed, expected)

    def test_ssc_measurement_continued(self):
        config = sut.Ads1115Config()
        self.ads1115.get_ssc_measurement(config=config)
        self.ads1115.get_ssc_measurement()  # use same config as previous read
        # -----------------------------------------------------------------
        with BurstHandler(i2c_bus=self.i2c_bus, i2c_adr=self.i2c_adr) as bh:
            computed = bh.read_register(0x01, byte_count=2)
        expected = [0x0583, 0x8583]
        # -----------------------------------------------------------------
        self.assertIn(computed, expected)

    def test_ssc_measurement_conflict1(self):
        config_ccm = sut.Ads1115Config(dom=sut.DOM.CCM)
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        # can't use singleshot with continuous conversion mode
        self.assertRaises(RuntimeError, self.ads1115.get_ssc_measurement, config=config_ccm)

    def test_ssc_measurement_conflict2(self):
        config_ccm = sut.Ads1115Config(dom=sut.DOM.CCM)
        with BurstHandler(i2c_bus=self.i2c_bus, i2c_adr=self.i2c_adr) as bh:
            bh.write_register(0x01, config_ccm.as_uint16(), byte_count=2)
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        # device is configured for continuous conversion mode
        self.assertRaises(RuntimeError, self.ads1115.get_ssc_measurement)

    # ---------------------------------------------------------------------

    def test_configure(self):
        config = sut.Ads1115Config(dom=sut.DOM.CCM)
        config.set_atlo(0xA000, unit=UNIT.STEPS)
        config.set_athi(0x5FFF, unit=UNIT.STEPS)
        self.ads1115.configure(config=config)
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        with BurstHandler(i2c_bus=self.i2c_bus, i2c_adr=self.i2c_adr) as bh:
            self.assertIn(bh.read_register(0x01, byte_count=2), [0x0483, 0x8483])
            self.assertEqual(bh.read_register(0x10, byte_count=2), 0xA000)
            self.assertEqual(bh.read_register(0x11, byte_count=2), 0x5FFF)

    @unittest.skipIf(HAS_HARDWARE, "unpredictable result on real hardware")
    def test_ccm_measurement(self):
        self.i2c_bus._state[0x48][0x00] = 0x1234
        self.ads1115.configure(config=sut.Ads1115Config(dom=sut.DOM.CCM))
        # -----------------------------------------------------------------
        computed = self.ads1115.get_ccm_measurement(unit=UNIT.STEPS)
        expected = 0x1234
        # -----------------------------------------------------------------
        self.assertEqual(expected, computed)

    @unittest.skipIf(HAS_HARDWARE, "unpredictable result on real hardware")
    def test_ccm_measurement_pga(self):
        self.i2c_bus._state[0x48][0x00] = 0x1234
        self.ads1115.configure(config=sut.Ads1115Config(dom=sut.DOM.CCM, pga=sut.PGA.MODE1))
        # -----------------------------------------------------------------
        computed = self.ads1115.get_ccm_measurement(unit=UNIT.MICRO)
        expected = 582518
        # -----------------------------------------------------------------
        self.assertEqual(expected, computed)

    def test_ccm_measurement_conflict(self):
        self.i2c_bus._state[0x48][0x00] = 0x1234
        self.ads1115.configure(config=sut.Ads1115Config(dom=sut.DOM.SSM))
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        self.assertRaises(RuntimeError, self.ads1115.get_ccm_measurement)
