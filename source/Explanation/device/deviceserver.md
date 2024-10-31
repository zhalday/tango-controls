# Device Server

{audience}`all`

A Tango Device Server is the process, the executable, that will contains and run instances of devices.
It can contain one or more [Tango Classes](./deviceclass.md), and instantiate any number of [devices](./device.md) from those classes.
[Devices](./device.md) started from the same Device Server will share resources so it can be convenient to group devices in a same Device Server.

```{figure} img/deviceservermodel.jpg
Runtime representation of a Device server
```

