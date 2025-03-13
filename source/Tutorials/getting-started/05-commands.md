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
* `brew` has no input or output parameters.
* `brew_no_name` has no input, but returns a string.
* `brew_name` accepts an input string and returns a string.
* `brew_names` accepts a list of strings and returns a list of strings.
* `brew_name_doc` shows how the input and output parameters can be documented.  There isn't a way to document the command itself.
* `brew_name_doc_dtype` is the same as the previous, but shows an alternative (older) way of declaring the types.

Run this example, and in a second terminal, use the [device proxy client](01-first-steps.md#first-tango-client) to check if it is working  :

```python-console
>>> dp.brew()  # nothing on client, but server will print a message
>>> dp.brew_no_name()
'brewing coffee for someone!'
>>> dp.brew_name("Java01")
'brewing coffee for Java01!'
>>> dp.brew_names(["I", "need", "coffee"])
['brewing coffee for I!', 'brewing coffee for need!', 'brewing coffee for coffee!']
```

You can also see how the documentation is available to the client:
```python-console
>>> help(dp.brew_name_doc)
# shows:

Help on function f in module tango.device_proxy:

f(*args, **kwds)
    brew_name_doc(DevString) -> DevString

    -  in (DevString): Name of coffee drinker
    - out (DevString): Order response

>>> print(dp.get_command_config("brew_name_doc"))
CommandInfo[
     cmd_name = 'brew_name_doc'
      cmd_tag = 0
   disp_level = tango._tango.DispLevel.OPERATOR
      in_type = tango._tango.CmdArgType.DevString
 in_type_desc = 'Name of coffee drinker'
     out_type = tango._tango.CmdArgType.DevString
out_type_desc = 'Order response']

>>> print(dp.get_command_config("brew_name_doc_dtype"))
CommandInfo[
     cmd_name = 'brew_name_doc_dtype'
      cmd_tag = 0
   disp_level = tango._tango.DispLevel.OPERATOR
      in_type = tango._tango.CmdArgType.DevString
 in_type_desc = 'Name of coffee drinker'
     out_type = tango._tango.CmdArgType.DevString
out_type_desc = 'Order response']

>>> print(dp.get_command_config("brew_name"))
CommandInfo[
     cmd_name = 'brew_name'
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

:::{note}
For PyTango, here is the full list of the [data types](inv:pytango:std:label#pytango-data-types).

Tango does not support 2-D arrays (images) for commands.
PyTango does not support enumerated types (`DevEnum`) for commands.
:::

So far, so good.  Commands were easy, next up: attributes.
