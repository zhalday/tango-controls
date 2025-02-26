(how-to-memorized-attribute)=
# How to use a Memorized Attribute

```{tags} audience:developers, lang:c++
```

It is possible to ask Tango to store the last written value for
attribute of the SCALAR data format, which are READ_WRITE or READ_WITH_WRITE,
in the database. This is fully automatic. During device startup phase all
device memorized attributes with a value written in the database will
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
`false` to define that only the set point should be initialsied.
