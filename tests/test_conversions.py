#!/usr/bin/env python3

import unittest

import feeph.ads1xxx.conversions as sut  # sytem under test
from feeph.ads1xxx.settings import PGA


# flake8: noqa: E131
class TestConversions(unittest.TestCase):

    def test_mode0(self):
        values = {
            # fmt: off
            # step     µV
            -32768: -6144188,  # lowest measureable value
                 1:      188,  # step resolution
             32767:  6144000,  # highest measureable value
            # fmt: on
        }
        for value, expected in values.items():
            self.assertEqual(sut.convert_step_to_microvolts(value, PGA.MODE0), expected)

    def test_mode1(self):
        values = {
            # fmt: off
            # step     µV
            -32768: -4096125,  # lowest measureable value
                 1:      125,  # step resolution
             32767:  4096000,  # highest measureable value
            # fmt: on
        }
        for value, expected in values.items():
            self.assertEqual(sut.convert_step_to_microvolts(value, PGA.MODE1), expected)

    def test_mode2(self):
        values = {
            # fmt: off
            # step     µV
            -32768: -2048063,  # lowest measureable value
                 1:       63,  # step resolution
             32767:  2048000,  # highest measureable value
            # fmt: on
        }
        for value, expected in values.items():
            self.assertEqual(sut.convert_step_to_microvolts(value, PGA.MODE2), expected)

    def test_mode3(self):
        values = {
            # fmt: off
            # step     µV
            -32768: -1024031,  # lowest measureable value
                 1:       31,  # step resolution
             32767:  1024000,  # highest measureable value
            # fmt: on
        }
        for value, expected in values.items():
            self.assertEqual(sut.convert_step_to_microvolts(value, PGA.MODE3), expected)

    def test_mode4(self):
        values = {
            # fmt: off
            # step    µV
            -32768: -512016,  # lowest measureable value
                 1:      16,  # step resolution
             32767:  512000,  # highest measureable value
            # fmt: on
        }
        for value, expected in values.items():
            self.assertEqual(sut.convert_step_to_microvolts(value, PGA.MODE4), expected)

    def test_mode5(self):
        values = {
            # fmt: off
            # step    µV
            -32768: -256008,  # lowest measureable value
                 1:       8,  # step resolution
             32767:  256000,  # highest measureable value
            # fmt: on
        }
        for value, expected in values.items():
            self.assertEqual(sut.convert_step_to_microvolts(value, PGA.MODE5), expected)
            self.assertEqual(sut.convert_step_to_microvolts(value, PGA.MODE6), expected)
            self.assertEqual(sut.convert_step_to_microvolts(value, PGA.MODE7), expected)
