(use-vector-set-attributes)=

# How to use vectors to set attributes

```{tags} audience:developers, lang:c++
```

This page contains examples on how to use the C++ vector class to set and get attribute
values on the servers side.

:::{warning}
Tango is optimized not to copy data. For this reason all the attribute
set_value() methods only take pointers as input. If you are going to
use C++ vectors, you should be aware of the fact that you are going to
copy the data! This might slow down execution time when working with
large amount of data.
:::

The `std::vector` class takes care of the memory of its entries, so it is mandatory to leave the optional
`release` parameter of `Attribute::set_value` to the default of `false`.

Examples for a read attribute and vector of shorts and strings:

```{code-block} cpp
:linenos: true

void MyClass::read_spectrum(Tango::Attribute &attr)
{
  DEBUG_STREAM << "MyClass::read_Spectrum(Tango::Attribute &attr) entering... "<< std::endl;
  /*----- PROTECTED REGION ID(MyClass::read_Spectrum) ENABLED START -----*/

  std::vector<Tango::DevShort> val;
  vec.emplace_back(1);
  vec.emplace_back(2);
  vec.emplace_back(3);

  attr.set_value(val.data(), val.size());

  /*----- PROTECTED REGION END -----*/ // MyClass::read_Spectrum
}
```

```{code-block} cpp
:linenos: true

void MyClass::read_string_spectrum(Tango::Attribute &attr)
{
  DEBUG_STREAM << "MyClass::read_StringSpectrum(Tango::Attribute &attr) entering... "<< std::endl;
  /*----- PROTECTED REGION ID(MyClass::read_StringSpectrum) ENABLED START -----*/

  std::vector<std::string> vec;
  vec.emplace_back("Hello");
  vec.emplace_back("foggy");
  vec.emplace_back("garden!");

  attr.set_value(vec.data(), vec.size());

  /*----- PROTECTED REGION END -----*/ // MyClass::read_StringSpectrum
}
```

For a writeable attribute the code looks similiar:


```{code-block} cpp
:linenos: true
void MyClass::write_double_spectrum(Tango::WAttribute &attr)
{
  DEBUG_STREAM << "MyClass::write_double_spectrum(Tango::WAttribute &attr) entering... " << std::endl;
  // Retrieve number of write values
  int w_length = attr.get_write_value_length();

  // Retrieve pointer on write values (Do not delete !)
  const Tango::DevDouble  *w_val;
  attr.get_write_value(w_val);
  /*----- PROTECTED REGION ID(MyClass::write_double_spectrum) ENABLED START -----*/

  // not strictly needed, but makes the code easier to grasp
  if(w_length == 0)
  {
    return;
  }

  std::vector<double> vec;
  vec.assign(w_val, w_val + w_length);

  /*----- PROTECTED REGION END -----*/ // MyClass::write_double_spectrum
}
```
