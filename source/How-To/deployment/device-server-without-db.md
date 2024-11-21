(device-server-without-database)=

# Running a device server without database

```{tags} audience:administrators, audience:developers
```

In some cases (Running a device server within a lab during hardware development, testing, ...), it can be
useful to have a device server able to run even if there is no {term}`Tango database` or {term}`File database`
available in the control system. Obviously, running a Tango device server without a database means loosing
some Tango features:

- No check that the same {term}`device server` is running twice
- No device configuration via {term}`properties <property>`
- No {term}`memorized attributes <Memorized Attribute>`
- No device attribute configuration via the database
- No check that the same {term}`device name <device>` is used twice within the same control system
- In case of several device servers running on the same host, the user
  must manually manage a list of already used network port

To run a device server without database, the **-nodb** command line option for the device server must be used.
One problem when running a device server without the database is to pass device name(s) to the device server.
Within Tango, it is possible to define these device names at two different levels :

1. At the command line with the **-dlist** option: In case of a device
   server with several {term}`device pattern` implementations, the device name
   list given at the command line is only for the last device pattern
   created in the *class_factory()* method. In the device name list,
   the device name separator is the comma character.

<!-- TODO unclear/broken, see https://gitlab.com/tango-controls/cppTango/-/issues/1355 -->

2. At the device pattern implementation level: In the class inherited
   from the Tango::DeviceClass class via reimplemntation of the method
   *device_name_factory()* (cppTango and PyTango).

Device definition at the command line has higher priority than overriding *device_name_factory*.

If nothing is passed or set, the device name *NoName* is used for each device pattern implementation.

## Example of device server started without database usage

Without database, you need to start a Tango device server on a
pre-defined port, and you must use one of the underlying ORB options
called *endPoint* like

{command}`server inst -ORBendPoint giop:tcp::<port number> -nodb -dlist a/b/c`

<!-- TODO Mention Class:: syntax once https://gitlab.com/tango-controls/cppTango/-/issues/1355 is fixed -->

which would start the device server executable `server` as the instance `inst` on all available network
interfaces giving it the device name `a/b/c`.

Two examples of starting a device server without database
database when the *device_name_factory()* method is not re-defined.

- {command}`StepperMotor et -nodb -dlist id11/motor/1,id11/motor/2`

  This command line starts the device server with two devices named *id11/motor/1* and *id11/motor/2*

- {command}`StepperMotor et -nodb`
  This command line starts a device server with one device named *NoName*

When the *device_name_factory()* method is re-defined within the
StepperMotorClass class.

```{code} cpp
:number-lines: 1

  void StepperMotorClass::device_name_factory(vector<string> &list)
  {
      list.push_back("sr/cav-tuner/1");
      list.push_back("sr/cav-tuner/2");
  }
```

- {command}`StepperMotor et -nodb`

  This commands starts a device server with two devices named *sr/cav-tuner/1* and *sr/cav-tuner/2*

- {command}`StepperMotor et -nodb -dlist id12/motor/1`

  Starts a device server with only one device named *id12/motor/1*

## Connecting clients to a device within a device server started without database

In this case, the host and port on which the device server is running
are part of the device name. If the device name is *a/b/c*, the host is
*mycomputer* and the port *1234*, the device name to be used by client
is

{command}`mycomputer:1234/a/b/c#dbase=no`

Some clients like atkpanel require *tango://* prefix:

{command}`tango://mycomputer:1234/a/b/c#dbase=no`

See [device naming ](#tango-object-naming) for all details about Tango object naming.
