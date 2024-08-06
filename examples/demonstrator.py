#!/usr/bin/env
"""
just a sample script to show expected usage
<replace as needed>

usage:
  pdm run scripts/demonstrator.py
"""

import argparse
import logging

# modules board and busio provide no type hints
import board  # type: ignore
import busio  # type: ignore

import feeph.ads1xxx

LH = logging.getLogger("main")

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname).1s: %(message)s', level=logging.INFO)

    parser = argparse.ArgumentParser(prog="demonstrator", description="demonstrate usage")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        LH.setLevel(level=logging.DEBUG)

    i2c_bus = busio.I2C(scl=board.SCL, sda=board.SDA)
    ads1115 = feeph.ads1xxx.Ads1115(i2c_bus=i2c_bus)

    # we don't know what was previously configured, let's reset
    ads1115.reset_device_registers()

    # take a single-shot measurement
    LH.info("measurement: %0.6fV", ads1115.get_singleshot_measurement() / (1000 * 1000))
