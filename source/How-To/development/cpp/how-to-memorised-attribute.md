(how-to-memorized-attribute)=
# How to use a memorized attribute

```{tags} audience:developers, lang:c++
```

It is possible to ask Tango to store the last written value for
attribute of the SCALAR data format, which are READ_WRITE or READ_WITH_WRITE,
in the database. This is fully automatic. During device startup phase all
device {term}`memorized attributes <memorized Attribute>` with a value written in the database will
have their value fetched and applied. A write_attribute
call can be generated to apply the memorized value to the attribute or
only the attribute set point can be initialised. The following piece of
code shows how to set an attribute as memorized and how to initialise
only the attribute set point.

```{code} cpp
:number-lines: 1

 void DevTestClass::attribute_factory(vector<Tango::Attr *> &att_list)
  {
      ...
      att_list.push_back(new String_attrAttr());
      att_list.back()->set_memorized();
      att_list.back()->set_memorized_init(false);
      ...
  }
```

Line 4 : The attribute to be memorized is created and inserted in the
attribute vector.

Line 5 : The `set_memorized()` method of the attribute base class is
called to define the attribute as memorized.

Line 6 : The `set_memorized_init()` method is called with the parameter
`false` to define that only the set point should be initialised.

:::{note}
Memorized attributes have the following behaviour to consider:
- The writing of the memorized attributes is carried out after the
function `init_device`, executed by the Tango layer, and not by the
Tango DeviceServer code. In case an error occurs during the
`init_device` it cannot be caught by the Tango DeviceServer programmer.
- If in the `init_device` method an error occurs that causes a change of
state in which the writing of an attribute is impossible, this error
will prohibit the restoration of the memorized value of the attribute.
- The order of reloading is deterministic but complex (*order of
ClassFactory then device definition in database then attribute
definition in Pogo*). Therefore relying on this order might have some
side effects particularly in case attributes are modified through
Pogo when attributes values are linked (*e.g. sampling frequency and
number of samples*).
- There could be performance issues in the case that the setpoint is
written at a high frequency as the static Tango database is queried
on each write of the memorized attribute. Since Tango 9 the database has been optimised
for memorized attributes and it should be possible to update memorized
attributes at 10 Hz without taking a performance hit.
:::

:::{tip}
If this standard Tango behaviour for reloading memorized values doesn’t
fit your needs then we recommend coding the reloading of attribute values
yourself. This is especially true for fast (> 10 Hz)
feedback loops, which can trigger the writing of attributes at a high frequency.
:::
