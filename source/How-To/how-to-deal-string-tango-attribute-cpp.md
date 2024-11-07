(how-to-deal-with-strings)=

# How to deal with Tango string attributes in C++

```{tags} audience:developers, lang:c++
```

The underlying technology for network operations is {term}`CORBA`. As this was standardized before C++,
it still uses plain char pointers instead of the std string class.

This means that you have to deal with

1. The pointer to the memory where the string is stored (`char *`)
2. The memory where the the string characters are stored

This adds one level of complexity and you have to take care about memory
allocation for these entities when you have string attributes (scalar, spectrum or image).

The first question you have to answer is: Do I want static or dynamic
memory allocation for my string attribute?

Static memory allocation means that the memory is allocated once.
Dynamic allocation means that the memory used for the attribute is
allocated and freed each time the attribute is read. Once one method is
chosen, both the pointer and the characters array memory has to follow
the same rule (all static or all dynamic, but not a mix of them)

(scalar-string-attr-static)=

## Scalar attributes - static allocation

Within {term}`Pogo`, for a correct management of this type of attribute, do not
click the "allocate" toggle button when you define the attribute. The
pointer to the character area is defined as one of the device data
members in the file `MyDev.h`. The Tango data type DevString is simply an alias
for a good old `char *` pointer.

```{code-block} cpp
:linenos: true

class MyDev : public TANGO_BASE_CLASS
{

    /*----- PROTECTED REGION ID(MyDev::Data Members) ENABLED START -----*/

    // Add your own data members
public:
    Tango::DevString the_str;
    /*----- PROTECTED REGION END -----*/ // MyDev::Data Members
}
```

In the `init_device` method (file MyDev.cpp), you have to initialize the
attribute data member created for you by Pogo

```{code-block} cpp
:linenos: true

void MyDev::init_device()
{
    DEBUG_STREAM << "MyDev::init_device() create device " << device_name << std::endl;

    /*----- PROTECTED REGION ID(StringAttr::init_device) ENABLED START -----*/

    attr_StringAttr_read = &the_str;

    /*----- PROTECTED REGION END -----*/    // MyDev::init_device
}
```

The attribute related code in the file MyDev.cpp looks like

```{code-block} cpp
:linenos: true

void MyDev::read_StringAttr(Tango::Attribute &attr)
{
    DEBUG_STREAM << "MyDev::read_StringAttr(Tango::Attribute &attr) entering... " << std::endl;

    /*----- PROTECTED REGION ID(MyDev::read_StringAttr) ENABLED START -----*/

    // Set the attribute value
    the_str = const_cast<char *>("Hola Barcelona");
    attr.set_value(attr_StringAttr_read);

    /*----- PROTECTED REGION END -----*/    // MyDev::read_StringAttr
}
```

The pointer `the_str` is defined as a device data member and is initialized to a statically allocated string. The
argument of the `Attribute::set_value` method is of type `char **` which is coherent with the definition of
the Tango::DevString type. Nevertheless, the definition of statically allocated string in C++ is a `const char *`.
This is why we need a `const_cast` during the pointer initialization.

Note that the use of the Pogo generated data member (named `attr_StringAttr_read` here) is not mandatory.
You can directly give the address of the `the_str` pointer to `the Attribute::set_value` method and do not
need any additional code in the `init_device` method.

(scalar-string-attr-dynamic)=

## Scalar attributes - dynamic allocation

### Memory freeing done by Tango layer

Within {term}`Pogo`, for a correct management of this type of attribute, do not
click the "allocate" toggle button when you define the attribute. In
this case, we do not need to define anything as device data member.

The attribute related code in the file `MyDev.cpp` looks like

```{code-block} cpp
:linenos: true

void MyDev::read_StringAttr(Tango::Attribute &attr)
{
    DEBUG_STREAM << "MyDev::read_StringAttr(Tango::Attribute &attr) entering... " << std::endl;

    /*----- PROTECTED REGION ID(MyDev::read_StringAttr) ENABLED START -----*/

    // Set the attribute value
    attr_StringAttr_read = new Tango::DevString;
    *attr_StringAttr_read = Tango::string_dup("Bonjour Paris");
    attr.set_value(attr_StringAttr_read, 1, 0, true);

    /*----- PROTECTED REGION END -----*/    // MyDev::read_StringAttr
}
```

As explained in the introduction, both the pointer and the char array memory are dynamically allocated. The
pointer is allocated first, then it is initialized with the result of a `Tango::string_dup` method which
allocates memory and copies the string given as argument. The Tango attribute value is set with the classical
`set_value` method but requiring Tango to free all the memory previously allocated.

### Memory freeing done by device class

This example is in the case where within {term}`Pogo`, the "allocate" toggle
button was active when the attribute was defined.

The `init_device` and `delete_device` method looks like:

```{code-block} cpp
:linenos: true

void MyDev::init_device()
{
    DEBUG_STREAM << "MyDev::init_device() create device " << device_name << std::endl;

    attr_StringAttr_read = new Tango::DevString[1];

    /*----- PROTECTED REGION ID(StringAttr::init_device) ENABLED START -----*/

    *attr_StringAttr_read = nullptr;

    /*----- PROTECTED REGION END -----*/    // MyDev::init_device
}

void MyDev::delete_device()
{
    /*----- PROTECTED REGION ID(MyDev::delete_device) ENABLED START -----*/

    Tango::string_free(*attr_StringAttr_read);

    /*----- PROTECTED REGION END -----*/    // MyDev::delete_device
    delete[] attr_StringAttr_read;

}
```

The pointer for the characters array is allocated in the `init_device` method
and initialized to null pointer. In the `delete_device` method, the character
array memory is freed with the `Tango::string_free` method.

```{code-block} cpp
:linenos: true

void MyDev::read_StringAttr(Tango::Attribute &attr)
{
    DEBUG_STREAM << "MyDev::read_StringAttr(Tango::Attribute &attr) entering... " << std::endl;

    /*----- PROTECTED REGION ID(MyDev::read_StringAttr) ENABLED START -----*/

    // Set the attribute value
    Tango::string_free(*attr_StringAttr_read);
    *attr_StringAttr_read = Tango::string_dup("Bonjour Paris");
    attr.set_value(attr_StringAttr_read);

    /*----- PROTECTED REGION END -----*/    // MyDev::read_StringAttr
}
```

The Tango::DevString pointer created by {term}`Pogo` (named `attr_StringAttr_read`) is allocated in the
`init_device` method (Pogo generated code) and freed in the `delete_device` method (Pogo generated code).
Nevertheless, nothing is done for the memory used to store the characters array on attribute reading. Freeing
of an existing attribute is done in this code snippet in the first line of the protected region. Then the
memory is allocated for the new characters array and used to set to the Tango Attribute instance value.

Note that only the memory allocated for the character array is allocated/freed at each attribute reading. The
pointer is allocated once in the `init_device` method and freed in the `delete_device` method.

## Spectrum / Image attributes - static allocation

The code needed in this case is very similar to the [scalar case](#scalar-string-attr-dynamic). We also
need pointers to the character arrays. They are defined as device data members in the file `MyDev.h`.

```{code-block} cpp
:linenos: true

{
constexpr long str_arr_size = 2;

} // anonymous namespace

class MyDev : public TANGO_BASE_CLASS
{
   /*----- PROTECTED REGION ID(MyDev::Data Members) ENABLED START -----*/

  // Add your own data members
public:
   Tango::DevString  the_str_array[str_arr_size];

   /*----- PROTECTED REGION END -----*/ // MyDev::Data Members
}
```

In the `init_device` method (file `MyDev.cpp`), you have to initialize the
attribute data members created for you by {term}`Pogo`.

```{code-block} cpp
:linenos: true

void MyDev::init_device()
{
    DEBUG_STREAM << "MyDev::init_device() create device " << device_name << std::endl;

    /*----- PROTECTED REGION ID(StringAttr::init_device) ENABLED START -----*/

    attr_StringAttr_read = the_str_array;

    /*----- PROTECTED REGION END -----*/    // MyDev::init_device
}
```

The attribute related code in the file `MyDev.cpp` looks like

```{code-block} cpp
:linenos: true

void MyDev::read_StringAttr(Tango::Attribute &attr)
{
    DEBUG_STREAM << "MyDev::read_StringAttr(Tango::Attribute &attr) entering... " << std::endl;

    /*----- PROTECTED REGION ID(MyDev::read_StringAttr) ENABLED START -----*/

    // Set the attribute value
    the_str_array[0] = const_cast<char *>("Hola Barcelona");
    the_str_array[1] = const_cast<char *>("Ciao Trieste");
    attr.set_value(attr_StringAttr_read, str_arr_size);

    /*----- PROTECTED REGION END -----*/    // MyDev::read_StringAttr
}
```

The array `the_str_array` defined as a device data member is initialized to statically allocated strings. The
argument of the `Attribute::set_value` method is of type `char **` which is coherent with the definition of
the Tango::DevString type. Nevertheless, the definition of statically allocated string in C++ is a `const char *`.
This is why we need a `const_cast` during the pointer initialization.

Note that the use of the {term}`Pogo` generated data member (named `attr_StringAttr_read` in our case) is not
mandatory. You can directly give the name of the `the_str_array` data member to the `Attribute::set_value`
method and do not need any additional code in the `init_device` method.

Something similar can be done using a vector of C++ strings if:

1. The vector is initialized somewhere in your Tango class
2. The vector is declared as a device data member (in MyDev.h)
3. The vector size is less or equal to the attribute maximum dimension

The code looks like

```{code-block} cpp
:linenos: true

void MyDev::read_StringAttr(Tango::Attribute &attr)
{
    DEBUG_STREAM << "MyDev::read_StringAttr(Tango::Attribute &attr) entering... " << std::endl;

    /*----- PROTECTED REGION ID(MyDev::read_StringAttr) ENABLED START -----*/

    // Set the attribute value
    for (size_t i = 0;i < str_arr_size;i++)
    {
       the_str_array[i] = vs[i].data();
    }

    attr.set_value(attr_StringAttr_read, vs.size());

    /*----- PROTECTED REGION END -----*/    // MyDev::read_StringAttr
}
```

## Spectrum / Image attribute - dynamic allocation

### Memory freeing done by Tango layer

Within {term}`Pogo`, for a correct management of this type of attribute, do not
click the "allocate" toggle button when you define the attribute. In
this case, we do not need to define anything as device data member.

The attribute related code in the file `MyDev.cpp` looks like

```{code-block} cpp
:linenos: true

{
constexpr long str_arr_size = 2;

} // anonymous namespace

void MyDev::read_StringAttr(Tango::Attribute &attr)
{
    DEBUG_STREAM << "MyDev::read_StringAttr(Tango::Attribute &attr) entering... " << std::endl;

    /*----- PROTECTED REGION ID(MyDev::read_StringAttr) ENABLED START -----*/

    // Set the attribute value
    Tango::DevString *ptr_array = new Tango::DevString[str_arr_size]
    ptr_array[0] = Tango::string_dup("Bonjour Paris");
    ptr_array[1] = Tango::string_dup("Salut Grenoble");
    attr.set_value(ptr_array, str_arr_size, 0, true);

    /*----- PROTECTED REGION END -----*/    // MyDev::read_StringAttr
}
```

The Tango::DevString pointer array is allocated first, then it is initialized with the results of a
`Tango::string_dup` method which allocates memory and copies the string given as argument. The Tango attribute
value is set with the classical `set_value` method but requiring Tango to free all the memory previously
allocated.

## Conclusion

:::{note}
Do not mix the two solutions. Use either dynamic or static allocation and also ensure that you are using it for both levels (pointers and character arrays)
:::
