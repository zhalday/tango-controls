# First steps

## First Tango device server

You start with the simplest Tango device to control one of these coffee machines:

:::::{tab-set}

::::{tab-item} Python
```{literalinclude} src/python/01/main.py
:caption: main.py
:language: python
```
::::

::::{tab-item} Pogo (C++)
```{literalinclude} src/cpp/01/MegaCoffee3k.xmi
:caption: MegaCoffee3k.xmi
:language: xml
```
::::

::::{tab-item} C++
```{literalinclude} src/cpp/01/main.cpp
:caption: main.cpp
:language: cpp
```

```{literalinclude} src/cpp/01/MegaCoffee3kClass.h
:caption: MegaCoffee3kClass.h
:language: cpp
```

```{literalinclude} src/cpp/01/MegaCoffee3kClass.cpp
:caption: MegaCoffee3kClass.cpp
:language: cpp
```

```{literalinclude} src/cpp/01/MegaCoffee3k.h
:caption: MegaCoffee3k.h
:language: cpp
```

```{literalinclude} src/cpp/01/MegaCoffee3k.cpp
:caption: MegaCoffee3k.cpp
:language: cpp
```

```{literalinclude} src/cpp/01/MegaCoffee3kStateMachine.cpp
:caption: MegaCoffee3kStateMachine.cpp
:language: cpp
```

```{literalinclude} src/cpp/01/CMakeLists.txt
:caption: CMakeLists.txt
:language: cmake
```
::::

::::{tab-item} Pogo (Java)
```{literalinclude} src/java/01/MegaCoffee3k.xmi
:caption: MegaCoffee3k.xmi
:language: xml
```
::::

::::{tab-item} Java
```{literalinclude} src/java/01/org/tango/megacoffee3k/MegaCoffee3k.java
:caption: MegaCoffee3k.java
:language: java
```
::::

:::::

For the Python example, copy that to a file `main.py`.

Make sure your [Pixi shell](tutorial.md#installation) is active, so the prompt should look something
like this.
```console
(tango-tut) $
```

Now you can run your first Tango device server, using PyTango's `test_context` utility:
```console
(tango-tut) $ python -m tango.test_context main.MegaCoffee3k --host 127.0.0.1
```

You see the output:
```{code-block} console
:emphasize-lines: 2
Can't create notifd event supplier. Notifd event not available
Ready to accept request
MegaCoffee3k started on port 8888 with properties {}
Device access: tango://127.0.0.1:8888/test/nodb/megacoffee3k#dbase=no
Server access: tango://127.0.0.1:8888/dserver/MegaCoffee3k/megacoffee3k#dbase=no
```

The `Ready to accept request` line tells you that device server has started up.

The lines after that are from the "test context" used to launch it.  You'll use the cryptic `Device access` part
in the next section.

:::{hint}
Don't worry about the `notifd` warning, if you see it.  It isn't used in newer Tango systems.
:::

::::{admonition} Troubleshooting errors when launching
:class: dropdown, tip

If TCP port 8888 is already in use on your system, you'll get an error like this:
```console
omniORB: (? 6151811072) 2024-10-28 08:05:02.317646: Failed to bind to address 127.0.0.1 port 10000. Address in use?
omniORB: (? 6151811072) 2024-10-28 08:05:02.317662: Error: Unable to create an endpoint of this description: giop:tcp:127.0.0.1:10000
```

Try a different port number, like 8889:
```console
(tango-tut) $ python -m tango.test_context main.MegaCoffee3k --host 127.0.0.1 --port 8889
```

---

If you get something like

```console
zsh: command not found: python
```

Or

```console
python3.11: Error while finding module specification for 'tango.test_context' (ModuleNotFoundError: No module named 'tango')
```

Then your Pixi shell might not be activated.  Try this, and check the [Pixi installation](tutorial.md#installation) again.
```console
$ pixi shell
```

Or, if you're not using Pixi, your virtual environment isn't active, or you haven't installed PyTango.

::::


## First Tango client

Tango uses a distributed client-server architecture.  Now that you have your *MegaCoffee3k* device server running,
you need to connect a client.

Start a new terminal, so that the server keeps running in the old terminal.  Again, activate your environment.

```console
$ pixi shell
(tango-tut) $ python
```

We use PyTango, and the *Device access* Tango resource locator, `tango://127.0.0.1:8888/test/nodb/megacoffee3k#dbase=no`
to connect our client, a Tango *Device Proxy*.

```python-console
>>> import tango
>>> dp = tango.DeviceProxy("tango://127.0.0.1:8888/test/nodb/megacoffee3k#dbase=no")
>>> dp.ping()
382
>>> dp.State()
tango._tango.DevState.UNKNOWN
>>> dp.Status()
'The device is in UNKNOWN state.'
>>>
```

It works!  That was super east, but it isn't super useful yet.  Read on!

:::{hint}
If you're wondering, the value `382` is the ping response time in microseconds.
:::

::::{admonition} Troubleshooting errors when using the client
:class: dropdown, tip

```python-console
>>> dp.ping()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/projects/tango-tut/.pixi/envs/default/lib/python3.12/site-packages/tango/green.py", line 234, in greener
    return executor.run(fn, args, kwargs, wait=wait, timeout=timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/projects/tango-tut/.pixi/envs/default/lib/python3.12/site-packages/tango/green.py", line 124, in run
    return fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^
  File "/Users/projects/tango-tut/.pixi/envs/default/lib/python3.12/site-packages/tango/device_proxy.py", line 1974, in __DeviceProxy__ping
    return self._ping(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
PyTango.DevFailed: DevFailed[
DevError[
    desc = TRANSIENT CORBA system exception: TRANSIENT_ConnectFailed
  origin = void Tango::Connection::connect(const std::string &) at (/Users/runner/miniforge3/conda-bld/cpptango_1729356321178/work/src/client/devapi_base.cpp:633)
  reason = API_CorbaException
severity = ERR]

DevError[
    desc = Failed to connect to device test/nodb/megacoffee3k
  origin = void Tango::Connection::connect(const std::string &) at (/Users/runner/miniforge3/conda-bld/cpptango_1729356321178/work/src/client/devapi_base.cpp:633)
  reason = API_ServerNotRunning
severity = ERR]
]
```

This means the device server is not running.   Make sure it is still running in a different terminal.
```console
(tango-tut) $ python -m tango.test_context main.MegaCoffee3k --host 127.0.0.1
```

::::

## Finishing up

You can use the keyboard combination `Ctrl`+`C` to end the Tango device server application.

```{code-block} console
:emphasize-lines: 6
Can't create notifd event supplier. Notifd event not available
Ready to accept request
MegaCoffee3k started on port 8888 with properties {}
Device access: tango://127.0.0.1:8888/test/nodb/megacoffee3k#dbase=no
Server access: tango://127.0.0.1:8888/dserver/MegaCoffee3k/megacoffee3k#dbase=no
^CDone
(tango-tut) $
```

Similarly, you can exit the Python interpreter console when you are done with the client.
