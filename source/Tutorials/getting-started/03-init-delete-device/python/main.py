# SPDX-FileCopyrightText: All Contributors to the Tango Controls Community tutorials
# SPDX-License-Identifier: MIT-0

from tango.server import Device


class MegaCoffee3k(Device):

    # __init__ method is included to show when it is called in the lifecycle
    def __init__(self, *args, **kwargs):
        print("MegaCoffee3k: __init__ start")
        super().__init__(*args, **kwargs)
        print("MegaCoffee3k: __init__ end")

    def init_device(self):
        super().init_device()
        print("MegaCoffee3k: init_device")

    def delete_device(self):
        print("MegaCoffee3k: delete_device")
        super().delete_device()


if __name__ == "__main__":
    MegaCoffee3k.run_server()
