#!/usr/bin/env python3
"""
configure the programmable gain amplifier

This example requires a PGA:
 - ADS1014, ADS1015
 - ADS1114, ADS1115

usage:
  pdm run examples/04_amplifier.py
"""

import board  # type: ignore

# module busio and board provide no type hints
import busio  # type: ignore

from feeph.ads1xxx import PGA, Ads1114, Ads1114Config

if __name__ == '__main__':
    i2c_bus = busio.I2C(scl=board.SCL, sda=board.SDA)
    ads1x14 = Ads1114(i2c_bus=i2c_bus)

    # make sure the voltage between AIN0 and GND does not exceed 0.5V
    # (e.g. use a resistive divider)
    #
    # check feeph/ads1xxx/settings.py for an explanation of this setting
    # or hover on 'PGA' and let your IDE show the docstring
    config1 = Ads1114Config(pga=PGA.MODE2)  # FSR = ±2.048V
    config2 = Ads1114Config(pga=PGA.MODE4)  # FSR = ±0.512V

    value1 = ads1x14.get_ssc_measurement(config=config1)
    print("value1: {value1}µV")  # 63µV resolution
    value2 = ads1x14.get_ssc_measurement(config=config2)
    print("value2: {value2}µV")  # 16µV resolution
