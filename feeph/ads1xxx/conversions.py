#!/usr/bin/env python3

from enum import Enum

from feeph.ads1xxx.settings import PGA


class UNIT(Enum):
    STEPS = 0
    MICRO = 1


def convert_step_to_microvolts(step: int, pga: PGA) -> int:
    """
    convert the step value to microvolts
    ```
    PGA.MODE2:
     -32768 -> -2048mV
     +32767 -> +2048mV
    ```
    """
    factor = {
        PGA.MODE0: 6144,
        PGA.MODE1: 4096,
        PGA.MODE2: 2048,
        PGA.MODE3: 1024,
        PGA.MODE4: 512,
        PGA.MODE5: 256,
        PGA.MODE6: 256,  # same as MODE5
        PGA.MODE7: 256,  # same as MODE5
    }
    # it doesn't make much sense to return a floating point value
    #  1 step at the highest precision level (PGA.MODE5) is 7.8µV
    return round(step * (factor[pga] * 1000 / 32767))
