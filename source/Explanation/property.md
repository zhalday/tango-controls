(properties)=

# Property

The property concept in Tango Control System is foundamental to its approach in managing and controlling devices. In Tango, each device has properties, which are configurations that define the characteristics and the unique behavior of each device.

## Property format
In the Tango Control System, properties are represented as key-value pairs, where the key is the property name, and the value is the property's setting or configuration. Property values can come in several different data formats depending on the complexity and requirements of the device or class. Here’s a breakdown of common formats:

- String: Properties can be simple strings i.e: "ip" = "192.168.0.21"
- Integer: Integer values are used for properties that define discrete numerical settings i.e: "max_speed" = 1000
- Double: properties that require decimal precision i.e: "threshold" = 0.05
- Boolean: property that is either True or False i.e: "enabled" = True
- Array: Properties can also be arrays of values, typically for configurations requiring multiple entries i.e: "calibration" = [0.0, 23.2, 55.4, 76.2, 100.0]

Properties in TANGO are divided into four main types: device properties, class properties, attribute properties and free properties.

These properties are managed in the Tango database, which stores and provides persistent access to property values. The properties can be retrieved, updated and reconfiguration of devices as needed.

## Device Properties:

These properties are specific to individual devices.
They define settings and parameters that are unique to each device instance.
Examples include network addresses, calibration parameters, or limits unique to a device.

## Class Properties:

Class properties apply to all instances of a particular class.
They help in defining default configurations shared across devices of the same type, offering consistency and reducing the need for repetitive configuration.
For example, all motors of a specific model might share a class property defining maximum speed.

## Attribute Properties:

Attributes properties define the configuration of the device [attributes](#tango-attribute-model).
These include properties such as data type, display range, alarm limits, and units, ensuring attributes have both meaning and safety constraints.
For example, a temperature sensor’s attribute might have properties defining the minimum and maximum allowable values, units in Celsius, and alarm thresholds.


## Free properties

Free properties are defined and used for the entire control system. For example, the event system can be configured to send message via a [multicast](#configuring-events-to-use-multicast-transport).


