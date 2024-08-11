#!/usr/bin/env python3

from enum import Enum


class CQUE(Enum):
    """
    Comparator queue and disable  (config[0:1])
    ```
    CQUE.AA1 -> assert after one conversion
    CQUE.AA2 -> assert after two conversions
    CQUE.AA4 -> assert after four conversions
    CQUE.DIS -> disable comparator and set ALERT/RDY pin to high-impedance (default)
    ```
    """
    AA1 = 0b0000_0000_0000_0000
    AA2 = 0b0000_0000_0000_0001
    AA4 = 0b0000_0000_0000_0010
    DIS = 0b0000_0000_0000_0011


class CLAT(Enum):
    """
    latching comparator (config[2])
    ```
    CLAT.NLC -> non-latching comparator
    CLAT.LAT -> latching comparator
    ```
    """
    NLC = 0b0000_0000_0000_0000
    LAT = 0b0000_0000_0000_0100


class CPOL(Enum):
    """
    comparator polarity (config[3])
    ```
    CPOL.ALO -> active low
    CPOL.AHI -> active high
    ```
    """
    ALO = 0b0000_0000_0000_0000
    AHI = 0b0000_0000_0000_1000


class CMOD(Enum):
    """
    comparator mode (config[4])
    ```
    CMOD.TRD -> traditional comparator
    CMOD.WND -> window comparator
    ```
    """
    TRD = 0b0000_0000_0000_0000
    WND = 0b0000_0000_0001_0000


class DRS(Enum):
    """
    data rate setting (config[5:7])
    ```
                 ADS101x ADS111x
    DRS.MODE0 ->      8     128 samples per second
    DRS.MODE1 ->     16     250 samples per second
    DRS.MODE2 ->     32     490 samples per second
    DRS.MODE3 ->     64     920 samples per second
    DRS.MODE4 ->    128    1600 samples per second
    DRS.MODE5 ->    250    2400 samples per second
    DRS.MODE6 ->    475    3300 samples per second
    DRS.MODE7 ->    860    3300 samples per second
    ```
    """
    MODE0 = 0b0000_0000_0000_0000
    MODE1 = 0b0000_0000_0010_0000
    MODE2 = 0b0000_0000_0100_0000
    MODE3 = 0b0000_0000_0110_0000
    MODE4 = 0b0000_0000_1000_0000
    MODE5 = 0b0000_0000_1010_0000
    MODE6 = 0b0000_0000_1100_0000
    MODE7 = 0b0000_0000_1110_0000


class DOM(Enum):
    """
    device operation mode (config[8])
    ```
    DOM.CCM -> continuous conversion mode
    DOM.SSM -> single-shot mode
    ```
    """
    CCM = 0b0000_0000_0000_0000
    SSM = 0b0000_0001_0000_0000


class PGA(Enum):
    """
    programmable gain amplifier (config[9:11])
    ```
    PGA.MODE0 -> FSR: ±6.144 V @   3mV (Vdd: 5.9 ≤ x ≤ 7.0)
    PGA.MODE1 -> FSR: ±4.096 V @   2mV (Vdd: 3.8 ≤ x ≤ 7.0)
    PGA.MODE2 -> FSR: ±2.048 V @   1mV
    PGA.MODE3 -> FSR: ±1.024 V @ 500µV
    PGA.MODE4 -> FSR: ±0.512 V @ 250µV
    PGA.MODE5 -> FSR: ±0.256 V @ 125µV
    PGA.MODE6 -> FSR: ±0.256 V @ 125µV
    PGA.MODE7 -> FSR: ±0.256 V @ 125µV
    ```
    """
    MODE0 = 0b0000_0000_0000_0000
    MODE1 = 0b0000_0010_0000_0000
    MODE2 = 0b0000_0100_0000_0000
    MODE3 = 0b0000_0110_0000_0000
    MODE4 = 0b0000_1000_0000_0000
    MODE5 = 0b0000_1010_0000_0000
    MODE6 = 0b0000_1100_0000_0000
    MODE7 = 0b0000_1110_0000_0000


class MUX(Enum):
    """
    input multiplexer configuration (config[12:14])
    ```
    MUX.MODE0 -> AIN0»AIN1
    MUX.MODE1 -> AIN0»AIN3
    MUX.MODE2 -> AIN1»AIN3
    MUX.MODE3 -> AIN2»AIN3
    MUX.MODE4 -> AIN0»GND
    MUX.MODE5 -> AIN1»GND
    MUX.MODE6 -> AIN2»GND
    MUX.MODE7 -> AIN3»GND
    ```
    """
    MODE0 = 0b0000_0000_0000_0000
    MODE1 = 0b0001_0000_0000_0000
    MODE2 = 0b0010_0000_0000_0000
    MODE3 = 0b0011_0000_0000_0000
    MODE4 = 0b0100_0000_0000_0000
    MODE5 = 0b0101_0000_0000_0000
    MODE6 = 0b0110_0000_0000_0000
    MODE7 = 0b0111_0000_0000_0000


class SSC(Enum):
    """
    single-shot conversion trigger (config[15])
    ```
    SSC.NO_OP -> do nothing
    SSC.START -> start a conversion
    ```
    """
    NO_OP = 0b0000_0000_0000_0000
    START = 0b1000_0000_0000_0000
