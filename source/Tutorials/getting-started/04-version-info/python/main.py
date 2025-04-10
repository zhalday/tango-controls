# SPDX-FileCopyrightText: All Contributors to the Tango Controls Community tutorials
# SPDX-License-Identifier: LGPL-3.0-or-later

from tango.server import Device

__version__ = "0.1.0"


class MegaCoffee3k(Device):

    def init_device(self):
        super().init_device()
        self.add_version_info("MegaCoffee3k.Name", "MegaCoffee3k Tango device")
        self.add_version_info("MegaCoffee3k.Source", __file__)
        self.add_version_info("MegaCoffee3k.Version", __version__)
        self.add_version_info(
            "MegaCoffee3k.Repo",
            "https://gitlab.tango-mega-corp.com/controls/dev-tmc-megacoffee3k",
        )


if __name__ == "__main__":
    MegaCoffee3k.run_server()
