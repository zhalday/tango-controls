```{raw} latex
\clearpage
```

(first-cpp-device-class-implementation)=

# Write your first C++ TANGO device class

```{tags} audience:developers, lang:c++
```

The example code given in this chapter has been generated using the
Tango code generator [Pogo]`pogo-documentation`. The
following examples briefly describe how to write a device class with
commands that receive and return different kinds of Tango data types.
It also covers how to write device attributes.

This example device class implements 5 commands and 3 attributes. The commands are:

- The command `DevSimple`: handles the simple Tango data type
- The command `DevString`: handles Tango strings
- `DevArray`: receives and returns an array containing the simple Tango data type
- `DevStrArray`: does not receive any data but which returns an
  array of strings
- `DevStruct`: does not receive data but which returns one
  of the two Tango composed data types (`DevVarDoubleStringArray`)

For all of these commands, the default (*always allowed*)behavior of
the state machine is used.

The attributes are :

- A spectrum type attribute of the Tango string type called `StrAttr`
- A readable attribute of the `Tango::DevLong` type called
  `LongRdAttr`. This attribute is linked with the following writable
  attribute
- A writable attribute also of the `Tango::DevLong` type called
  `LongWrAttr`.


## The commands and attributes code

For each command called DevXxxx, Pogo generates a method named `dev_xxx`
in the device class which will be executed when the command is
requested by a client. In this chapter, the name of the device class is
`DocDs`.

### The `DevSimple` command

This method receives and returns a `Tango::DevFloat` data type which is simply
a double representation of the input value. The code for the method executed
by this command is the following:

```{code} cpp
:number-lines: 1

  Tango::DevFloat DocDs::dev_simple(Tango::DevFloat argin)
  {
          Tango::DevFloat argout ;
          DEBUG_STREAM << "DocDs::dev_simple(): entering... !" << endl;

          //      Add your own code to control device here

          argout = argin * 2;
          return argout;
  }
```

This method is fairly simple. The received data is passed to the method
as an argument and it is doubled at line 8 before being returning the result.

### The `DevArray` command

This method receives and returns a `Tango::DevVarLongArray` data type. Each
element of the array is doubled. The code for the method executed by this command is the
following:

```{code} cpp
:number-lines: 1

  Tango::DevVarLongArray *DocDs::dev_array(const Tango::DevVarLongArray *argin)
  {
          //      POGO has generated a method core with argout allocation.
          //      If you would like to use a static reference without copying,
          //      See "TANGO Device Server Programmer's Manual"
          //              (chapter x.x)
          //------------------------------------------------------------
          Tango::DevVarLongArray  *argout  = new Tango::DevVarLongArray();

          DEBUG_STREAM << "DocDs::dev_array(): entering... !" << endl;

          //      Add your own code to control device here

          long argin_length = argin->length();
          argout->length(argin_length);
          for (int i = 0;i < argin_length;i++)
                  (*argout)[i] = (*argin)[i] * 2;

          return argout;
  }
```

The `argout` array is created at line 8. Its length is set at line 15
from the input argument length. The array is populated at line 16 & 17 and
then returned. This method allocates memory for the `argout` array, which
is freed by the Tango core classes after the data have been sent to the
caller, therefore the array does not need to be explictly deleted in the method.
It is also possible to return data from a
statically allocated array without copying.

### The `DevString` command

This method receives and returns a `Tango::DevString` data type. The command
simply displays the content of the input string and returns a hard-coded string. The
code for the method executed by this command is the following:

```{code} cpp
:number-lines: 1

  Tango::DevString DocDs::dev_string(Tango::DevString argin)
  {
          //      POGO has generated a method core with argout allocation.
          //      If you would like to use a static reference without copying,
          //      See "TANGO Device Server Programmer's Manual"
          //              (chapter x.x)
          //------------------------------------------------------------
          Tango::DevString        argout;
          DEBUG_STREAM << "DocDs::dev_string(): entering... !" << endl;

          //      Add your own code to control device here

          cout << "the received string is " << argin << endl;

          string str("Am I a good Tango dancer ?");
          argout = new char[str.size() + 1];
          strcpy(argout, str.c_str());

          return argout;
  }
```

The `argout` string is created at line 8. Internally, this method is using
a standard C++ string. Memory for the returned data is allocated at line
16 and is initialized at line 17. Again, this memory is freed by the Tango core
classes after the data have been sent to the caller and therefore
does not need to be explictly deleted in the method. It is also
possible to return data from a statically allocated string without
copying.

### The `DevStrArray` command

This method does not receive any input data but returns an array of strings
(the `Tango::DevVarStringArray` data type). The code for the method executed by
this command is the following:

```{code} cpp
:number-lines: 1

  Tango::DevVarStringArray *DocDs::dev_str_array()
  {
          //      POGO has generated a method core with argout allocation.
          //      If you would like to use a static reference without copying,
          //      See "TANGO Device Server Programmer's Manual"
          //              (chapter x.x)
          //------------------------------------------------------------
          Tango::DevVarStringArray        *argout  = new Tango::DevVarStringArray();

          DEBUG_STREAM << "DocDs::dev_str_array(): entering... !" << endl;

          //      Add your own code to control device here

          argout->length(3);
          (*argout)[0] = Tango::string_dup("Rumba");
          (*argout)[1] = Tango::string_dup("Waltz");
          string str("Jerck");
          (*argout)[2] = Tango::string_dup(str.c_str());
          return argout;
  }
```

The `argout` data array is created at line 8. Its length is set at line
14\. The array is populated at line 15, 16 and 18. The last array element
is initialized from a standard C++ string created at line 17. Note the
usage of the `string_dup` function within the Tango namespace. This is
necessary for string arrays due to the CORBA memory allocation schema.

### The `DevStruct` command

This method does not receive input data but returns a structure of the
`Tango::DevVarDoubleStringArray` data type. This type is a composed type with
an array of doubles and an array of strings. The code for the method
executed by this command is the following:

```{code} cpp
:number-lines: 1

  Tango::DevVarDoubleStringArray *DocDs::dev_struct()
  {
          //      POGO has generated a method core with argout allocation.
          //      If you would like to use a static reference without copying,
          //      See "TANGO Device Server Programmer's Manual"
          //              (chapter x.x)
          //------------------------------------------------------------
          Tango::DevVarDoubleStringArray  *argout  = new Tango::DevVarDoubleStringArray();

          DEBUG_STREAM << "DocDs::dev_struct(): entering... !" << endl;

          //      Add your own code to control device here

          argout->dvalue.length(3);
          argout->dvalue[0] = 0.0;
          argout->dvalue[1] = 11.11;
          argout->dvalue[2] = 22.22;

          argout->svalue.length(2);
          argout->svalue[0] = Tango::string_dup("Be Bop");
          string str("Smurf");
          argout->svalue[1] = Tango::string_dup(str.c_str());

          return argout;
  }
```

The `argout` data structure is created at line 8. The length of the double
array in the output structure is set at line 14. The array is populated
between lines 15 and 17. The length of the string array in the output
structure is set at line 19. This string array is populated between
lines 20 an 22 from a hard-coded string and from a standard C++ string.
This method allocates memory for the `argout` data, which is freed by the
Tango core classes after the data have been sent to the caller, therefore
the array does not need to be explictly deleted in the method. Again, note
the usage of the `string_dup` function of the Tango namespace. This is
necessary for strings array due to the CORBA memory allocation schema.

### The three attributes

Some variables have been added to the definition of the device class in order
to store attribute values. These are a part of the class definition
\:

```{code} cpp
:number-lines: 1

 protected :
         //      Add your own data members here
         //-----------------------------------------
         Tango::DevString        attr_str_array[5];
         Tango::DevLong          attr_rd;
         Tango::DevLong          attr_wr;
```

One variable has been created for each attribute. As the `StrAttr` attribute
is of type spectrum with a maximum *X* dimension of 5, an array of length
5 has been reserved.

Several methods are necessary for these attributes:
  - One method to read from the hardware, which is common to all readable attributes
  (e.g. `read_attr_hardware` in the example below)
  - One read method for each readable attribute (e.g. `read_LongRdAttr`, etc in the example below) and
  - One write method for each writable attribute (e.g. `write_LongWrAttr`, etc in the example below)

The code for these methods is the following:

```{code} cpp
:number-lines: 1

 void DocDs::read_attr_hardware(vector<long> &attr_list)
 {
     DEBUG_STREAM << "DocDs::read_attr_hardware(vector<long> &attr_list) entering... "<< endl;
     // Add your own code here

     string att_name;
     for (long i = 0;i < attr_list.size();i++)
     {
         att_name = dev_attr->get_attr_by_ind(attr_list[i]).get_name();

        if (att_name == "LongRdAttr")
        {
            attr_rd = 5;
        }
    }
 }

 void DocDs::read_LongRdAttr(Tango::Attribute &attr)
 {
     DEBUG_STREAM << "DocDs::read_LongRdAttr(Tango::Attribute &attr) entering... "<< endl;

     attr.set_value(&attr_rd);
 }

 void DocDs::read_LongWrAttr(Tango::Attribute &attr)
 {
     DEBUG_STREAM << "DocDs::read_LongWrAttr(Tango::Attribute &attr) entering... "<< endl;

     attr.set_value(&attr_wr);
 }

 void DocDs::write_LongWrAttr(Tango::WAttribute &attr)
 {
     DEBUG_STREAM << "DocDs::write_LongWrAttr(Tango::WAttribute &attr) entering... "<< endl;

     attr.get_write_value(attr_wr);
     DEBUG_STREAM << "Value to be written = " << attr_wr << endl;
 }

 void DocDs::read_StrAttr(Tango::Attribute &attr)
 {
     DEBUG_STREAM << "DocDs::read_StrAttr(Tango::Attribute &attr) entering... "<< endl;

     attr_str_array[0] = const_cast<char *>("Rock");
     attr_str_array[1] = const_cast<char *>("Samba");

     attr_set_value(attr_str_array, 2);
 }
```

The `read_attr_hardware()` method is executed once when a client
executes the `read_attributes` CORBA request whatever the number of
attribute to be read is. The rule of this method is to read values from the hardware
and to store the read values somewhere in the device object. In our
example, only the LongRdAttr attribute internal value is set by this
method at line 13.

The method `read_LongRdAttr()` is executed by the
`read_attributes` CORBA call when the `LongRdAttr` attribute is read but
after the `read_attr_hardware()` method has been executed. Its rule is
to set the attribute value in the TANGO core classes object representing
that attribute. This is done at line 22.

The method `read_LongWrAttr()`
will be executed when the `LongWrAttr` attribute is read (again, after the
`read_attr_hardware()` method). The attribute value is set at line 29.
In the same manner, the method called `read_StrAttr()` will be executed
when the attribute `StrAttr` is read. Its value is initialized in this
method at line 44 and 45. There
are several ways to code spectrum or image attribute of the `DevString`
data type.

The `write_LongWrAttr()` method is executed
when the `LongWrAttr` attribute value is set by a client. The new
attribute value coming from the client is stored in the data object at
line 36.

Pogo also generates a file called DocDsStateMachine.cpp (for a Tango
device server class called *DocDs*). This file is used to store methods
for the device state machine. By default an *always allowed* state
machine is provided. For more information about coding the state
machine, refer to the chapter on [state machine management](#state-machine-management).
