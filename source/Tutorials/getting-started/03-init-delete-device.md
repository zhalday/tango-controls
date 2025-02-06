# Init and Delete Device

The basic lifecycle of a Tango {term}`device` can be simplified into two parts:  initialisation and clean-up.
This happens within the operating system process that is called the {term}`device server`.

As you saw in the [previous lesson](02-state-status.md#state-and-status) there is an {py:meth}`~tango.server.Device.init_device` method.  Your device can also have a {py:meth}`~tango.server.Device.delete_device` method.  Both of these override the default implementation in the base class {py:class}`~tango.server.Device`.

:::::{tab-set}

::::{tab-item} Python
```{literalinclude} 03-init-delete-device/python/main.py
:caption: main.py
:language: python
:emphasize-lines: 15,16,17
```
::::


::::{tab-item} C++
Sorry, still TODO!
::::

::::{tab-item} Java
Sorry, still TODO!
::::

:::::

Here the `init_device` and `delete_device` methods simply print a message.
The`__init__` method is included with some print statements to show when it is called in the lifecycle.

:::{tip}
It is important to still call the super class methods, as shown.  `init_device` at the
start of your method, and `delete_device` at the end of your method.
:::

::::{admonition} Bonus tip: `__init__`
:class: dropdown, tip
Device methods that use the Tango "machinery" cannot be called
before `Device.__init__` has completed.  E.g., the logging methods like `info_stream`,
and things like `push_change_event`, which you'll learn about later.
::::

Run this example server, and you'll see the output:
```{code-block} console
:emphasize-lines: 1,2,3
MegaCoffee3k: __init__ start
MegaCoffee3k: init_device
MegaCoffee3k: __init__ end
Ready to accept request
MegaCoffee3k started on port 8888 with properties {}
Device access: tango://127.0.0.1:8888/test/nodb/megacoffee3k#dbase=no
Server access: tango://127.0.0.1:8888/dserver/MegaCoffee3k/megacoffee3k#dbase=no
```

The "init_device" message is printed *before* the device is ready to accept requests.
In this Python example, the `init_device` call came from the base class constructor, `Device.__init__`.

In a second terminal, use the [device proxy client](01-first-steps.md#first-tango-client) and send the built-in
`Init()` command, which will re-initialise the device.

```python-console
>>> dp.Init()
>>>
```

```{code-block} console
:emphasize-lines: 8,9
MegaCoffee3k: __init__ start
MegaCoffee3k: init_device
MegaCoffee3k: __init__ end
Ready to accept request
MegaCoffee3k started on port 8888 with properties {}
Device access: tango://127.0.0.1:8888/test/nodb/megacoffee3k#dbase=no
Server access: tango://127.0.0.1:8888/dserver/MegaCoffee3k/megacoffee3k#dbase=no
MegaCoffee3k: delete_device
MegaCoffee3k: init_device
```

To re-initialise the MegaCoffee3k device, Tango first calls the `delete_device`
method, and then the `init_device` method.  The constructor, `__init__`, is not called, so
you still have the same Python object instance.

Finally, use the keyboard combination `Ctrl`+`C` to end the Tango device server application.

```{code-block} console
:emphasize-lines: 10
MegaCoffee3k: __init__ start
MegaCoffee3k: init_device
MegaCoffee3k: __init__ end
Ready to accept request
MegaCoffee3k started on port 8888 with properties {}
Device access: tango://127.0.0.1:8888/test/nodb/megacoffee3k#dbase=no
Server access: tango://127.0.0.1:8888/dserver/MegaCoffee3k/megacoffee3k#dbase=no
MegaCoffee3k: delete_device
MegaCoffee3k: init_device
^CMegaCoffee3k: delete_device
Done
```

You can see that `delete_device` method was called again during the graceful shutdown.

:::{tip}
Variables needed for the device state are normally initialised in `init_device` rather than
in `__init__`, since `init_device` gets called again when the `Init()` command is used.
:::

:::{tip}
If any system resources (memory, connections, file handles, etc.) need to be released when
the device shuts down, this kind of clean-up is usually done in `delete_device`.
:::

## Restarting the device

Using the [admin device](#admin-device-hint), you can restart the device completely, while
the device server, i.e., operating system process, remains running.  This is typically done
less often than calling `Init()` on the device.

Start your example device server again.

Create another client, this time using the *Server access* Tango resource locator.
Send the built-in `DevRestart()` command, with the name of the device: `test/nodb/megacoffee3k`.

```python-console
>>> import tango
>>> ap = tango.DeviceProxy("tango://127.0.0.1:8888/dserver/MegaCoffee3k/megacoffee3k#dbase=no")
>>> ap.DevRestart("test/nodb/megacoffee3k")
>>>
```

You'll see the following output:
```{code-block} console
:emphasize-lines: 8,9,10,11
MegaCoffee3k: __init__ start
MegaCoffee3k: init_device
MegaCoffee3k: __init__ end
Ready to accept request
MegaCoffee3k started on port 8888 with properties {}
Device access: tango://127.0.0.1:8888/test/nodb/megacoffee3k#dbase=no
Server access: tango://127.0.0.1:8888/dserver/MegaCoffee3k/megacoffee3k#dbase=no
MegaCoffee3k: delete_device
MegaCoffee3k: __init__ start
MegaCoffee3k: init_device
MegaCoffee3k: __init__ end
```

This time you notice a second call to `__init__`, so a new instance of the Python object
representing the device has been created.

::::{admonition} Bonus tip: `RestartServer`
:class: dropdown, tip
The admin device also has a `RestartServer()` command than can be used to restart all
the devices in a server, without naming a specific one.  In this example `ap.RestartServer()`.
::::

## Summary

There are various ways of restarting/re-initialising a Tango device.  From least to most drastic:

| What?                  | How?                                                     | Process   | Object    |
|------------------------|----------------------------------------------------------|-----------|-----------|
| Re-initialise device   | Send `Init()` command to device                          | Unchanged | Unchanged |
| Re-start device        | Send `DevRestart()` or `RestartServer()` to admin device | Unchanged | New       |
| Re-start device server | Terminate operating system process and run it again      | New       | New       |
