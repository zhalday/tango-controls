# Device

A device is a key concept of Tango Controls. It is an object providing access to its {term}`attributes <attribute>`, {term}`pipes <pipe>` and {term}`commands <command>`. The device may relate to a piece of hardware or it may be a kind of a logical device providing some functionalities not directly related to hardware. 

Each device belongs to a [device class](#device-class). 

Devices are created by device servers, which will call the device classes. Each device is created and stored in a process called a device server. This will call the device class that the device belongs to. Devices are configured at runtime via a set of properties which are stored in the database.

All devices support a **black box** where client requests for attributes or operations are recorded. This feature allows easier debugging session for device already installed in a running control system.


## Device Class

A device class is an abstraction of a device’s interface. The device class contains a complete description and implementation of the behavior of all members of that class. It defines the list of attributes, pipes and commands that are available for a certain device, which are then available to users and to other components of a Tango system. 

A device class often relates to the specific hardware that it interfaces with, for example the `SerialLine` class defines an interface to communicate with serial line hardware.

All classes are derived from one root class thus allowing some common behavior for all devices. New device classes can also be constructed out of existing device classes. In this way a new hierarchy of classes can be built up in a short time. Device classes can use existing devices as sub-classes or as sub-objects. The practice of reusing existing classes is classical for Object Oriented Programming (OOP) and is one of its main advantages.
