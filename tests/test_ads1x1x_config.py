#!/usr/bin/env python3

import unittest

import feeph.ads1xxx.ads1x1x as sut  # sytem under test


class IncompleteConfig(sut.Ads1x1xConfig):
    # !! DO NOT WRITE CODE LIKE THIS !!
    # The purpose of this class is to disable all safety checks and
    # brute-force the usage of abstract methods so we can test that
    # the code correctly bugs out if this happens
    # !! DO NOT WRITE CODE LIKE THIS !!

    def as_uint16(self) -> int:
        # !! DANGER !!
        return super().as_uint16()  # type: ignore [safe-super]

    def get_atlo(self, unit: sut.UNIT) -> int:
        # !! DANGER !!
        return super().get_atlo(unit=unit)  # type: ignore [safe-super]

    def get_athi(self, unit: sut.UNIT) -> int:
        # !! DANGER !!
        return super().get_athi(unit=unit)  # type: ignore [safe-super]


class TestAds1x1xConfig(unittest.TestCase):

    def test_abstract_base_class(self):
        self.assertRaises(TypeError, sut.Ads1x1xConfig)

    def test_abstract_method1(self):
        self.assertRaises(TypeError, IncompleteConfig().as_uint16())

    def test_abstract_method2(self):
        self.assertRaises(TypeError, IncompleteConfig().get_atlo(unit=sut.UNIT.STEPS))

    def test_abstract_method3(self):
        self.assertRaises(TypeError, IncompleteConfig().get_athi(unit=sut.UNIT.STEPS))
