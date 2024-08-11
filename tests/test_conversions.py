#!/usr/bin/env python3

import unittest

import feeph.ads1xxx.conversions as sut  # sytem under test
from feeph.ads1xxx.settings import PGA

# flake8: noqa: E131


class TestNumberToSint16(unittest.TestCase):

    def test_numbers(self):
        values = [
            (-32768, 0x8000),
            (-1, 0xFFFF),
            (0, 0x0000),
            (32767, 0x7FFF),
        ]
        for number, sint16 in values:
            computed = sut.convert_number_to_sint16(number)
            expected = sint16
            self.assertEqual(computed, expected)

    def test_oor(self):
        self.assertRaises(ValueError, sut.convert_number_to_sint16, 32768)
        self.assertRaises(ValueError, sut.convert_number_to_sint16, -32769)


class TestSint16ToNumber(unittest.TestCase):

    def test_numbers(self):
        values = [
            (-32768, 0x8000),
            (-1, 0xFFFF),
            (0, 0x0000),
            (32767, 0x7FFF),
        ]
        for number, sint16 in values:
            computed = sut.convert_sint16_to_number(sint16)
            expected = number
            self.assertEqual(computed, expected)

    def test_oor(self):
        self.assertRaises(ValueError, sut.convert_sint16_to_number, 0xFFFFFF)


class TestStepToValue(unittest.TestCase):
    # not much to test, it's already covered by other tests

    def test_invalid_unit(self):
        self.assertRaises(ValueError, sut.convert_step_to_value, 0xFFFF, unit=None, pga=PGA.MODE2)

    def test_oor(self):
        self.assertRaises(ValueError, sut.convert_step_to_value, 0xFFFFFF, unit=sut.UNIT.STEPS, pga=PGA.MODE2)


class TestValueToStep(unittest.TestCase):
    # not much to test, it's already covered by other tests

    def test_invalid_unit(self):
        self.assertRaises(ValueError, sut.convert_value_to_step, 0xFFFF, unit=None, pga=PGA.MODE2)


class TestConvertToMicrovolt(unittest.TestCase):

    def test_mode0(self):
        values = {
            # fmt: off
            # step     µV
            0x8000: -6144188,  # lowest measureable value
            0x0001:      188,  # step resolution
            0x7FFF:  6144000,  # highest measureable value
            # fmt: on
        }
        for value, expected in values.items():
            self.assertEqual(sut.convert_step_to_microvolts(value, PGA.MODE0), expected)

    def test_mode1(self):
        values = {
            # fmt: off
            # step     µV
            0x8000: -4096125,  # lowest measureable value
            0x0001:      125,  # step resolution
            0x7FFF:  4096000,  # highest measureable value
            # fmt: on
        }
        for value, expected in values.items():
            self.assertEqual(sut.convert_step_to_microvolts(value, PGA.MODE1), expected)

    def test_mode2(self):
        values = {
            # fmt: off
            # step     µV
            0x8000: -2048063,  # lowest measureable value
            0x0001:       63,  # step resolution
            0x7FFF:  2048000,  # highest measureable value
            # fmt: on
        }
        for value, expected in values.items():
            self.assertEqual(sut.convert_step_to_microvolts(value, PGA.MODE2), expected)

    def test_mode3(self):
        values = {
            # fmt: off
            # step     µV
            0x8000: -1024031,  # lowest measureable value
            0x0001:       31,  # step resolution
            0x7FFF:  1024000,  # highest measureable value
            # fmt: on
        }
        for value, expected in values.items():
            self.assertEqual(sut.convert_step_to_microvolts(value, PGA.MODE3), expected)

    def test_mode4(self):
        values = {
            # fmt: off
            # step    µV
            0x8000: -512016,  # lowest measureable value
            0x0001:      16,  # step resolution
            0x7FFF:  512000,  # highest measureable value
            # fmt: on
        }
        for value, expected in values.items():
            self.assertEqual(sut.convert_step_to_microvolts(value, PGA.MODE4), expected)

    def test_mode5(self):
        values = {
            # fmt: off
            # step    µV
            0x8000: -256008,  # lowest measureable value
            0x0001:       8,  # step resolution
            0x7FFF:  256000,  # highest measureable value
            # fmt: on
        }
        for value, expected in values.items():
            self.assertEqual(sut.convert_step_to_microvolts(value, PGA.MODE5), expected)
            self.assertEqual(sut.convert_step_to_microvolts(value, PGA.MODE6), expected)
            self.assertEqual(sut.convert_step_to_microvolts(value, PGA.MODE7), expected)


# flake8: noqa: E131
class TestConvertToStep(unittest.TestCase):

    def test_mode0(self):
        values = {
            # fmt: off
            # step     µV
            0x8000: -6144188,  # lowest measureable value
            0x0001:      188,  # step resolution
            0x7FFF:  6144000,  # highest measureable value
            # fmt: on
        }
        for step, microvolt in values.items():
            computed = sut.convert_microvolts_to_step(microvolt, PGA.MODE0)
            expected = step
            self.assertEqual(computed, expected)

    def test_mode1(self):
        values = {
            # fmt: off
            # step     µV
            0x8000: -4096125,  # lowest measureable value
            0x0001:      125,  # step resolution
            0x7FFF:  4096000,  # highest measureable value
            # fmt: on
        }
        for step, microvolt in values.items():
            computed = sut.convert_microvolts_to_step(microvolt, PGA.MODE1)
            expected = step
            self.assertEqual(computed, expected)

    def test_mode2(self):
        values = {
            # fmt: off
            # step     µV
            0x8000: -2048063,  # lowest measureable value
            0x0001:       63,  # step resolution
            0x7FFF:  2048000,  # highest measureable value
            # fmt: on
        }
        for step, microvolt in values.items():
            computed = sut.convert_microvolts_to_step(microvolt, PGA.MODE2)
            expected = step
            self.assertEqual(computed, expected)

    def test_mode3(self):
        values = {
            # fmt: off
            # step     µV
            0x8000: -1024031,  # lowest measureable value
            0x0001:       31,  # step resolution
            0x7FFF:  1024000,  # highest measureable value
            # fmt: on
        }
        for step, microvolt in values.items():
            computed = sut.convert_microvolts_to_step(microvolt, PGA.MODE3)
            expected = step
            self.assertEqual(computed, expected)

    def test_mode4(self):
        values = {
            # fmt: off
            # step    µV
            0x8000: -512016,  # lowest measureable value
            0x0001:      16,  # step resolution
            0x7FFF:  512000,  # highest measureable value
            # fmt: on
        }
        for step, microvolt in values.items():
            computed = sut.convert_microvolts_to_step(microvolt, PGA.MODE4)
            expected = step
            self.assertEqual(computed, expected)

    def test_mode5(self):
        values = {
            # fmt: off
            # step    µV
            0x8000: -256008,  # lowest measureable value
            0x0001:       8,  # step resolution
            0x7FFF:  256000,  # highest measureable value
            # fmt: on
        }
        for step, microvolt in values.items():
            computed = sut.convert_microvolts_to_step(microvolt, PGA.MODE5)
            expected = step
            self.assertEqual(computed, expected)
        for step, microvolt in values.items():
            computed = sut.convert_microvolts_to_step(microvolt, PGA.MODE6)
            expected = step
            self.assertEqual(computed, expected)
        for step, microvolt in values.items():
            computed = sut.convert_microvolts_to_step(microvolt, PGA.MODE7)
            expected = step
            self.assertEqual(computed, expected)
