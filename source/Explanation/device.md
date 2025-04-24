(device-explanation)=

# Device

%[glossary_term][device]
%A device is a key concept of Tango Controls. It is an object providing access to its {term}`attributes <attribute>`, {term}`pipes <pipe>` and {term}`commands <command>`. The list of attributes, pipes and commands available for a certain device is defined by its {term}`class <device class>`. The device may be related to a hardware device it interfaces with or it may be a kind of a logical device providing some functionalities not directly related to hardware.

A device is a key concept of Tango Controls. It is an object providing access to its {term}`attributes <attribute>`, {term}`pipes <pipe>` and {term}`commands <command>`. The device may relate to a piece of hardware or it may be a kind of a logical device providing some functionalities not directly related to hardware.

Each device belongs to a [Device Class](#device-class).

Devices are created by [Device Servers](#device-server), which will call the device classes. Each device is created and stored in a process called a device server. This will call the device class that the device belongs to. Devices are configured at runtime via a set of properties which are stored in the database.

All devices support a **black box** where client requests for attributes or operations are recorded. This feature allows easier debugging session for device already installed in a running control system.

In the real world, devices vary from serial line devices to devices interfaced by field-bus to memory mapped VME cards or PC cards to entire
data acquisition systems. The definition of a device depends very much on the user’s requirements. In the simple case a device server can be
used to hide the serial line protocol required to communicate with a device. For more complicated devices the device server can be used to
hide the entire complexity of the device timing, configuration and acquisition cycle behind a set of high level commands.


## Device Class

%[glossary_term][device class]
%A Device Class is an abstraction of a device's interface. It defines {term}`attributes <attribute>`, {term}`pipes <pipe>`, {term}`commands <command>` and {term}`properties <property>` which a device of the class provides to users and to other components of a Tango system. A device class ofter relates to a specific kind of equipment it allows to interface with like a `SerialLine` class defines interface to communicate with serial line equipment.

A device class is an abstraction of a device’s interface. The device class contains a complete description and implementation of the behavior of all members of that class. It defines the list of attributes, pipes and commands
that are available for a certain device, which are then available to users and to other components of a Tango system.

A device class often relates to the specific hardware that it interfaces with, for example the `SerialLine` class defines an interface to communicate with serial line hardware.

All classes are derived from one root class thus allowing some common behavior for all devices. New device classes can also be constructed out of existing device classes. In this way a new hierarchy of classes can be built up in a
short time. Device classes can use existing devices as sub-classes or as sub-objects. The practice of reusing existing classes is classical for Object Oriented Programming (OOP) and is one of its main advantages.

### The `DeviceClass`

#### Description

Every device of the same class supports the same list of commands and hence this list of available commands is stored in the `DeviceClass`. For example, the structure returned by the `info` operation contains a URL to the documentation. This URL is the same for every device belonging to the same class and hence the documentation URL is a data member of this class. There should only be one instance of this class per device. The `DeviceClass` also stores the device list.

The `DeviceClass` is an abstract class because the two methods `device_factory()` and `command_factory()` are declared as `pure virtual`. The role of the `device_factory()` method is to create all the devices belonging to the device class. The role of the `command_factory()` method is to create one instance of all the classes needed to support device commands.

The `DeviceClass` also contains the `attribute_factory` method whose role is to store the name of all the device attributes. The default implementation of this method is an empty body representing a device without any attributes.

#### Contents

The contents of this class can be summarize as:

- The `command_handler` method
- Methods to access data members
- Signal related method (C++ specific)
- Class constructor. It is protected to implements the Singleton  pattern
- Class data members like the class command list, the device list, etc

(device-server)=
(device-server-explanation)=

## Device Server

%[glossary_term][device server]
%A Device Server is a program (executable) which is able to create {term}`devices <device>` of certain classes. A Device Server may implement one or multiple classes and instantiate one or more devices. A running device server is called a {term}`device server instance`.

%[glossary_term][device server instance]
%A running device server is called a device server instance. So it means, it is a process. Every device server instance has an unique name in Tango Controls by which it can be referenced. The name is built as *\{DeviceServerName}*/*\{instanceName}*. For each running device server the system creates a special device of `DServer` {term}`device class`: *dserver/\{DeviceServerName}/\{instanceName}*. This device provides a management facility for the corresponding device server instance (see [DServer class device commands ](#dserver-class-device-commands)).

A Device Server is the process (i.e. the executable) that will create, run and serve instances of Devices.
It must contain one or more [Device Class](#device-class), and can instantiate any number of [Devices](#device) from those classes.
[Devices](#device) started from the same Device Server will run in the same process and hence share system resources such as memory, therefore it can be convenient to group devices into the same Device Server to optimise performance.

Each Device Server has a unique name made up of the name of the executable and a character string called the instance name.
The pair of executable / instance name has to be unique in a Tango control system.
The Device Server is responsible for querying the database to find out the list of Devices and their Device Classes to create.
The Device Server must create the Devices, call their initialise routine and export them once the Device is created.

Device Servers create an internal device of their own called the **Admin** Device.
This device is used to monitor and control the Device Server process lifecycle. It can perform tasks like restarting Devices, restarting the Device Server process, and starting or stopping polling.

Device Servers are linked to the Device classes that they will serve. Device Servers are usually managed by the [Astor](inv:astor:std#index) tool.

```{figure} device/deviceservermodel.jpg
Runtime representation of a Device server with two classes A and B
```
