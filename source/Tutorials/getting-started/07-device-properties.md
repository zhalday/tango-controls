# Device properties

You are definitely going to need more than one coffee machine to satisfy all your colleagues!
With one Tango device per coffee machine, you'll need to provided network connection details to use for each one.
You know that hard-coding that information in your source files is a bad idea, so how can you make it configurable?
The answer is to use a {term}`property` in Tango.  There are a few different types, but we'll use a device property.

The values of the device properties are stored in the {term}`Tango Database`, so they can persist.  Every time the device
starts up, it reads the property values from the database. You'll learn more about the database later.

:::::{tab-set}

::::{tab-item} Python
```{literalinclude} 07-device-properties/python/main.py
:caption: main.py
:language: python
:emphasize-lines: 1,6,7,8
```
::::

::::{tab-item} C++
Sorry, still TODO!
::::

::::{tab-item} Java
Sorry, still TODO!
::::

:::::

In Python, you import {py:class}`~tango.server.device_property` and use it to define you properties.

You've defined three device properties:
- The host name, a string with no default, and `mandatory` set to true, so it has to be configured.
- The port number, an integer with default.  Most machines will use the same TCP port.
- The location at MegaCorp, an optional string with no default.


Now when you run the Tango device server, using PyTango's `test_context` utility we will get an error:
```console
(tango-tut) $ python -m tango.test_context main.MegaCoffee3k --host 127.0.0.1
```


```{code-block} console
:emphasize-lines: 7,9,23-25
init_device before super: None:None @ None
Traceback (most recent call last):
...
  File "/path/to/pytango/tango/server.py", line 1694, in tango_loop
    util.server_init()
    ~~~~~~~~~~~~~~~~^^
tango._tango.PyTango.DevFailed: DevFailed[
    DevError[
        desc = Exception: Device property host is mandatory
        origin = Traceback (most recent call last):
              File "/path/to/pytango/tango/device_class.py", line 648, in __DeviceClass__device_factory
                device = self._new_device(deviceImplClass, klass, dev_name)
              File "/path/to/pytango/tango/device_class.py", line 627, in __DeviceClass__new_device
                return klass(dev_class, dev_name)
              File "/path/to/pytango/tango/server.py", line 806, in __init__
                self.init_device()
                ~~~~~~~~~~~~~~~~^^
              File "/path/to/pytango/tango/server.py", line 404, in init_device
                return worker.execute(init_device_orig, self)
                       ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
              File "/path/to/pytango/tango/green.py", line 105, in execute
                return fn(*args, **kwargs)
              File "/path/to/tango-tut/src/07-device-properties/python/main.py", line 12, in init_device
                super().init_device()
                ~~~~~~~~~~~~~~~~~~~^^
              File "/path/to/pytango/tango/server.py", line 404, in init_device
                return worker.execute(init_device_orig, self)
                       ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
              File "/path/to/pytango/tango/green.py", line 105, in execute
                return fn(*args, **kwargs)
              File "/path/to/pytango/tango/server.py", line 825, in init_device
                self.get_device_properties()
                ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
              File "/path/to/pytango/tango/server.py", line 877, in get_device_properties
                raise Exception(msg)
            Exception: Device property host is mandatory
        reason = PyDs_PythonError
        severity = ErrSeverity.ERR
    ]
]
```

You don't have a real database to store the property values yet, but they can be provided on the command line when
launching the device server via the `--prop` argument:

```console
(tango-tut) $ python -m tango.test_context main.MegaCoffee3k --prop '{"host": "localhost"}' --host 127.0.0.1
```

```{code-block} console
:emphasize-lines: 1,2
init_device before super: None:None @ None
init_device after super: localhost:9788 @ None
Ready to accept request
MegaCoffee3k started on port 8888 with properties {'host': 'localhost'}
Device access: tango://127.0.0.1:8888/test/nodb/megacoffee3k#dbase=no
Server access: tango://127.0.0.1:8888/dserver/MegaCoffee3k/megacoffee3k#dbase=no
```

This time you see no errors.  The printout shows that before the `super().init_device()` call the property values
were `None`, but after the call, you have the expected values:  `"localhost"`, which you provided, and the default
port number of `9788`.  The location wasn't provided, so it still has the value `None`.

Now you provide the location as well:

```console
(tango-tut) $ python -m tango.test_context main.MegaCoffee3k --prop '{"host": "localhost", "location": "control room"}' --host 127.0.0.1
```

```{code-block} console
:emphasize-lines: 2
init_device before super: None:None @ None
init_device after super: localhost:9788 @ control room
Ready to accept request
MegaCoffee3k started on port 8888 with properties {'host': 'localhost', 'location': 'control room'}
Device access: tango://127.0.0.1:8888/test/nodb/megacoffee3k#dbase=no
Server access: tango://127.0.0.1:8888/dserver/MegaCoffee3k/megacoffee3k#dbase=no
```

Next up, you'll look into using an external Tango database for persisting and configuring these values.
