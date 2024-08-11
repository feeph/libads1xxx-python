#!/usr/bin/env python3

import unittest

import feeph.ads1xxx as sut  # sytem under test
from feeph.ads1xxx.conversions import UNIT
from feeph.ads1xxx.settings import CLAT, CMOD, CPOL, CQUE, DOM, DRS, PGA, SSC


class TestAds1014Config(unittest.TestCase):

    def test_default_config(self):
        # -----------------------------------------------------------------
        computed = sut.Ads1014Config().as_uint16()
        expected = 0x0583
        # -----------------------------------------------------------------
        self.assertEqual(expected, computed)

    # ---------------------------------------------------------------------
    # ADS1113, ADS1014 & ADS1115
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

    # ---------------------------------------------------------------------
    # ADS1014 & ADS1115
    # ---------------------------------------------------------------------

    def test_programmable_gain_amplifier(self):
        values = {
            PGA.MODE0: 0x0183,
            PGA.MODE1: 0x0383,
            PGA.MODE2: 0x0583,
            PGA.MODE3: 0x0783,
            PGA.MODE4: 0x0983,
            PGA.MODE5: 0x0B83,
            PGA.MODE6: 0x0D83,
            PGA.MODE7: 0x0F83,
        }
        for mode, config_uint16 in values.items():
            computed = sut.Ads1115Config(pga=mode).as_uint16()
            expected = config_uint16
            self.assertEqual(computed, expected)

    def test_comparator_mode(self):
        values = {
            CMOD.TRD: 0x0583,
            CMOD.WND: 0x0593,
        }
        for mode, config_uint16 in values.items():
            computed = sut.Ads1115Config(cmod=mode).as_uint16()
            expected = config_uint16
            self.assertEqual(computed, expected)

    def test_comparator_polarity(self):
        values = {
            CPOL.ALO: 0x0583,
            CPOL.AHI: 0x058B,
        }
        for mode, config_uint16 in values.items():
            computed = sut.Ads1115Config(cpol=mode).as_uint16()
            expected = config_uint16
            self.assertEqual(computed, expected)

    def test_comparator_latch(self):
        values = {
            CLAT.NLC: 0x0583,
            CLAT.LAT: 0x0587,
        }
        for mode, config_uint16 in values.items():
            computed = sut.Ads1115Config(clat=mode).as_uint16()
            expected = config_uint16
            self.assertEqual(computed, expected)

    def test_comparator_queue(self):
        values = {
            CQUE.AA1: 0x0580,
            CQUE.AA2: 0x0581,
            CQUE.AA4: 0x0582,
            CQUE.DIS: 0x0583,
        }
        for mode, config_uint16 in values.items():
            computed = sut.Ads1115Config(cque=mode).as_uint16()
            expected = config_uint16
            self.assertEqual(computed, expected)

    def test_get_atlo_as_steps(self):
        computed = sut.Ads1014Config(atlo=0x9FFF).get_atlo(unit=UNIT.STEPS)
        expected = 0x9FFF
        self.assertEqual(computed, expected)

    def test_get_atlo_as_microvolts(self):
        computed = sut.Ads1014Config(atlo=0x9FFF).get_atlo(unit=UNIT.MICRO)
        expected = -1536109
        self.assertEqual(computed, expected)

    def test_set_atlo_using_steps(self):
        config = sut.Ads1014Config()
        config.set_atlo(0x9FFF, unit=UNIT.STEPS)
        computed = config.get_atlo()
        expected = -1536109
        self.assertEqual(computed, expected)

    def test_set_atlo_using_steps_oor(self):
        computed = sut.Ads1014Config().set_atlo(0xFFFFFF, unit=UNIT.STEPS)
        expected = False
        self.assertEqual(computed, expected)

    def test_set_atlo_using_microvolts(self):
        config = sut.Ads1014Config()
        config.set_atlo(-1536109, unit=UNIT.MICRO)
        computed = config.get_atlo()
        expected = -1536109
        self.assertEqual(computed, expected)

    def test_get_athi_as_steps(self):
        computed = sut.Ads1014Config(atlo=0x6000).get_atlo(unit=UNIT.STEPS)
        expected = 0x6000
        self.assertEqual(computed, expected)

    def test_get_athi_as_microvolts(self):
        computed = sut.Ads1014Config(atlo=0x6000).get_atlo(unit=UNIT.MICRO)
        expected = 1536047
        self.assertEqual(computed, expected)

    def test_set_athi_using_steps(self):
        config = sut.Ads1014Config()
        config.set_athi(0x6000, unit=UNIT.STEPS)
        computed = config.get_athi()
        expected = 1536047
        self.assertEqual(computed, expected)

    def test_set_athi_using_steps_oor(self):
        computed = sut.Ads1014Config().set_athi(0xFFFFFF, unit=UNIT.STEPS)
        expected = False
        self.assertEqual(computed, expected)

    def test_set_athi_using_microvolts(self):
        config = sut.Ads1014Config()
        config.set_athi(1536047, unit=UNIT.MICRO)
        computed = config.get_athi()
        expected = 1536047
        self.assertEqual(computed, expected)
