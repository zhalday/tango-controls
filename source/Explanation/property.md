(properties)=

# Property

%[glossary_term][property]
%A configuration parameter stored in the {term}`Tango Database`. Properties can be assigned to a {term}`device class`, {term}`device` or elements of device interface ({term}`attributes <attribute>`, {term}`commands <command>`, {term}`pipes <pipe>`). Properties can be also not related to {term}`device` - such properties are called `free properties`. Property values are often used by elements of {term}`Tango Controls` system during its startup. These usually provides information required to configure things like connections to hardware or to adjust to user preferences.

The property concept in Tango Control System is fundamental to its approach in managing and controlling devices. In Tango, each device has properties, which are configurations that define the characteristics and the unique behavior of each device, for example, an axis controller must be configured for the motor mechanics according to the characteristics of the actuator and the movements to achieve.

The properties are used to configure a device without changing the Tango class code. They managed in the Tango database, which stores and provides persistent access to property values. The properties can be retrieved, updated and reconfiguration of devices as needed.


## Property format
In the Tango Control System, properties are represented as key-value pairs, where the key is the property name, and the value is the property's setting or configuration. Property values can come in several different data formats depending on the complexity and requirements of the device or class. Here’s a breakdown of common formats:

- String: Properties can be simple strings i.e: "ip" = "192.168.0.21"
- Integer: Integer values are used for properties that define discrete numerical settings i.e: "max_speed" = 1000
- Double: properties that require decimal precision i.e: "threshold" = 0.05
- Boolean: property that is either True or False i.e: "enabled" = True
- Array: Properties can also be arrays of values, typically for configurations requiring multiple entries i.e: "calibration" = [0.0, 23.2, 55.4, 76.2, 100.0]



## Property Levels
Configuration properties are available on different levels:
- **Device** properties: These are properties to configure the device itself and its attributes. They are specific to individual devices. The device properties configure the device with the necessary set-up information during initialisation. Examples include network addresses, calibration parameters, or limits unique to a device.
- **Class** properties: Class properties apply to all instances of a particular class.
They help in defining default configurations shared across devices of the same type, offering consistency and reducing the need for repetitive configuration.
For example, all motors of a specific model might share a class property defining maximum speed.

   Note that a property defined on the class level will be overwritten by a property of the same name on the device level.
- **Attribute** properties: Attributes properties define the configuration of the device [attributes](#attribute-explanation). These include properties such as data type, display range, alarm limits, and units, ensuring attributes have both meaning and safety constraints. For example, a temperature sensor’s attribute might have properties defining the minimum and maximum allowable values, units in Celsius, and alarm thresholds.
- **Free** properties: Free properties are defined and used for the entire control system. These are configuration values which are not attached to any device or class and can be freely used by programmers. For example, the event system can be configured to send message via a [multicast](#configuring-events-to-use-multicast-transport).

Class level, device level and attribute level properties are automatically loaded during device initialisation when starting-up a device server or calling the
“init” command, while the reading and writing of free properties must be handled by the programmer. Device, attribute and class level properties can also be initialised with default values set at the interface creation time, for example, with [Pogo](#pogo-documentation). Default values are stored in the device server code and are overwritten when another value is found in the configuration database.

It is necessary to assign a default value for every property. This value will be used when the property is not defined in the Tango database. If a default value for a device property does not make sense, the property should be declared as mandatory. A mandatory property has to have a value configured in the Tango
database. If no value is configured, the device initialisation will stop with an exception on the missing property value.