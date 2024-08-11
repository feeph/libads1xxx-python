#!/usr/bin/env python3
"""
configure the input multiplexer

This example requires a MUX:
 - ADS1015
 - ADS1115

usage:
  pdm run examples/05_multiplexer.py
"""

import logging
import time

import board  # type: ignore

# module busio and board provide no type hints
import busio  # type: ignore

from feeph.ads1xxx import MUX, PGA, Ads1115, Ads1115Config

LH = logging.getLogger("main")

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname).1s: %(message)s', level=logging.INFO)

    i2c_bus = busio.I2C(scl=board.SCL, sda=board.SDA)
    ads1x15 = Ads1115(i2c_bus=i2c_bus)

    # configure 2 channels
    #  - config_abs: measure against ground (±2.0V)
    #  - config_dif: measure delta, using a higher precision (±0.5V)
    #
    # check feeph/ads1xxx/settings.py for an explanation of this setting
    # or hover on 'MUX' and let your IDE show the docstring
    config_abs = Ads1115Config(mux=MUX.MODE4, pga=PGA.MODE1)  # AIN0»GND
    config_dif = Ads1115Config(mux=MUX.MODE0, pga=PGA.MODE4)  # AIN0»AIN1

    # switch between both configurations and take measurements
    while True:
        value1 = ads1x15.get_ssc_measurement(config=config_abs)
        value2 = ads1x15.get_ssc_measurement(config=config_dif)
        print(f"value1: {value1}µV, value2: {value1}µV")
        time.sleep(1)
