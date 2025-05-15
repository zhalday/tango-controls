# About and version info

Tango devices are discoverable on the network, and their APIs can be queried.  They can also provide general information about themselves that is easily accessible by clients.  You know that source version info is important for debugging issues in production!  Luckily, it is super easy to add extra details to your Tango device.

:::::{tab-set}

::::{tab-item} Python
```{literalinclude} 04-version-info/python/main.py
:caption: main.py
:language: python
:lines: 4-
:emphasize-lines: 10-16
```
::::

::::{tab-item} C++
Sorry, still TODO!
::::

::::{tab-item} Java
Sorry, still TODO!
::::

:::::

The {py:meth}`~tango.server.Device.add_version_info` method can be called as many times as you like to add key-value pairs of strings.

If you run this example, and in a second terminal, use the [device proxy client](01-first-steps.md#first-tango-client) to read back the information:

```python-console
>>> dp.info()
DeviceInfo(dev_class = 'MegaCoffee3k', dev_type = 'MegaCoffee3k', doc_url = 'Doc URL = http://www.tango-controls.org', server_host = 'my.computer', server_id = 'MegaCoffee3k/MegaCoffee3k', server_version = 6, version_info = {'Build.PyTango.NumPy': '2.2.3', 'Build.PyTango.Pybind11': '2.13.6', 'Build.PyTango.Python': '3.13.2', 'Build.PyTango.cppTango': '10.0.2', 'MegaCoffee3k.Name': 'MegaCoffee3k Tango device', 'MegaCoffee3k.Repo': 'https://gitlab.tango-mega-corp.com/controls/dev-tmc-megacoffee3k', 'MegaCoffee3k.Source': '/path/to/tango-tut/src/04-version-info/python/main.py', 'MegaCoffee3k.Version': '0.1.0', 'NumPy': '2.2.3', 'PyTango': '10.1.0rc2', 'Python': '3.13.2', 'cppTango': '10.0.2', 'cppTango.git_revision': 'unknown', 'cppzmq': '41000', 'idl': '6.0.2', 'omniORB': '4.3.2', 'opentelemetry-cpp': '1.18.0', 'zmq': '40305'})
>>> print(dp.info())
DeviceInfo[
    dev_class = "MegaCoffee3k"
    dev_type = "MegaCoffee3k"
    doc_url = "Doc URL = http://www.tango-controls.org"
    server_host = "my.computer"
    server_id = "MegaCoffee3k/MegaCoffee3k"
    server_version = 6
    version_info = {
        "Build.PyTango.NumPy": "2.2.3",
        "Build.PyTango.Pybind11": "2.13.6",
        "Build.PyTango.Python": "3.13.2",
        "Build.PyTango.cppTango": "10.0.2",
        "MegaCoffee3k.Name": "MegaCoffee3k Tango device",
        "MegaCoffee3k.Repo": "https://gitlab.tango-mega-corp.com/controls/dev-tmc-megacoffee3k",
        "MegaCoffee3k.Source": "/path/to/tango-tut/src/04-version-info/python/main.py",
        "MegaCoffee3k.Version": "0.1.0",
        "NumPy": "2.2.3",
        "PyTango": "10.1.0rc2",
        "Python": "3.13.2",
        "cppTango": "10.0.2",
        "cppTango.git_revision": "unknown",
        "cppzmq": "41000",
        "idl": "6.0.2",
        "omniORB": "4.3.2",
        "opentelemetry-cpp": "1.18.0",
        "zmq": "40305"
    }
]
```

Using `print` gives us a much more readable ouput of the data structure.

::::{admonition} Bonus tip: getting project URL in Python
:class: dropdown, tip

Given `pyproject.toml` with:

:::{code-block} toml
[project]
name = "tangods-megacoffee3k"

[project.urls]
Source = "https://gitlab.tango-mega-corp.com/controls/dev-tmc-megacoffee3k"

:::

This code can fetch the URL at runtime:

:::{code-block} python
import importlib.metadata

def _get_repo_info_from_package() -> str:
    try:
        metadata = importlib.metadata.metadata("tangods-megacoffee3k")
        repo_url = (
            metadata["Project-URL"].split(" ")[1]
            if "Project-URL" in metadata
            else "Unknown"
        )
    except importlib.metadata.PackageNotFoundError:
        repo_url = "Unknown"
    return repo_url

:::


::::

Next up, you'll add a command so the device can finally do something!
