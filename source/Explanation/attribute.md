(attribute-explanation)=
# Attribute

(attribute)=

{audience}`all`, {lang}`all`

An Attribute is a Tango concept that can represent a physical quantity of a device or equipment. It can also represent a quantity which is not tied to any equipment but might have been computed in software as there is no enforced tie to hardware for Attributes. The main purpose of an Attribute is to provide read and (optionally) write access to this quantity. In object oriented terminology, an Attribute corresponds to an instance variable (also called a field or a member) of a [Device](#device-explanation) object or simpler an Attribute is one of the parts of a Device.

Some example use cases of an Attribute are:

- The wind speed measured by a weather station.
- The position of a motor.
- The temperature reading of some equipment.
- A correction factor computed by an algorithm that is applied elsewhere.
- A fourier transformation of a 2d-array.
- A random number.

## Attribute metadata
Tango Attributes are self-describing entities that come in various forms and shapes. They are defined by three sets of metadata which are always part of the Attributes:

- Static metadata that defines the Attribute like its name, data type (e.g. integer, float, string) and data format (e.g. scalar, array).
- Dynamic metadata that defines the Attribute's behaviour. For example minimum and maximum warning or alarm thresholds for the Attribute's value define when an Attribute might indicate a wraning or alarm condition in its runtime metadata.
- Runtime metadata describing the Attribute’s value and its current condition like warning or alarm and its timestamp.

:::hint
It is perfectly fine to skip the next section about the static metadata if you are not a developer. :ok_hand:
:::

### A quick excursion into an Attribute's static metadata

 The following list contains some of the mandatory static metadata of an Attribute. It provides an insight into what is currently supported.

- Its name: The name identifies the Attribute and is unique for a Device. There cannot be other entities with the same name in a Device. Some restrictions to the allowed characters in a name apply, but alphanumerical characters are supported.
-The data type: Many interger data types are supported, strings, booleans and floating point types are supported as well. Enumerations are supported and explained more in the [Enumerated Attribute](#enumerated-attribute) document. To learn more about the all of available data types, please refer to the [Tango Controls RFCs](#RFC), especially the [RFC for the Tango Data Types](https://tango-controls.readthedocs.io/projects/rfc/en/latest/9/DataTypes.html).
- Write access: Specifies if the Attribute's quantity can be modified by clients (read-write) or not (read-only). Read-only Attributes are immutable for clients but its quantity can internally be modified by the Device that it is a member of.
- Its data format: The dimensionality of the Attribute. Currently scalar, one and two dimensional arrays are supported.

Attributes are allowed to contain more static metadata but not less. Which metadata (static, configuration and runtime) an Attribute can contain is listed in the [full specificatin of Tango Attributes](https://tango-controls.readthedocs.io/projects/rfc/en/latest/4/Attribute.html) which is part of the [Tango Controls RFCs](#RFC).

### Runtime metadata and why one might want to look at it

As an example for how the runtime metadata of an Attribute looks like, below is the output for a PyTango client that reads an attribute from a Device:

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

## Enumerated Attribute
Tango supports enumerated Attributes. They are not implemented on top of the enumeration types of the core Tango languages but they behave like them. In the day-to-day business one will not notice a big difference compared to the language enumerations. A couple of smaller limitations exist though, one being that only Attributes with the scalara data format can be Enumerated Attributes. Meaning: Enumerated Attribute arrays are not supported.

## Memorised Attribute

Tango supports that Attributes of scalar data format have their last set quantity automatically and permanently be stored in the [Tango Database](#tangodb-explanation). This is indicated when the Attribute is defined in the source code. Clients are unable to tell if an Attribute is memorised or not. In addition to the storing of the quantity, the last stored value can also be applied to the memorised Attribute when its Device starts, effectively maintaining the Attribute's quantity over Device restarts.

## Forwarded Attribute

:::{warning}
Forwarded attribute is a feature that is not entirely mature. Its use is not recommended.
:::

Tango supports the forwarding of Attributes of scalar data format. A forwarded attribute will let you access an attribute from another device, this will be called the **root attribute** as an attribute of this device.
A forwarded attribute will retrieve all its metadata and information from the **root attribute**. All call to read, write, configuration or property settings, except for the **label** property, are forwarded to the **root attribute** and will modify its state.
A typical use case is when a single hardware connection let you handle several devices.
It is then common to implement a Tango class, lets call it **Interface** to handle the hardware connection. The **Interface** class will expose the attributes for each devices.
We can then use another class, let's call it **device**, that will logically represents each devices. The device class could use forwarded attributes to match its attributes to the one defined in the **Interface** class.
