(attribute-explanation)=
# Attribute

(attribute)=

```{tags} audience:all, lang:all
```
%[glossary_term][Attribute]
%An attribute represents a process value (or values) in the system. It may have different formats or dimensions like scalar(0D), spectrum(1D) or image(2D). The attribute allows to read and/or write these values depending on programmer-defined access. The values may have different data types. In addition, an attribute provides some metadata like {term}`attribute quality`, timestamp or configuration properties. For a complete list please refer to the manual. A list of attributes available for a certain device is defined by its {term}`device class`.

An Attribute is a Tango concept that can represent a physical quantity of a device or equipment. It can also represent a quantity which is not tied to any equipment but might have been computed in software as there is no enforced tie to hardware for Attributes. Essentially, any value that you want available on the Tango bus is an attribute. For example:

- A device associated with a motor **has** a {samp}`{position}` attribute expressed in mm.
- A device associated with a thermocouple **has** a {samp}`{temperature}` attribute expressed in Celsius (or any another suitable unit).

The main purpose of an Attribute is to replace getters and setters by providing read and (optionally) write access to this quantity. For example: the position of a motor will be obtained by reading the associated attribute (position) and not by running a command like `get_position`. 

In object oriented terminology, an Attribute corresponds to an instance variable (also called a field or a member) of a [Device](#device-explanation) object or simpler an Attribute is one of the parts of a Device.

The data associated with the Tango attributes are the only values that can be archived. The Tango *archiving system* (HDB/TDB) doesn’t have any functions to archive the result of a command. Similarly, some mechanisms to store the experimental data (such as those implemented by the DataRecorder of SOLEIL) are only based on attributes.

Some further example use cases of an Attribute are:

- The wind speed measured by a weather station.
- A correction factor computed by an algorithm that is applied elsewhere.
- A fourier transformation of a 2d-array.
- A random number.

## Attribute Properties
A Tango attribute has a group of settings that describe it.

These configuration parameters are called AttributeProperties. They can be considered as metadata to enhance the semantic and describe the
data. They can be used by GUI clients for configuring their viewers in the best manner and displaying extra information.

Attribute properties describe the attribute data and define some of its behaviour such as alarm limits, units etc…

There are 3 types of *Attribute Properties*:
- Static metadata: They describe the kind of data carried by the Tango Attribute. The static metadata includes properties such as the name, the type, the dimension, if the attribute is writable or not. These data are hardcoded, defined for the whole life of the attribute and cannot be modified.
- Dynamic metadata: They describe more precisely the meaning of the data and some behaviour. They are used by GUI viewers to configure themselves. Most importantly, they can be modified at run time.
- Runtime metadata: They describe the Attribute’s value and its current condition like warnings or alarms and its timestamp.

Attributes can be statically defined in the source code of a {term}`Device` or be created in a dynamic way during the runtime of a Device. When an Attribute is added during the runtime of a Device it is referred to as a Dynamic Attribute.

These metadata are hosted in the class itself and can be set by the programmer or by a configuration in the Tango database. The following section goes into more detail with examples of static and dynamic properties 


### Static attribute properties

The following list contains some of the mandatory static metadata of an Attribute. It provides an insight into what is currently supported.

- `name`: The name identifies the Attribute and is unique for a Device. There cannot be other entities with the same name in a Device. Some restrictions to the allowed characters in a name apply, but alphanumerical characters are supported. For example: OutCurrent, InCurrent…
- `data_type`: The attribute data type identifies the Tango numeric type associated to the attribute: *DevBoolean, DevUChar, Dev\[U\]Short, Dev\[U\]Long, Dev\[U\]Long64, DevFloat, DevDouble, DevString, DevEncoded* (the Tango type that encapsulates client data). Enumerations are supported and explained more in the [Enumerated Attribute](#enumerated-attribute) document. To learn more about the all of available data types, please refer to the [Tango Controls RFCs](#RFC), especially the [RFC for the Tango Data Types](https://tango-controls.readthedocs.io/projects/rfc/en/latest/9/DataTypes.html).
- `writeable`: specifies if the Attribute's quantity can be modified by clients (read-write) or not (read-only). Read-only Attributes are immutable for clients but its quantity can internally be modified by the Device that it is a member of. There are 4 possible types of access but in many cases only 2 really need to be used: 
  - **READ**: The attribute can only be read (e.g. a temperature)
  - WRITE: The attribute can only be written (to be used only in very specific cases. The READ_WRITE is generally more suitable for real cases)
  - **READ_WRITE**: The attribute can be written and read (the most common case) e.g. The current of a power supply, The position of an axis…
  - READ_WITH_WRITE (deprecated, do not use)
- `data_format`: describes the dimension of the data. This can be a scalar (value), spectrum (1D array) or and image (2D array). 

Attributes are allowed to contain more static metadata but not less. Which metadata (static, configuration and runtime) an Attribute can contain is listed in the [full specification of Tango Attributes](https://tango-controls.readthedocs.io/projects/rfc/en/latest/4/Attribute.html) which is part of the [Tango Controls RFCs](#RFC).

Some further useful static metadata are listed below:
- `max_dim_x`: this property is valid only for a spectrum or image `data_format`. It gives the maximum number of element in the X dimension, e.g. the max length of a spectrum or the maximum number of rows of an image. This property is used to reserve memory space to host the data. Nothing prevents having a real length much shorter that this maximum. For example: 0 for a scalar, n for a spectrum of max n elements, n for an image of max n rows.
- `max_dim_y`: this property is valid only for an image `data_format`. It gives the maximum number of element in the Y dimension, e.g. the maximum number of columns of an image. Again, this property is used to reserve memory space to host the data. Nothing prevents having a real length much shorter that this maximum. For example: 0 for a scalar or a spectrum, n for an image of max n columns.
- `display_level`: enables the hiding of the attribute depending on the client mode (expert or not), i.e. `Tango::OPERATOR` or `Tango::EXPERT`.

### Dynamic attribute properties

%[glossary_term][Dynamic Attribute]
%A {term}`device` can create {term}`Attribute`s that have their configuration determined during device initialization or even later when the Device is already running. This kind of Attribute is called *Dynamic Attribute*.

These properties carry information regarding the display of a value and they are editable while the device is running. These properties enhance the meaning of the attribute and should as much as possible be defined by the device server programmer as default values when known. For instance, in the general case, the programmer knows the unit of the data and is able to describe it. Knowing the attribute property at the development stage will allow all generic clients to display the data in the best manner.

Some example of dynamic properties are:

- `description`: describes the attribute, e.g. “The power supply output current”
- `label`: label used on the GUIs, e.g. “Output Current”, “Input Current”
- `unit`: attribute unit to be displayed in the client viewer, e.g. “mA”, “mm”
- `standard_unit`: conversion factor to get an attribute value into S.I (M.K.S.A)\_unit. Be careful as this information is intended to be used ONLY by the client, e.g ATKPanel uses it, but jive->test device does not. This property is given as a string that is interpreted as a floating point value. For example, if the device attribute gives the current in mA we would have to divide by 1000 to obtain it in Amps (S.I. unit) meaning we would set this property to 1E-03
- `display_unit`: used by the GUIs to display the attribute in a unit more appropriate for the user. Again be careful as this information is intended to be used ONLY by the client, e.g ATKPanel uses it, but JiveTest device does not. This property is given as a string that is interpreted as a floating point value. For example, if the device attribute gives a current in A and we want to display it in mA, then we have to multiply by 1000 to obtain it in mA meaning we could set this property to 1000.0.
- `format`: specifies how a numeric attribute value should be presented, e.g. « %6.3f »
- `min_value` and `max_value`: minimum and maximum allowable value. These properties are automatically checked at each execution of a write attribute. If the value requested is not between the min_value and the max_value, an exception will be returned to the client. This property is given as a string  that is interpreted as a floating point value (e.g. 10.1, 1E01, 0.12). Note that these properties are valid only for writable attributes.



### Attributes properties related to Events configuration

These settings are used for tuning the events related to the attribute.

- `Rel_change`: relative change in the value in percent
- `Abs_change`: absolute change in the value in the standard unit.
- `Period`: period between two consecutive events
- `Archive_rel_change`: relative change in the value
- `Archive_abs_change`: absolute change in the value
- `Archive_period`: period between two consecutive events.

### Runtime properties

Below is the output of a PyTango client that reads an attribute from a Device - it demonstrates how the runtime metadata of an Attribute can be used. 

```python
In [7]: attr = "my_rw_attribute"  # The Attribute's name.

In [8]: attr_value = dp.read_attribute(attr)  # Read the attributes value together with the runtime metadata.
In [9]: print(f"{attr_value}")  # Print what we received.
DeviceAttribute[
data_format = tango._tango.AttrDataFormat.SCALAR
      [...]
       name = 'my_rw_attribute'
      [...]
       time = TimeVal(tv_nsec = 0, tv_sec = 1730369596, tv_usec = 629978)
       type = tango._tango.CmdArgType.DevDouble
       value = 5.4321
      [...]
       w_value = 0.0]
```

Some of the mandatory static metadata is part of the runtime metadata as can be seen above: `data_format`, `name`, `type` (data type) are equivalents of what has been described earlier.


%[glossary_term][Attribute quality factor]
%A value returned by an {term}`Attribute` has a runtime quality factor which is an enumeration describing the state of the read value (one of VALID, INVALID, ALARM, CHANGING, WARNING).

%[glossary_term][Attribute quality]
%Another name for {term}`Attribute quality factor`.

## Enumerated Attribute

%[glossary_term][Enumerated Attribute]
%Attributes with a scalar data format can be enumerated allowing a set of defined label+value pairs.

Tango supports enumerated Attributes. They are not implemented on top of the enumeration types of the core Tango languages but they behave like them. In the day-to-day business one will not notice a big difference compared to the language enumerations. There are however a couple of smaller limitations, one being that only Attributes with the scalar data format can be enumerated Attributes. This means that enumerated Attribute arrays are not supported.

See the [how-to](#how-to-enumerated-attribute) section for an example on how to use enumerated attributes.

## Memorized Attribute

%[glossary_term][Memorized Attribute]
%The last written value for this type of attribute will automatically be stored in the database so that on startup this value is fetched and written to the attribute.

Attributes with a scalar data format can be configured to have their last set quantity automatically and permanently be stored in the [Tango Database](#tangodb-explanation). This is done by defining such an attribute in the source code. 

In addition to the storing of the quantity, the stored value will be reloaded into the set value associated with this attribute at device start-up and (optionally) upon each execution of the “Init” command, effectively maintaining the Attribute's quantity over Device restarts. The Tango code generator (Pogo) provides the interface allowing the developer to select the expected behaviour.

:::{note}
Memorized attributes are only possible with an attribute with WRITE or READ_WRITE mode and
SCALAR type
:::

Clients are unable to tell if an Attribute is memorized or not. 

See the [how-to](#how-to-memorized-attribute) section for an example on how to use a memorized attribute.

## Forwarded Attribute

%[glossary_term][Forwarded Attribute]
%A forwarded attribute is one that gets its configuration from another attribute, which is known as the *root attribute*. It will forward requests, configuration changes, event subscriptions and locking behaviour to the root attribute.

:::{warning}
Forwarded attribute is a feature that is not entirely mature. Its use is not recommended.
:::

Tango supports the forwarding of Attributes of scalar data format. A forwarded attribute will let you access an attribute from another device, this will be called the **root attribute** as an attribute of this device.
A forwarded attribute will retrieve all its metadata and information from the **root attribute**. All call to read, write, configuration or property settings, except for the **label** property, are forwarded to the **root attribute** and will modify its state.
A typical use case is when a single hardware connection let you handle several devices.
It is then common to implement a Tango class, lets call it **Interface** to handle the hardware connection. The **Interface** class will expose the attributes for each devices.
We can then use another class, let's call it **device**, that will logically represents each devices. The device class could use forwarded attributes to match its attributes to the one defined in the **Interface** class.

See the [how-to](#how-to-forwarded-attribute) section for an example on how to use a forwarded attribute.
