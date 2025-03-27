# Commands

You are going to need your coffee machines to make coffee on demand, so you'll need a way to tell the Tango device to do something.  In Tango, an action is triggered using a {term}`command`.

For starters, here are some very simple commands.  Commands have a name, an optional input parameter, and an optional return value.  Multiple parameters are not supported, and neither are complex types.
:::::{tab-set}

::::{tab-item} Python
```{literalinclude} 05-commands/python/main.py
:caption: main.py
:language: python
:emphasize-lines: 1
```
::::

::::{tab-item} C++
Sorry, still TODO!
::::

::::{tab-item} Java
Sorry, still TODO!
::::

:::::

In Python, you need to import {py:func}`~tango.server.command` and then use that to decorate a method on the {py:class}`~tango.server.Device`. In other languages, it is a little more complicated.

You have the following commands:
* `Brew` has no input or output parameters.
* `BrewNoName` has no input, but returns a string.
* `BrewName` accepts an input string and returns a string.
* `BrewNames` accepts a list of strings and returns a list of strings.
* `BrewNameDoc` shows how the input and output parameters can be documented.  There isn't a way to document the command itself.
* `BrewNameDocDtype` is the same as the previous, but shows an alternative (older) way of declaring the types.

The command names use capitalisation as per the Tango [Naming Rules](#naming-rules).

Run this example, and in a second terminal, use the [device proxy client](01-first-steps.md#first-tango-client) to check if it is working:

```python-console
>>> dp.Brew()  # nothing on client, but server will print a message
>>> dp.BrewNoName()
'brewing coffee for someone!'
>>> dp.BrewName("Java01")
'brewing coffee for Java01!'
>>> dp.BrewNames(["I", "need", "coffee"])
['brewing coffee for I!', 'brewing coffee for need!', 'brewing coffee for coffee!']
```

Calling the command as a function is a convenience provided by the `DeviceProxy` object.  You can also use the more low-level {py:meth}`~tango.DeviceProxy.command_inout` method:

```python-console
>>> dp.command_inout("BrewNoName")
'brewing coffee for someone!'
>>> dp.command_inout("BrewName", "Java01")
'brewing coffee for Java01!'
```

Tango is case insensitive when accessing commands by name, so all of the following calls access the same command:

```python-console
>>> dp.BrewNoName()
'brewing coffee for someone!'
>>> dp.brewnoname()
'brewing coffee for someone!'
>>> dp.command_inout("brewNONAME")
'brewing coffee for someone!'
```

You can also see how the documentation is available to the client:
```python-console
>>> help(dp.BrewNameDoc)
# shows:

Help on function f in module tango.device_proxy:

f(*args, **kwds)
    BrewNameDoc(DevString) -> DevString

    -  in (DevString): Name of coffee drinker
    - out (DevString): Order response

>>> print(dp.get_command_config("BrewNameDoc"))
CommandInfo[
     cmd_name = 'BrewNameDoc'
      cmd_tag = 0
   disp_level = tango._tango.DispLevel.OPERATOR
      in_type = tango._tango.CmdArgType.DevString
 in_type_desc = 'Name of coffee drinker'
     out_type = tango._tango.CmdArgType.DevString
out_type_desc = 'Order response']

>>> print(dp.get_command_config("BrewNameDocDtype"))
CommandInfo[
     cmd_name = 'BrewNameDocDtype'
      cmd_tag = 0
   disp_level = tango._tango.DispLevel.OPERATOR
      in_type = tango._tango.CmdArgType.DevString
 in_type_desc = 'Name of coffee drinker'
     out_type = tango._tango.CmdArgType.DevString
out_type_desc = 'Order response']

>>> print(dp.get_command_config("BrewName"))
CommandInfo[
     cmd_name = 'BrewName'
      cmd_tag = 0
   disp_level = tango._tango.DispLevel.OPERATOR
      in_type = tango._tango.CmdArgType.DevString
 in_type_desc = 'Uninitialised'
     out_type = tango._tango.CmdArgType.DevString
out_type_desc = 'Uninitialised']

```

The {py:meth}`~tango.DeviceProxy.get_command_config` method provides all the details about a command.

To simplify the implementation of all clients and servers, the data types available to commands are limited:
- simple types:  integer, float, string, boolean
- lists of simple types
- special structures:
  - a list of numbers combined with a list of strings:  `DevVarDoubleStringArray` and `DevVarLongStringArray`
  - an encoded byte array, with string indicating the format: `DevEncoded`

:::{tip}
For more complicated input and output data structures, it is common to use a string that is serialised and de-serialised using JSON.  This allows structures like dicts to be passed between client and server.  The downside is that the schema of those dicts is not obvious.
:::

:::{tip}
You can easily get a list of all the commands a Tango device offers:

```python-console
>>> dp.get_command_list()
['Brew', 'BrewName', 'BrewNameDoc', 'BrewNameDocDtype', 'BrewNames', 'BrewNoName', 'Init', 'State', 'Status']
```

State and Status are special, and show up as commands and attributes.  Normally we access them as commands.
Init is a built-in command.

:::

:::{note}
For PyTango, here is the full list of the [data types](inv:pytango:std:label#pytango-data-types).

Tango does not support 2-D arrays (images) for commands.
PyTango does not support enumerated types (`DevEnum`) for commands.
:::

So far, so good.  Commands were easy, next up: attributes.
