#!/usr/bin/env python3
"""
configure the comparator

The ADS1x14 and ADS1x15 feature a programmable digital comparator that can
issue an alert on the ALERT/RDY pin if the low or high threshold values are
exceeded. Together with continuous-conversion mode this feature can be used
to trigger a hardware interrupt and alert on abnormal conditions.

This example works with all variations:
 - ADS1013, ADS1014, ADS1015
 - ADS1113, ADS1114, ADS1115
(Please note that the samping rates on ADS101x and 111x are different.)

usage:
  pdm run examples/03_comparator.py
"""

import logging
import time

import board  # type: ignore

# module busio and board provide no type hints
import busio  # type: ignore

from feeph.ads1xxx import DOM, DRS, Ads1114, Ads1114Config

LH = logging.getLogger("main")

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname).1s: %(message)s', level=logging.INFO)

    i2c_bus = busio.I2C(scl=board.SCL, sda=board.SDA)
    ads1x14 = Ads1114(i2c_bus=i2c_bus)

    # create a configuration
    #  - enable continuous conversion mode
    #  - set desired data rate
    # on ADS1x14/ADS1x15: configure comparator (clat, cmod, cpol & cque)
    my_config = Ads1114Config(dom=DOM.CCM, drs=DRS.MODE2)

    if ads1x14.configure(config=my_config):
        while True:
            # on an ADS111x in MODE2 there should be a new sample
            # every 0.5 seconds (ADS101x is much faster)
            value = ads1x14.get_ccm_measurement()
            print(f"value: {value}µV")
            time.sleep(0.5)
    else:
        print("Unable to configure ADC.")
