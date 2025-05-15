# SPDX-FileCopyrightText: All Contributors to the Tango Controls Community tutorials
# SPDX-License-Identifier: MIT-0

from tango.server import Device, command


class MegaCoffee3k(Device):

    @command
    def Brew(self):
        print("brewing coffee! (but nobody knows)")

    @command
    def BrewNoName(self) -> str:
        return "brewing coffee for someone!"

    @command
    def BrewName(self, name: str) -> str:
        return f"brewing coffee for {name}!"

    @command
    def BrewNames(self, names: list[str]) -> list[str]:
        return [f"brewing coffee for {name}!" for name in names]

    @command(doc_in="Name of coffee drinker", doc_out="Order response")
    def BrewNameDoc(self, name: str) -> str:
        return f"brewing coffee for {name}!"

    @command(
        dtype_in=str,
        doc_in="Name of coffee drinker",
        dtype_out=str,
        doc_out="Order response",
    )
    def BrewNameDocDtype(self, name):
        return f"brewing coffee for {name}!"


if __name__ == "__main__":
    MegaCoffee3k.run_server()
