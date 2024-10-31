# Device Server

{audience}`all`

A Tango Device Server is the process, the executable, that will create, run and serve instances of Devices.
It must contain one or more [Tango Classes](./deviceclass.md), and can instantiate any number of [Devices](./device.md) from those classes.
[Devices](./device.md) started from the same Device Server will run in the same process and therefore share resources like memory, so it can be convenient for example for performance to group devices in a same Device Server. 

Device Servers create an internal device of their own called the **admin** Device. 
This device is used to monitor and control the Device Server process lifecycle like restarting an individual Device or the whole process.

```{figure} img/deviceservermodel.jpg
Runtime representation of a Device server with two classes in it
```

