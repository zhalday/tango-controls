# SPDX-FileCopyrightText: All Contributors to the Tango Controls Community tutorials
# SPDX-License-Identifier: MIT-0

from tango import AttReqType, DevState
from tango.server import Device, attribute, command


MIN_WATER_REQUIRED_FOR_BREWING_L = 0.2


class MegaCoffee3k(Device):

    def init_device(self):
        super().init_device()
        self.set_state(DevState.OFF)
        self._water_level = 0.1
        self._bean_levels = [82.5, 100.0]
        self._brewing_temperature = 94.4

    @attribute
    def waterLevel(self) -> float:
        print("reading water level")
        return self._water_level

    def is_waterLevel_allowed(self, req_type: AttReqType) -> bool:
        print(f"checking if waterLevel attribute allowed: {req_type=}")
        return self.get_state() == DevState.ON

    @attribute(max_dim_x=2,fisallowed="is_beanLevels_allowed")
    def beanLevels(self) -> list[float]:
        print("reading bean levels")
        return self._bean_levels

    def is_beanLevels_allowed(self, req_type: AttReqType) -> bool:
        print(f"checking if beanLevels attribute allowed: {req_type=}")
        return self.get_state() == DevState.ON

    @attribute
    def brewingTemperature(self) -> float:
        print("reading brewing temperature")
        return self._brewing_temperature

    @brewingTemperature.setter
    def brewingTemperature(self, temperature: float):
        print("writing brewing temperature ")
        self._brewing_temperature = temperature

    @brewingTemperature.is_allowed
    def brewingTemperature(self, req_type: AttReqType) -> bool:
        print(f"checking if brewing temperature allowed: {req_type=}")
        state = self.get_state()
        if state != DevState.ON:
            action = "check" if req_type == AttReqType.READ_REQ else "change"
            raise RuntimeError(
                f"Cannot {action} settings! Machine is {state},"
                f" but needs to be {DevState.ON}. Try the On() command."
            )
        else:
            return True

    @command
    def Brew(self):
        print("brewing coffee!")

    def is_Brew_allowed(self) -> bool:
        if self._water_level < MIN_WATER_REQUIRED_FOR_BREWING_L:
            raise RuntimeError(
                f"Sorry, not enough water to brew your coffee!"
                f" There is {self._water_level*1000:.0f} ml, but we need"
                f" at least {MIN_WATER_REQUIRED_FOR_BREWING_L * 1000:.0f} ml."
                f" Add more water.  Quick!"
            )
        return True

    @command
    def On(self):
        self.set_state(DevState.ON)

    @command
    def Off(self):
        self.set_state(DevState.OFF)


if __name__ == "__main__":
    MegaCoffee3k.run_server()
