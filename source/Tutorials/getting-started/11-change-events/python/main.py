# SPDX-FileCopyrightText: All Contributors to the Tango Controls Community tutorials
# SPDX-License-Identifier: MIT-0

import random

import RPi.GPIO as GPIO
from tango import DevState
from tango.server import Device, attribute, command, device_property


class LedDevice(Device):

    gpio_pin: int = device_property(default_value=17)

    def init_device(self):
        super().init_device()
        self._led_on = False
        self._random_number = 0.0
        self.set_state(DevState.OFF)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT, initial=GPIO.LOW)
        self.set_change_event("ledOn", True, False)
        self.set_change_event("randomNumber", True, True)

    def delete_device(self):
        GPIO.cleanup()
        super().delete_device()

    @attribute(dtype=bool)
    def ledOn(self) -> bool:
        return self._led_on

    @command(dtype_in=bool, doc_in="True to switch the LED on, False to switch it off")
    def SetLed(self, on: bool):
        self._led_on = on
        GPIO.output(self.gpio_pin, GPIO.HIGH if on else GPIO.LOW)
        self.set_state(DevState.ON if on else DevState.OFF)
        self.push_change_event("ledOn", self._led_on)

    @attribute(dtype=float, abs_change=0.001)
    def randomNumber(self) -> float:
        return self._random_number

    @command
    def GenerateRandomNumber(self):
        self._random_number = random.random()
        self.push_change_event("randomNumber", self._random_number)


if __name__ == "__main__":
    LedDevice.run_server()
