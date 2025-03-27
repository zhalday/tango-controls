# Attributes

Running out of coffee is dangerous!  You need to monitor the level of beans.  And to get the perfect cup, you'll
tweak the brewing temperature and coarseness of the grind.  In Tango, reading and writing a value like
that is done with an {term}`attribute`.

Attributes have a name and a data type.  They can be read-only, read/write or write-only.  Similar to commands, there is a pre-defined list of data types, so arbitrarily complex types are not supported.
:::::{tab-set}

::::{tab-item} Python
```{literalinclude} 06-attributes/python/main.py
:caption: main.py
:language: python
:emphasize-lines: 4
```
::::

::::{tab-item} C++
Sorry, still TODO!
::::

::::{tab-item} Java
Sorry, still TODO!
::::

:::::

In Python, you need to import {py:class}`~tango.server.attribute` and then use that to decorate a method on the {py:class}`~tango.server.Device`, or use it to create objects (non-decorator syntax), and link those to methods. In other languages, it is a little more complicated.

You have the following attributes:
* `waterLevel` a read-only float.  It is a scalar value (in other words, zero-dimensional, or 0-D).
* `beanLevels` is also read-only, but returns a list of up to two floats.  In Tango 1-D arrays are called *spectrum* attributes, and 2-D arrays are *image* attributes.
* `beanLevelsDoc` shows how documentation and the units can be defined.
* `grind` is a read-write, scalar attribute using an enumeration data type.  There is one method handling reading, and one handling writing.  The docstring for the read method is an alternative to the `doc` keyword argument.
* `brewingTemperature` is defined using assignment rather than decorator syntax.  It is a read-write scalar float.  The pattern for naming the methods is critical: `read_` and `write_`, followed by the attribute name.

The attribute names use capitalisation as per the Tango [Naming Rules](#naming-rules).

Run this example, and in a second terminal, use the [device proxy client](01-first-steps.md#first-tango-client) to check if it is working  :

```python-console
>>> dp.waterLevel
54.2
>>> dp.beanLevels
array([ 82.5, 100. ])
>>> dp.grind
<grind.FINE: 0>
>>> dp.grind = "MEDIUM"
>>> dp.grind
<grind.MEDIUM: 1>
>>> dp.brewingTemperature
94.4
>>> dp.brewingTemperature = 95.1
>>> dp.brewingTemperature
95.1
```

Getting the value by reading the attribute name directly on the `DeviceProxy` object is a convenience.  There is actually a lot more information available when an attribute is read.  You can also use the more low-level {py:meth}`~tango.DeviceProxy.read_attribute` and {py:meth}`~tango.DeviceProxy.write_attribute` methods to see the full data structure:

```python-console
>>> reading = dp.read_attribute("waterLevel")
>>> print(reading)
DeviceAttribute[
data_format = tango._tango.AttrDataFormat.SCALAR
      dim_x = 1
      dim_y = 0
 has_failed = False
   is_empty = False
       name = 'waterLevel'
    nb_read = 1
 nb_written = 0
    quality = tango._tango.AttrQuality.ATTR_VALID
r_dimension = AttributeDimension(dim_x = 1, dim_y = 0)
       time = TimeVal(tv_nsec = 0, tv_sec = 1742478185, tv_usec = 208290)
       type = tango._tango.CmdArgType.DevDouble
      value = 54.2
    w_dim_x = 0
    w_dim_y = 0
w_dimension = AttributeDimension(dim_x = 0, dim_y = 0)
    w_value = None]

>>> reading.value
54.2
>>> dp.write_attribute("brewingTemperature", 94.9)
>>> dp.brewingTemperature
94.9
```

As a high-level convenience, you can also get the struct using indexed access in Python:

```python-console
>>> reading = dp["waterLevel"]
>>> print(reading)
DeviceAttribute[
data_format = tango._tango.AttrDataFormat.SCALAR
      dim_x = 1
      dim_y = 0
 has_failed = False
   is_empty = False
       name = 'waterLevel'
    nb_read = 1
 nb_written = 0
    quality = tango._tango.AttrQuality.ATTR_VALID
r_dimension = AttributeDimension(dim_x = 1, dim_y = 0)
       time = TimeVal(tv_nsec = 0, tv_sec = 1742478283, tv_usec = 8934)
       type = tango._tango.CmdArgType.DevDouble
      value = 54.2
    w_dim_x = 0
    w_dim_y = 0
w_dimension = AttributeDimension(dim_x = 0, dim_y = 0)
    w_value = None]
```

Tango is case insensitive when accessing attributes by name, so all of the following calls access the same attribute:

```python-console
>>> dp.brewingTemperature
95.1
>>> dp.BREWINGTemperature
95.1
>>> dp.brewingtemperature
95.1
>>> dp.read_attribute("BreWingTemPeraTure").value
95.1
>>> dp["BreWingTemPeraTure"].value
95.1
```


The documentation for each attribute is available to the client:
```python-console
>>> dp.get_attribute_config("beanLevels").description
'No description'
>>> dp.get_attribute_config("beanLevelsDoc").description
'How full is each bean dispenser'
>>> dp.get_attribute_config("grind").description
'Setting for the coffee bean grinder'
```

The {py:meth}`~tango.DeviceProxy.get_attribute_config` method provides all the details about an attribute:

```python-console
>>> config = dp.get_attribute_config("brewingTemperature")
>>> print(config)
AttributeInfoEx[
            alarms = AttributeAlarmInfo(delta_t = 'Not specified', delta_val = 'Not specified', extensions = [], max_alarm = 'Not specified', max_warning = 'Not specified', min_alarm = 'Not specified', min_warning = 'Not specified')
       data_format = tango._tango.AttrDataFormat.SCALAR
         data_type = tango._tango.CmdArgType.DevDouble
       description = 'No description'
        disp_level = tango._tango.DispLevel.OPERATOR
      display_unit = 'No display unit'
       enum_labels = []
            events = AttributeEventInfo(arch_event = ArchiveEventInfo(archive_abs_change = 'Not specified', archive_period = 'Not specified', archive_rel_change = 'Not specified', extensions = []), ch_event = ChangeEventInfo(abs_change = 'Not specified', extensions = [], rel_change = 'Not specified'), per_event = PeriodicEventInfo(extensions = [], period = '1000'))
        extensions = []
            format = '%6.2f'
             label = 'brewingTemperature'
         max_alarm = 'Not specified'
         max_dim_x = 1
         max_dim_y = 0
         max_value = 'Not specified'
         memorized = tango._tango.AttrMemorizedType.NONE
         min_alarm = 'Not specified'
         min_value = 'Not specified'
              name = 'brewingTemperature'
    root_attr_name = 'Not specified'
     standard_unit = 'No standard unit'
    sys_extensions = []
              unit = ''
          writable = tango._tango.AttrWriteType.READ_WRITE
writable_attr_name = 'brewingTemperature']

```

To simplify the implementation of all clients and servers, the data types available to attributes are limited:
- simple types:  integer, float, string, boolean, enum
- 1-D lists of simple types (spectrum)
- 2-D lists of simple types (image)
- special structures:
  - an encoded byte array, with string indicating the format: `DevEncoded`

:::{tip}
For more examples of using Python type hints for declaring attributes see [device server type hints](inv:pytango:std:label#type-hint).
:::

:::{tip}
For more complicated input and output data structures, it is common to use a string that is serialised and de-serialised using JSON.  This allows structures like dicts to be passed between client and server.  The downside is that the schema of those dicts is not obvious.
:::

:::{tip}
You can easily get a list of all the attributes a Tango device offers:

```python-console
>>> dp.get_attribute_list()
['waterLevel', 'beanLevels', 'beanLevelsDoc', 'grind', 'brewingTemperature', 'State', 'Status']
```

State and Status are special, and show up as commands and attributes.  Normally we access them as commands.

:::


:::{note}
Python limits/simplifies the data types that can be used, compared to C++ and Java.  For PyTango, here is the full list of the [data types](inv:pytango:std:label#pytango-data-types).
:::

You've already learned quite a lot of the basics!  Next up is a way to configure persistent settings.
