# State and Status

All Tango devices automatically provide *State* and *Status* information that can be queried at any time.

In the [previous lesson](01-first-steps.md#first-tango-client) you saw that this was just `UNKNOWN` and `'The device is in UNKNOWN state.'`
for your first device.  You want to make this a little better.

:::::{tab-set}

::::{tab-item} Python
```{literalinclude} src/python/02/main.py
:caption: main.py
:language: python
:emphasize-lines: 8,9
```
::::

::::{tab-item} Pogo (C++)
```{literalinclude} src/cpp/02/MegaCoffee3k.xmi
:caption: MegaCoffee3k.xmi
:language: xml
```
::::

::::{tab-item} C++
```{literalinclude} src/cpp/02/main.cpp
:caption: main.cpp
:language: cpp
```

```{literalinclude} src/cpp/02/MegaCoffee3kClass.h
:caption: MegaCoffee3kClass.h
:language: cpp
```

```{literalinclude} src/cpp/02/MegaCoffee3kClass.cpp
:caption: MegaCoffee3kClass.cpp
:language: cpp
```

```{literalinclude} src/cpp/02/MegaCoffee3k.h
:caption: MegaCoffee3k.h
:language: cpp
```

```{literalinclude} src/cpp/02/MegaCoffee3k.cpp
:caption: MegaCoffee3k.cpp
:language: cpp
```

```{literalinclude} src/cpp/02/MegaCoffee3kStateMachine.cpp
:caption: MegaCoffee3kStateMachine.cpp
:language: cpp
```

```{literalinclude} src/cpp/02/CMakeLists.txt
:caption: CMakeLists.txt
:language: cmake
```
::::

::::{tab-item} Pogo (Java)
```{literalinclude} src/java/02/MegaCoffee3k.xmi
:caption: MegaCoffee3k.xmi
:language: xml
```
::::

::::{tab-item} Java
```{literalinclude} src/java/02/org/tango/megacoffee3k/MegaCoffee3k.java
:caption: MegaCoffee3k.java
:language: java
```
::::

:::::

Here the `set_state` and `set_status` methods have been used to modify the device's state and status on startup.

If you run this example, and in a second terminal, use the [device proxy client](01-first-steps.md#first-tango-client) to check if it is working  :

```python-console
>>> dp.State()
tango._tango.DevState.OFF
>>> dp.Status()
'Hello world - device is off.'
>>>
```

It works, super easy!  Nice.

:::{tip}
It is good practice to set the state and status values at the same time, since
clients will often read both of them, and they need to agree.
:::

There `DevState` enum has many values, but the other common ones are `STANDBY`, `ON`, `RUNNING`, `ALARM`, and `FAULT`.

But what was that `init_device` method?  It is part of the device implementation class, and
it is called automatically when the device starts up.  You'll learn more about it soon.
