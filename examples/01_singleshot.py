#!/usr/bin/env python3
"""
perform a single-shot measurement

In single-shot mode, the ADC performs one conversion of the input signal
upon request, stores the conversion value to an internal conversion
register, and then enters a power-down state. This mode is intended to
provide significant power savings in systems that only require periodic
conversions or when there are long idle periods between conversions.

This example works with all variations:
 - ADS1013, ADS1014, ADS1015
 - ADS1113, ADS1114, ADS1115

usage:
  pdm run examples/01_singleshot.py
"""

import logging
import time

import board  # type: ignore

# module busio and board provide no type hints
import busio  # type: ignore

from feeph.ads1xxx import DRS, UNIT, Ads1113, Ads1113Config

LH = logging.getLogger("main")

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname).1s: %(message)s', level=logging.INFO)

    i2c_bus = busio.I2C(scl=board.SCL, sda=board.SDA)
    ads1x13 = Ads1113(i2c_bus=i2c_bus)

    # create a configuration
    #   Without any parameters provided this will match the default
    #   configuration for this device.
    my_config = Ads1113Config()

    # take our first measurement
    #   It is recommended to provide a configuration at least once in order
    #   to ensure the device uses the expected configuration.
    value1 = ads1x13.get_ssc_measurement(config=my_config)
    print(f"value1: {value1}µV")

    # take a second measurement
    #   if no configuration is provided we continue to use the previous one
    value2 = ads1x13.get_ssc_measurement()
    print(f"value2: {value2}µV")

    # convert from MicroVolt to Volt
    #   This might skew the value due to conversion to float!
    value3 = ads1x13.get_ssc_measurement() / (1000 * 1000)
    print(f"value3: {value3:0.6f}V")

    # show the raw value
    # range:
    #   -32768 ≤ x ≤ 32767
    # granularity:
    #   ADS101x: 15 steps (..., 15, 30, 45, ...)
    #   ADS111x:  1 step  (..., 1, 2, 3, 4, ...)
    value4 = ads1x13.get_ssc_measurement(unit=UNIT.STEPS)
    print(f"value4: {value4}")

    print('-' * 80)

    # take multiple measurements and alternate between 2 configurations
    config1 = Ads1113Config(drs=DRS.MODE4)
    config2 = Ads1113Config(drs=DRS.MODE5)
    for i in range(1, 10):
        value5 = ads1x13.get_ssc_measurement(config=config1) / (1000 * 1000)
        value6 = ads1x13.get_ssc_measurement(config=config2) / (1000 * 1000)
        print(f"#{i:} value5: {value5:.03f}V, value6: {value6:.03f}V")
        time.sleep(1)
