#!/usr/bin/env python3

from enum import Enum

from feeph.ads1xxx.settings import PGA


class UNIT(Enum):
    STEPS = 0
    MICRO = 1


PGA_FACTOR = {
    PGA.MODE0: 6144,
    PGA.MODE1: 4096,
    PGA.MODE2: 2048,
    PGA.MODE3: 1024,
    PGA.MODE4: 512,
    PGA.MODE5: 256,
    PGA.MODE6: 256,  # same as MODE5
    PGA.MODE7: 256,  # same as MODE5
}


def convert_number_to_sint16(value: int) -> int:
    """
    -32768 -> 0x8000
        -1 -> 0xFFFF
         0 -> 0x0000
     32767 -> 0x7FFF
    """
    if 0 <= value <= 32767:
        return value
    elif -32768 <= value <= -1:
        return 65536 + value
    else:
        raise ValueError("out of range")


def convert_sint16_to_number(value: int) -> int:
    if 0 <= value <= 32767:
        return value
    elif 32768 <= value <= 65535:
        return -65536 + value
    else:
        raise ValueError('')


def convert_step_to_microvolts(step: int, pga: PGA) -> int:
    """
    convert the step value to microvolts
    ```
    PGA.MODE2:
     -32768 -> -2048000µV
     +32767 -> +2048000µV
    ```
    """
    # it doesn't make much sense to return a floating point value
    #  1 step at the highest precision level (PGA.MODE5) is 7.8µV
    number = convert_sint16_to_number(step)
    return round(number * (PGA_FACTOR[pga] * 1000 / 32767))


def convert_microvolts_to_step(value: int, pga: PGA) -> int:
    """
    convert the microvolt value to steps
    ```
    PGA.MODE2:
     -2048000µV -> -32768
     +2048000µV -> +32767
    ```
    """
    number = round(value / (PGA_FACTOR[pga] / 2048) * 32767 / 2048000)
    return convert_number_to_sint16(number)


def convert_step_to_value(step: int, unit: UNIT, pga: PGA) -> int:
    if 0x0000 <= step <= 0xFFFF:
        if unit == UNIT.STEPS:
            return step
        elif unit == UNIT.MICRO:
            return convert_step_to_microvolts(step=step, pga=pga)
        else:
            raise ValueError(f"invalid unit '{unit}'")
    else:
        raise ValueError(f"step '{step}' is out of range")


def convert_value_to_step(value: int, unit: UNIT, pga: PGA) -> int:
    """
    convert the provided value to microvolts

    raises ValueError if the value can't be converted
    """
    if unit == UNIT.STEPS:
        step = value
    elif unit == UNIT.MICRO:
        step = convert_microvolts_to_step(value=value, pga=pga)
    else:
        raise ValueError("usage error - invalid value '{unit}'")
    if step is not None and 0x0000 <= step <= 0xFFFF:
        return step
    else:
        raise ValueError("invalid value or out of range")
