# Tango Data Model

{audience}`all`

This page list and links to the different elements of the Tango Data Model.

## Simplified Model

The following diagram shows the main elements of the Tango Device Model :

```{mermaid}
classDiagram
  class cls["Device Class"]
  class dserver["Device Server"]
  click dserver href "./device.html#tango-device-server" "Device Server documentation"
  class Pipe
  click Pipe href "./pipe.html#tango-pipe-model" "Pipe documentation"
  class Command
  click Command href "./command.html#tango-command-model" "Command documentation"
  class Attribute
  click Attribute href "./attribute.html#tango-attribute-model" "Attribute documentation"
  class Event
  click Event href "./event.html" "Event documentation"
  class Device {
    domain
    family
    member
  }
  Pipe "*" <--* cls 
  Command "*" <--* cls
  Attribute "*" <--* cls
  Event "*" <--* Attribute
  State --|> Attribute
  Status --|> Attribute
  Device *--> "1" cls : belongs
  dserver *--> "1..*" Device
  Device *--> "*" DeviceProperty
```

## Complete Model

Here is a more complete version of the above:

```{mermaid}
classDiagram
  direction LR
  class cls["Device Class"]
  class dserver["Device Server"]
  click dserver href "./device.html#tango-device-server" "Device Server documentation"
  class Pipe
  click Pipe href "./pipe.html#tango-pipe-model" "Pipe documentation"
  class Command
  click Command href "./command.html#tango-command-model" "Command documentation"
  class Attribute
  click Attribute href "./attribute.html#tango-attribute-model" "Attribute documentation"
  class Event
  click Event href "./event.html" "Event documentation"
  class Device {
    domain
    family
    member
  }
  Pipe "*" <--* cls 
  Command "*" <--* cls
  Attribute "*" <--* cls
  Event "*" <--* Attribute
  DeviceInterfaceChangeEvent --|> Event
  ChangeEvent --|> Event
  ArchiveEvent --|> Event
  AlarmEvent --|> Event
  PeriodicEvent --|> Event
  UserEvent --|> Event
  DataReadyEvent --|> Event
  AttributeConfigurationEvent --|> Event
  State --|> Attribute
  Status --|> Attribute
  Device *--> "1" cls : belongs
  dserver *--> "1..*" Device
  Device *--> "*" DeviceProperty
  AdminDevice --|> Device
  dserver *--> "1" AdminDevice
  cls --|> DeviceImpl
  Property *--> "0..10" PropertyHistory
  AttributeProperty --|> Property
  DeviceAttributeProperty --|> AttributeProperty
  ClassAttributeProperty --|> AttributeProperty
  Device *--> "*" DeviceAttributeProperty
  DeviceProperty --|> Property
  PipeProperty --|> Property
  DevicePipeProperty --|> PipeProperty
  ClassPipeProperty --|> PipeProperty
  FreeProperty --|> Property
  ClassProperty --|> Property
  cls *--> "*" ClassProperty
  Pipe *--> "*" PipeProperty
  Attribute *--> "*" AttributeProperty
  note for Attribute "At least State and Status are always available"
  note for cls "The main class that the developer has to implement"
```

## Elements

| **Block**                   | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Device                      | Abstract concept defined by the TANGO device server object model; it can be a piece of hardware (an interlock bit) a collection of hardware (a screen attached to a stepper motor)a logical device (a taper) or a combination of all these (an accelerator). For more information please see the [device documentation](./device/device.md).                                                                                                                                                                                 |
| Device Class                 | From Object Oriented Programming concept, this is the main class that the developer has to implement                                                                                                                                                                                                                                                                                                                                                                                                            |
| DeviceServer                | The server (also referred as device server) is a process whose main task is to offer one or more services to one or more clients. To do this, the server has to spend most of its time in a wait loop waiting for clients to connect to it. The devices are hosted in the server process. A server is able to host several classes of devices.In short, it is a process that export devices available to accept requests). Fore more information see the [device server documentation](./device.md). |
| Property                    | Store a generic configuration                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| DeviceProperty              | Device specific configuration                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ClassProperty               | Class specific configuration                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| AttributeProperty           | Attribute specific configuration                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ClassAttributeProperty      | Attribute specific configuration at class level                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| DeviceAttributeProperty     | Specific configuration for a specific attribute of a specific device                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| FreeProperty                | User-defined specific configuration (for instance GUI, generic system and so on)                                                                                                                                                                                                                                                                                                                                                                                                                                |
| PropertyHistory             | History of the values for a property (maximum 10 latest are stored for each property)                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Attribute                   | See [attribute](./attribute.md).                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| AttributeAlias              | One word which can be used to identify a specific attribute. (shortcut)                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Pipe                        | See [pipe] (./pipe.md).                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| PipeProperty                | Pipe specific configuration                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| DevicePipeProperty          | Configuration of a specific pipe of a specific device                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ClassPipeProperty           | Configuration of a specific pipe for a specific class                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Event                       | See [event](./event.md).                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Command                     | See [command](./command.md).                                                                                                                                                                                                                                                                                                                                    |
| ChangeEvent                 | It is a type of event that gets fired when the associated attribute changes its value according to its configuration specified in system specific attribute properties (abs_change and rel_change). See [events](./event.md).                                                                                                                                                                                                                                                                 |
| ArchiveEvent                | It is a type of event that gets fired when the associated attribute should be archived according to its configuration specified in system specific attribute properties (archive_abs_change, archive_rel_change and archive_period). See [events](./event.md).                                                                                                                                                                                                                                |
| UserEvent                   | It is a type of event that gets fired when the device server programmer wants to. See [events](./event.md).                                                                                                                                                                                                                                                                                                                                                                                   |
| PeriodicEvent               | It is a type of event that gets fired at a fixed periodic interval. See [events](./event.md).                                                                                                                                                                                                                                                                                                                                                                                                 |
| DataReadyEvent              | It is a type of event that gets fired to inform a client that it is now possible to read an attribute. See [events](./event.md).                                                                                                                                                                                                                                                                                                                                                              |
| AttributeConfigurationEvent | It is a type of event that gets fired if the attribute configuration is changed. See [events](./event.md).                                                                                                                                                                                                                                                                                                                                                                                   |
| DeviceInterfaceChangeEvent  | It is a type of event that gets fired when the device interface changes. See [events](./event.md).                                                                                                                                                                                                                                                                                                                                                                                            |
| DeviceImpl                  | Base implementation of every class that will become a device.                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| State                       | The device state is a number which reflects the availability of the device.                                                                                                                                                                                                                                                                                                                                                                     |
| Status                      | The state of the device as a formatted ascii string                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| AdminDevice                 | Special type of Device dedicated to creating and managing the devices, i.e. restart device, kill the device server (the process), creating polling mechanism and so on                                                                                                                                                                                                                                                                                                                                          |

## Attributes

| **Block**    | **Attribute** | **Description**                                                                                                                                                                                                                                                                                    |
| ------------ | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Device       | name          | Correspond to “Domain/family/member”                                                                                                                                                                                                                                                               |
|              | alias         | A word that you can use to access the device, like a shortcut. Device name alias(es) must also be unique within a control system. There is no predefined syntax for device name alias.                                                                                                             |
|              | domain        | Each device has a unique name in the control system. Within Tango, a four field name space has been adopted consisting of\[//FACILITY/\]DOMAIN/CLASS/MEMBERFacility refers to the control system instance, domain refers to the sub-system, class the class and member the instance of the device. |
|              | family        |                                                                                                                                                                                                                                                                                                    |
|              | member        |                                                                                                                                                                                                                                                                                                    |
|              | version       | It correspond to the version of base device implementation class (for backward compatibility). It is used to know how to communicate with this device and what features are supported.                                                                                                             |
|              | class         | Name of the class corresponding to the Device                                                                                                                                                                                                                                                      |
|              | ior           | Orb Identifier used to connect with the device                                                                                                                                                                                                                                                     |
|              | host          | Where the device is running                                                                                                                                                                                                                                                                        |
|              | pid           | Id of the specific process                                                                                                                                                                                                                                                                         |
|              | exported      | Means that the device is available to accept request                                                                                                                                                                                                                                               |
| DeviceServer | Facility      | Represent the host where the device server instance (aka process) lives                                                                                                                                                                                                                            |
| Attribute    | alias         | A shortcut that you can use to access the attribute (in the Database there is a specific table)                                                                                                                                                                                                    |

## Relations

| **Left Block** | **Right Block**         | **Multiplicity** | **Description**                                                                                                               |
| -------------- | ----------------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Device         | Device Class             | 1                | Every device belongs to a Tango  Device class                                                                                         |
| Attribute      | ClassAttributeProperty  | 0..\*            | An attribute can have more than one class attribute property associated                                                       |
| Attribute      | Event                   | 0..\*            | An attribute can have more than one event associated                                                                          |
| Device         | DeviceAttributeProperty | 0..\*            | A device can have more than one Device Attribute Property associated                                                          |
| Device         | DeviceProperty          | 0..\*            | A device can have more than one Device Property associated                                                                    |
| Device         | Attribute               | 2..\*            | A Device can have more than one Attribute associated via reference                                                            |
| DeviceServer   | AdminDevice             | 1                | Every device server is exporting one admin device                                                                             |
| DeviceServer   | Device                  | 1..\*            | Every Device server has many devices inside itself                                                                            |
| Pipe           | PipeProperty            | 0..\*            | A pipe can have more than one Pipe Property associated                                                                        |
| Property       | PropertyHistory         | 0..10            | A Property can have more than one Property history associated (this will maintain the history of the change for the property) |
| Device Class    | Attribute               | 2..\*            | A Device Class can have more than one Attribute associated                                                                     |
| Device Class    | ClassProperty           | 0..\*            | A Device Class can have more than one Class Property associated                                                                |
| Device Class    | Command                 | 2..\*            | A Device Class can have more than one Command associated                                                                       |
| Device Class    | Pipe                    | 0..\*            | A Device Class can have more than one Pipe associated                                                                          |

## Rationale

Please refer to the [Tango Device Model ](#deviceservermodel).
