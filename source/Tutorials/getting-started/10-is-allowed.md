# Is allowed

Sometimes you'll want to prevent certain actions on the coffee machines.  For example, you definitely don't want people
trying to brew coffee if the water level is too low - they'll end up burning out the machine! This kind of business
logic and state handling can be partially achieved with Tango's concept of *is allowed* methods.  Each {term}`attribute`
and {term}`command` can have a custom method that is automatically called as a check, or guard, before invoking the
attribute or command handler.

These methods must return a boolean value (true or false).  If the method returns true, the Tango device can continue
with reading or writing the attribute, or executing the command.  If the method returns false, or raises an exception,
the client is informed that their request was denied.

:::::{tab-set}

::::{tab-item} Python
```{literalinclude} 10-is-allowed/python/main.py
:caption: main.py
:language: python
:lines: 4-
:emphasize-lines: 22-24,31-33,45-56,62-70
```
::::

::::{tab-item} C++
Sorry, still TODO!
::::

::::{tab-item} Java
Sorry, still TODO!
::::

:::::

The convention for naming these guard methods follows the pattern `is_<name>_allowed`.
Where `<name>` is replaced with the Tango attribute or command name.

In Python high-level devices there are a few ways to link these guard methods to a specific attribute or command:
- Naming convention.  Methods named according to the convention above are automatically discovered and used.
  For example, the `is_waterLevel_allowed` method.
  This is called whenever a client tries to read the `waterLevel` attribute.
  You also see `is_Brew_allowed` which will be called when the `Brew` command is attempted.
- The `fisallowed` keyword argument. It can name the method on the device class as a string,
  like `"is_beanLevels_allowed"`, for the `beanLevels` attribute.
  If the guard function is already available (defined before the class), then it can be used directly
  instead of a string.
- Attribute decorator `.is_allowed`.
  This is used like `@brewingTemperature.is_allowed`, linking the decorated method to
  the `brewingTemperature` attribute.
  There is no equivalent for commands.

[Run this example](#tut-01-run-server-no-db),
and in a second terminal, use the [device proxy client](01-first-steps.md#first-tango-client) to check if it is working:

```python-console
>>> dp.waterLevel
...
tango._tango.DevFailed: DevFailed[
    DevError[
        desc = It is currently not allowed to read attribute waterLevel
        origin = void Tango::Device_3Impl::read_attributes_no_except(const Tango::DevVarStringArray &, Tango::AttributeIdlData &, bool, std::vector<long> &) at (/Users/runner/miniforge3/conda-bld/cpptango_1758200193404/work/src/server/device_3.cpp:983)
        reason = API_AttrNotAllowed
        severity = ERR
    ],
    DevError[
        desc = Failed to read_attribute on device test/nodb/megacoffee3k, attribute waterLevel
        origin = virtual DeviceAttribute Tango::DeviceProxy::read_attribute(const std::string &) at (/Users/runner/miniforge3/conda-bld/cpptango_1758200193404/work/src/client/devapi_base.cpp:6285)
        reason = API_AttributeFailed
        severity = ERR
    ]
]
```

Notice that it doesn't tell use *why* you cannot read the `waterLevel`.
It just has a generic "it is currently not allowed" message.
This is what happens if you simply return false from an is-allowed method - Tango cannot give us any further info.

If you want to provide the user with more information, you should raise an exception in the
is-allowed method.  That is what happens with `brewingTemperature`:

```python-console
>>> dp.brewingTemperature
...
tango._tango.DevFailed: DevFailed[
    DevError[
        desc = RuntimeError: Cannot check settings! Machine is OFF, but needs to be ON. Try the On() command.
        origin = Traceback (most recent call last):
              ...
        reason = PyDs_PythonError
        severity = ERR
    ],
    DevError[
        desc = Failed to read_attribute on device test/nodb/megacoffee3k, attribute brewingTemperature
        origin = virtual DeviceAttribute Tango::DeviceProxy::read_attribute(const std::string &) at (/Users/runner/miniforge3/conda-bld/cpptango_1758200193404/work/src/client/devapi_base.cpp:6285)
        reason = API_AttributeFailed
        severity = ERR
    ]
]
>>> dp.brewingTemperature = 95
Traceback (most recent call last):
   ...
```

The is-allowed method for attributes gets the request type as a parameter.
This means you can have different behaviour depending on what the caller is doing.
Maybe you always want to allow reading, but have some rules limiting writing.
In the example code, the `req_type` parameter is checked.

:::::{tab-set}

::::{tab-item} Python
```{literalinclude} 10-is-allowed/python/main.py
:caption: main.py
:language: python
:lines: 48-59
:emphasize-lines: 2,6
```
::::

::::{tab-item} C++
Sorry, still TODO!
::::

::::{tab-item} Java
Sorry, still TODO!
::::

:::::

You can see the device server prints out that the is-allowed methods were called:

```
$ python -m tango.test_context main.MegaCoffee3k --host 127.0.0.1
Ready to accept request
...
checking if waterLevel attribute allowed: req_type=<AttReqType.READ_REQ: 0>
checking if brewing temperature allowed: req_type=<AttReqType.READ_REQ: 0>
checking if brewing temperature allowed: req_type=<AttReqType.WRITE_REQ: 1>
```

If you turn the device on first, then the attributes can be read:

```python-console
>>> dp.On()
>>> dp.waterLevel
0.1
>>> dp.brewingTemperature
94.4
```

When you use the `Brew` command, it fails too, as expected.

```python-console
>>> dp.Brew()
...
tango._tango.DevFailed: DevFailed[
    DevError[
        desc = RuntimeError: Sorry, not enough water to brew your coffee! There is 100 ml, but we need at least 200 ml. Add more water.  Quick!
        origin = Traceback (most recent call last):
              ...
        reason = PyDs_PythonError
        severity = ERR
    ],
    DevError[
        desc = Failed to execute command_inout on device test/nodb/megacoffee3k, command Brew
        origin = virtual DeviceData Tango::Connection::command_inout(const std::string &, const DeviceData &) at (/Users/runner/miniforge3/conda-bld/cpptango_1758200193404/work/src/client/devapi_base.cpp:2029)
        reason = API_CommandFailed
        severity = ERR
    ]
]
```

Hooray - our coffee machines are a bit safer!
