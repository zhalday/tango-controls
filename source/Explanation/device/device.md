# Device

A device is a key concept of Tango Controls. It is an object providing access to its {term}`attributes <attribute>`, {term}`pipes <pipe>` and {term}`commands <command>`. The device may relate to a piece of hardware or it may be a kind of a logical device providing some functionalities not directly related to hardware. 

Each device belongs to a [device class](#device-class). 

Each device is created and stored in a process called a [device server](#device-device-server). This will call the device class that the device belongs to. Devices are configured at runtime via a set of properties which are stored in the database.

All devices support a **black box** where client requests for attributes or operations are recorded. This feature allows easier debugging session for device already installed in a running control system.
