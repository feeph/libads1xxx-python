#!/usr/bin/env python3

import unittest

import feeph.ads1xxx as sut  # sytem under test
from feeph.ads1xxx.settings import DOM, DRS, SSC


class TestAds1013Config(unittest.TestCase):

    def test_default_config(self):
        # -----------------------------------------------------------------
        computed = sut.Ads1013Config().as_uint16()
        expected = 0x0583
        # -----------------------------------------------------------------
        self.assertEqual(expected, computed)

    # ---------------------------------------------------------------------
    # ADS1013, ADS1114 & ADS1115
    # ---------------------------------------------------------------------

    def test_single_shot_conversion(self):
        values = {
            SSC.NO_OP: 0x0583,
            SSC.START: 0x8583,
        }
        for mode, config_uint16 in values.items():
            computed = sut.Ads1115Config(ssc=mode).as_uint16()
            expected = config_uint16
            self.assertEqual(computed, expected)

    def test_device_operation_mode(self):
        values = {
            DOM.CCM: 0x0483,
            DOM.SSM: 0x0583,
        }
        for mode, config_uint16 in values.items():
            computed = sut.Ads1115Config(dom=mode).as_uint16()
            expected = config_uint16
            self.assertEqual(computed, expected)

    def test_data_rate_setting(self):
        values = {
            DRS.MODE0: 0x0503,
            DRS.MODE1: 0x0523,
            DRS.MODE2: 0x0543,
            DRS.MODE3: 0x0563,
            DRS.MODE4: 0x0583,
            DRS.MODE5: 0x05A3,
            DRS.MODE6: 0x05C3,
            DRS.MODE7: 0x05E3,
        }
        for mode, config_uint16 in values.items():
            computed = sut.Ads1115Config(drs=mode).as_uint16()
            expected = config_uint16
            self.assertEqual(computed, expected)
