# SPDX-FileCopyrightText: All Contributors to the Tango Controls Community tutorials
# SPDX-License-Identifier: LGPL-3.0-or-later

from tango.server import Device

class MegaCoffee3k(Device):
    pass


if __name__ == "__main__":
    MegaCoffee3k.run_server()
