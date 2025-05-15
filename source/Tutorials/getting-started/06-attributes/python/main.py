# SPDX-FileCopyrightText: All Contributors to the Tango Controls Community tutorials
# SPDX-License-Identifier: MIT-0

from enum import IntEnum

from tango import AttrWriteType
from tango.server import Device, attribute


class GrinderSetting(IntEnum):
    FINE = 0
    MEDIUM = 1
    COARSE = 2


class MegaCoffee3k(Device):

    def init_device(self):
        super().init_device()
        self._water_level = 54.2
        self._bean_levels = [82.5, 100.0]
        self._brewing_temperature = 94.4
        self._grind = GrinderSetting.FINE

    # decorator-style attributes -------------

    @attribute
    def waterLevel(self) -> float:
        print("reading water level")
        return self._water_level

    @attribute(max_dim_x=2)
    def beanLevels(self) -> list[float]:
        print("reading bean levels")
        return self._bean_levels

    @attribute(
        dtype=[float], max_dim_x=2, doc="How full is each bean dispenser", unit="%"
    )
    def beanLevelsDoc(self):
        return self._bean_levels

    @attribute
    def grind(self) -> GrinderSetting:
        """Setting for the coffee bean grinder"""
        print("reading grinder setting")
        return self._grind

    @grind.setter
    def grind(self, value: int):
        self._grind = GrinderSetting(value)
        print(f"Set grinder to {self._grind}")

    # non-decorator style attributes -------------

    brewingTemperature = attribute(access=AttrWriteType.READ_WRITE, doc="Temperature to brew coffee at [deg C]")

    def read_brewingTemperature(self) -> float:
        return self._brewing_temperature

    def write_brewingTemperature(self, temperature: float):
        self._brewing_temperature = temperature


if __name__ == "__main__":
    MegaCoffee3k.run_server()
