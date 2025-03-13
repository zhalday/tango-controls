from tango.server import Device, command


class MegaCoffee3k(Device):

    @command
    def brew(self):
        print("brewing coffee! (but nobody knows)")

    @command
    def brew_no_name(self) -> str:
        return "brewing coffee for someone!"

    @command
    def brew_name(self, name: str) -> str:
        return f"brewing coffee for {name}!"

    @command
    def brew_names(self, names: list[str]) -> list[str]:
        return [f"brewing coffee for {name}!" for name in names]

    @command(doc_in="Name of coffee drinker", doc_out="Order response")
    def brew_name_doc(self, name: str) -> str:
        return f"brewing coffee for {name}!"

    @command(
        dtype_in=str,
        doc_in="Name of coffee drinker",
        dtype_out=str,
        doc_out="Order response",
    )
    def brew_name_doc_dtype(self, name):
        return f"brewing coffee for {name}!"


if __name__ == "__main__":
    MegaCoffee3k.run_server()
