#!/usr/bin/env python3
"""
ADS1xxx family of I²C analog-to-digital converters
"""

# the following imports are provided for user convenience
# flake8: noqa: F401
# 12bit / 3300 samples per second
from feeph.ads1xxx.ads1013 import Ads1013, Ads1013Config
from feeph.ads1xxx.ads1014 import Ads1014, Ads1014Config
from feeph.ads1xxx.ads1015 import Ads1015, Ads1015Config

# 16bit / 860 samples per second
from feeph.ads1xxx.ads1113 import Ads1113, Ads1113Config
from feeph.ads1xxx.ads1114 import Ads1114, Ads1114Config
from feeph.ads1xxx.ads1115 import Ads1115, Ads1115Config

# config settings
from feeph.ads1xxx.conversions import UNIT
from feeph.ads1xxx.settings import CLAT, CMOD, CPOL, CQUE, DOM, DRS, MUX, PGA, SSC
