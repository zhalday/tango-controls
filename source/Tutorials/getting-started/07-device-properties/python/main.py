# SPDX-FileCopyrightText: All Contributors to the Tango Controls Community tutorials
# SPDX-License-Identifier: LGPL-3.0-or-later

from tango.server import Device, device_property


class MegaCoffee3k(Device):

    host: str = device_property(mandatory=True)
    port: int = device_property(default_value=9788)
    location: str = device_property()

    def init_device(self):
        print(f"init_device before super: {self.host}:{self.port} @ {self.location}")
        super().init_device()
        print(f"init_device after super: {self.host}:{self.port} @ {self.location}")


if __name__ == "__main__":
    MegaCoffee3k.run_server()
