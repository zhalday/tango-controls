# Device Server

{audience}`all`

A Tango Device Server is the process, the executable, that will create, run and serve instances of Devices.
It must contain one or more [Tango Classes](./deviceclass.md), and can instantiate any number of [Devices](./device.md) from those classes.
[Devices](./device.md) started from the same Device Server will run in the same process and therefore share resources like memory, so it can be convenient for example for performance to group devices in a same Device Server. 

Each Device Server has a unique name made up of the name of the executable and a character string called the instance name. 
The pair of executable / instance name has to be unique in a Tango control system. 
The Device Server is responsible for querying the database to find out the list of Devices and their Device Classes to create. 
The Device Server must create the Devices, call their initialise routine and export them once the Device is created.

Device Servers create an internal device of their own called the **Admin** Device. 
This device is used to monitor and control the Device Server process lifecycle like restarting an all  Devices or the Device Server process, and starting or stopping polling. 
The Admin Device manages a BlackBox of the last N actions executed on Devices managed by the Device Server process for debugging and monitoring purposes.

Device Servers are linked with the Device classes that they will serve. Device Servers are usually managed by the [Astor](inv:astor:std#index) tool.

```{figure} img/deviceservermodel.jpg
Runtime representation of a Device server with two classes A and B
```

