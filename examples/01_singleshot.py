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

import time

import board  # type: ignore

# module busio and board provide no type hints
import busio  # type: ignore

from feeph.ads1xxx import DRS, UNIT, Ads1113, Ads1113Config

if __name__ == '__main__':
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
    print("value1: {value1}µV")

    # take a second measurement
    #   if no configuration is provided we continue to use the previous one
    value2 = ads1x13.get_ssc_measurement()
    print("value2: {value1}µV")

    # convert from MicroVolt to Volt
    #   This might skew the value due to conversion to float!
    value3 = float(value1) / (1000 * 1000)
    print("value3: {value2:0.6f}V")

    # show the raw value
    # range:
    #   -32768 ≤ x ≤ 32767
    # granularity:
    #   ADS101x: 15 steps (..., 15, 30, 45, ...)
    #   ADS111x:  1 step  (..., 1, 2, 3, 4, ...)
    value4 = ads1x13.get_ssc_measurement(unit=UNIT.STEPS)
    print("value4: {value1}")

    print('-' * 80)

    # take multiple measurements and alternate between 2 configurations
    config1 = Ads1113Config(drs=DRS.MODE4)
    config2 = Ads1113Config(drs=DRS.MODE5)
    while True:
        value4 = ads1x13.get_ssc_measurement(config=config1)
        print("value4: {value1}µV")
        value5 = ads1x13.get_ssc_measurement(config=config2)
        print("value5: {value1}µV")
        time.sleep(1)
