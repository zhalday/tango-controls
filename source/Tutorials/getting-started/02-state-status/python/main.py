# SPDX-FileCopyrightText: All Contributors to the Tango Controls Community tutorials
# SPDX-License-Identifier: LGPL-3.0-or-later

from tango import DevState
from tango.server import Device


class MegaCoffee3k(Device):
    def init_device(self):
        super().init_device()
        self.set_state(DevState.OFF)
        self.set_status("Hello world - device is off.")


if __name__ == "__main__":
    MegaCoffee3k.run_server()
