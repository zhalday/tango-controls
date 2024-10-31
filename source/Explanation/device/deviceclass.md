(device-class)=
# Device Class

A device class is an abstraction of a device’s interface. The device class contains a complete description and implementation of the behavior of all members of that class. It defines the list of attributes, pipes and commands 
that are available for a certain device, which are then available to users and to other components of a Tango system. 

A device class often relates to the specific hardware that it interfaces with, for example the `SerialLine` class defines an interface to communicate with serial line hardware.

All classes are derived from one root class thus allowing some common behavior for all devices. New device classes can also be constructed out of existing device classes. In this way a new hierarchy of classes can be built up in a 
short time. Device classes can use existing devices as sub-classes or as sub-objects. The practice of reusing existing classes is classical for Object Oriented Programming (OOP) and is one of its main advantages.

## The `DeviceClass`

### Description

Every device of the same class supports the same list of commands and hence this list of available commands is stored in the `DeviceClass`. For example, the structure returned by the `info` operation contains a URL to the documentation. This URL is the same for every device belonging to the same class and hence the documentation URL is a data member of this class. There should only be one instance of this class per device. The `DeviceClass` also stores the device list. 

The `DeviceClass` is an abstract class because the two methods `device_factory()` and `command_factory()` are declared as `pure virtual`. The role of the `device_factory()` method is to create all the devices belonging to the device class. The role of the `command_factory()` method is to create one instance of all the classes needed to support device commands. 

The `DeviceClass` also contains the `attribute_factory` method whose role is to store the name of all the device attributes. The default implementation of this method is an empty body representing a device without any attributes.

### Contents

The contents of this class can be summarize as:

- The `command_handler` method
- Methods to access data members
- Signal related method (C++ specific)
- Class constructor. It is protected to implements the Singleton  pattern
- Class data members like the class command list, the device list, etc