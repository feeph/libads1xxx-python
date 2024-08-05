#!/usr/bin/env python3

import unittest

import feeph.ads1xxx as sut  # sytem under test


class TestAds1115Config(unittest.TestCase):

    def test_default_config(self):
        # -----------------------------------------------------------------
        computed = sut.Ads1115Config().as_uint16()
        expected = 0x0583
        # -----------------------------------------------------------------
        self.assertEqual(expected, computed)
