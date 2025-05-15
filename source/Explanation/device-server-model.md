(deviceservermodel)=

# The Tango device server model

```{tags} audience:developers, lang:all
```

%[glossary_term][TDSOM]
%The Tango device server object model. Abstract model how Tango devices and client interact.

This chapter describes the Tango device server object model, hereafter
referred to as {term}`TDSOM`.

The TDSOM can be divided into the following basic elements:

- device
- server
- database
- API

This chapter will treat each of the above elements
separately.

Some knowledge of COBRA might be useful when reading this chapter - please
see [](corba-intro).


## The model

The basic idea of the TDSOM is to treat each {term}`device` as an `object`.
Each device is a separate entity which has its own data and behavior.
Each device has a unique name which identifies it in network name space.
Devices are organized according to `classes`, each device belonging to
a class. All classes are derived from one root class thus allowing some
common behavior for all devices. Five kind of requests can be sent to a
device:

- Execute actions via Tango `commands`
- Read/Set data specific to each device belonging to a class via Tango `attributes`
- Read/Set data specific to each device belonging to a class via Tango `pipes`
- Read some basic device data available for all devices via [CORBA](corba-intro) attributes
- Execute a predefined set of actions available for every device via
  CORBA operations

Each device is stored in a process called a {term}`device server`. Devices
are configured at runtime via {term}`properties <property>` which are stored in the
{term}`database <Tango Database>`.

(devicesection-deviceservermodel)=

## The device

The device is at the heart of the TDSOM. A device is an abstract concept
defined by the TDSOM. In reality, it can be a piece of hardware (an
interlock bit), a collection of hardware (a screen attached to a stepper
motor), a logical device (a taper) or a combination of all these (an
accelerator). Each device has a unique name in the control system and
eventually one alias. Within Tango, a four field name space has been
adopted consisting of

```
[//TANGO_HOST:PORT/]DOMAIN/FAMILY/MEMBER
```

`TANGO_HOST:PORT` refers to the {term}`tango database`,
domain refers to the sub-system, family the group and member the instance of the device.
Device name alias(es) must also be unique within a control system. There
is no predefined syntax for device name alias.

Each device belongs to a class. The {term}`device class` contains a complete
description and implementation of the behavior of all members of that
class. New device classes can be constructed out of existing device
classes. In this way a new hierarchy of classes can be built up in a short
time. Device classes can reuse existing devices as sub-classes.

All device classes are derived from the exact same base class (the device root
class) and implements the **identical CORBA interface**. All devices
implementing the identical CORBA interface ensures that all control objects support
the same set of CORBA operations and attributes. The device root class
contains part of the common device code. By inheriting from this class,
all devices share a common behavior. This also makes maintenance and
improvements to the TDSOM easy to carry out.

All devices also bring a `black box` where client requests for
attributes and operations are recorded. This feature helps in debugging sessions
of devices already installed in a running control system. This is a lightweight alternative to
[telemetry](telemetry-howto).

(commands-deviceservermodel)=

### Tango Commands

Commands are executed using two CORBA operations named `command_inout` for synchronous commands and
`command_inout_async` for asynchronous commands. These two operations call a special method implemented in
the device root class, the `command_handler` method. The `command_handler` calls an `is_allowed` method
implemented in the device class before calling the command itself. The `is_allowed` method is specific to each
command [^fn:command]. It checks to see whether the command to be executed is compatible with the present
device state. The command function is executed only if the `is_allowed` method allows it. Otherwise, an
exception is sent to the client.

### Tango attributes

In addition to commands, Tango devices also support normalized data
types called attributes [^fn:attribute]. Commands are device specific and the data
they transport are not normalized i.e. they can be any one of the Tango
data types with no restriction on what each byte means. This means that
it is difficult to interpret the output of a command in terms of what
kind of value(s) it represents. Generic display programs need to know
what the data returned represents, in what units it is, plus additional
information like minimum, maximum, quality etc. Tango attributes solve
this problem.

Tango attributes are zero, one or two dimensional data which have a fixed
set of properties e.g. quality, minimum and maximum, alarm low and high.
They are transferred in a specialized Tango type and can be READ, WRITE
or READ-WRITE. A device can support a list of attributes. Clients can
read one or more attributes from one or more devices. To read Tango
attributes, the client uses the `read_attributes` operation. To write
Tango attributes, a client uses the `write_attributes` operation. To
write then read Tango attributes within the same network request, the
client uses the `write_read_attributes` operation. To query a device
for all the attributes it supports, a client uses the
`get_attribute_config` operation. A client is also able to modify
some of the parameters defining an attribute with the
`set_attribute_config` operation. These five operations are defined
in the device CORBA interface.

Tango support thirteen data types for attributes (and arrays for one
or two dimensional data) which are: boolean, short, long (32 bits), long
(64 bits), float, double, unsigned char, unsigned short, unsigned long
(32 bits), unsigned long (64 bits), string, a specific data type for
Tango device state and finally another specific data type to transfer
data as an array of unsigned char with a string describing the coding of
the data.

### The Tango pipes

:::{warning}
Pipes are slated for removal.
:::

Tango devices also support pipes.

In some cases, it is required to exchange data between client and device
of varying data type. This is for instance the case of data gathered
during a scan on one experiment. Because the number of actuators and
sensors involved in the scan may change from one scan to another, it is
not possible to use a well defined data type. Tango pipes have been
designed for such cases. A Tango pipe is basically a pipe dedicated to
transfer data between client and device. A pipe has a set of two
properties which are the pipe label and its description. A pipe can be
read or read-write. A device can support a list of pipes. Clients can
read one or more pipes from one or more devices. To read a Tango pipe,
the client uses the `read_pipe` operation. To write a Tango pipe, a
client uses the `write_pipe` operation. To write then read a Tango
pipe within the same network request, the client uses the
`write_read_pipe` operation. To query a device for all the pipes it
supports, a client uses the `get_pipe_config` operation. A client is
also able to modify some of parameters defining a pipe with the
`set_pipe_config` operation. These five operations are defined in
the device CORBA interface.

In contrast to commands or attributes, a Tango pipe does not have a
pre-defined data type. Data transferred through pipes may be of any
basic Tango data type (or array of) and this may change every time a
pipe is read or written.

### Commands, attributes or pipes?

There are no strict rules concerning what should be returned as command
result and what should be implemented as an attribute or as a pipe.
Nevertheless, attributes are more adapted to return physical values which
have a kind of time consistency. Attribute also have more properties
which help the client to precisely know what it represents. For
instance, the state and the status of a power supply are not physical
values and are returned as command results. The current generated by the
power supply is a physical value and is implemented as an attribute. The
attribute properties allow a client to know its unit, its label and some
other information which are related to a physical value. Commands are
well adapted to send orders to a device like switching from one mode of
operation to another mode of operation. For a power supply, the switch
from a STANDBY mode to a ON mode is typically done via a command.
Finally, pipe is well adapted when the kind and number of data exchanged
between the client and the device changes with time.

### The CORBA attributes

Some key data implemented for each device can be read without the need
to call a command or read an attribute:

- The device state: a number representing its state. A set of predefined states are defined in the TDSOM.
- The device status: a string describing in plain text the device state and any additional useful information of
the device as a formatted ASCII string.
- The device name: name as defined [here](devicesection-deviceservermodel)
- The administration device name called `adm_name`: for each set of devices grouped within the same server, an
administration device is automatically added. This `adm_name` is the name of the administration device.
- The device description: an ASCII string describing the device


These five CORBA attributes are implemented in the device root class and therefore do not need to be
implemented by the device server developer. As explained in the [CORBA](corba-intro)
paragraph, the CORBA attributes are not allowed to raise exceptions whereas command (which are implemented
using CORBA operations) can.

### The remaining CORBA operations

The TDSOM also supports a list of actions defined as CORBA operations in
the device interface and implemented in the device root class.
Therefore, these actions are implemented automatically for every Tango
device:

```{list-table}
:header-rows: 1

* - Operation
  - Explanation
* - ping
  - Ping a device to check if the device is alive and reachable over the network
    Obviously, it checks only the connection from a client to the device and not all the device functionalities
* - command_list_query
  - Request a list of all the commands supported by a device with their input, output types and description
* - command_query
  - Request information about a specific command which are its input, output type and description
* - info
  - Request general information on the device like its name, the host where the device server hosting the
    device is running etc.
* - black_box
  - Read the device black-box as an array of strings
```

### The special case of the device state and status

The device state and status are the most important pieces of device information.
Nearly all client software dealing with Tango devices need device
state and/or status. In order to simplify client software developer
work, it is possible to get these two piece of information in three
different ways:

1. Using the appropriate CORBA attribute (`state` and `status`)
2. Using a command on the device. The commands are called `State` and `Status`
3. Using attributes: Even if the state and status are not real attributes,
   it is possible to get their value using the `read_attributes`
   operation. Nevertheless, it is not possible to set the attribute
   configuration for state and status. An error is reported by the
   server if a client tries to do so.

### Device polling

Within the Tango framework, it is also possible to force executing
commands or reading attributes at a fixed frequency. This is called
`device polling`. This is automatically handled by Tango core software
with a pool of polling threads. The command results or attribute values are
stored in circular buffers. When a client wants to read an attribute value,
or command result, for a polled attribute/command they have
the choice to get the attribute value (or command result) with direct
access to the device or from the last value stored in the device ring
buffer. The latter is optimal for “slow” devices as getting data from
the buffer is much faster than accessing the device itself. The
disadvantage is the time taken between the data returned from
the polling buffer and the time of the request. Polling a command is
only possible for commands without input arguments and these commands should also be idempotent.
It is not possible to poll a device pipe.

Two other CORBA operations called `command_inout_history_X` and
`read_attribute_history_X` allow a client to retrieve the history of
polled commands/attributes stored in the polling buffers.

See the [device polling](./../Explanation/polling.md#device-polling) explanation for details.

## The server

Another integral part of the TDSOM is the server concept. The server
(also referred to as the device server) is a process where the main task is to
offer one or more services to one or more clients. To do this, the
server has to spend most of its time in a loop waiting for clients
to connect to it. The devices are hosted in the server process. A server
is able to host several classes of devices. In the TDSOM, a device of
the `DServer` class is automatically hosted by each device server.
This class of device supports commands which enable remote device server
process administration.

(tango-logging-service-overview)=
## The Tango Logging Service

During software life, it is always convenient to print miscellaneous
information which help to:

- Debug the software
- Report on error
- Give regular information to the user

This is classically done using the `print` function in your chosen programming language. In a highly
distributed control system, it is difficult to get all this information coming from a high number of
different processes running on a large number of computers. Tango has incorporated a
Logging Service called the Tango Logging Service (TLS) which allows print messages to be:

- Displayed on a console (the classical way)

- Sent to a file

- Sent to specific Tango device called `LogConsumer`. The Tango package has
  an implementation of a log consumer where every consumer device is
  associated to a graphical interface.

The log consumer's graphical interface displays messages but could also be used to sort messages, to filter
messages etc. With this feature it is possible to centralize these messages coming from different devices
embedded within different processes.

These log consumers can be:

  - Statically configured meaning that it memorizes the list of Tango
    devices for which it will get and display messages
  - Dynamically configured. The user chooses devices from which they want to see messages

## The database

To achieve complete device independence, it is however necessary to
supplement device classes with the possibility for configuring device
dependencies at runtime. The utility which does this in the TDSOM is the
`property database`. Properties [^fn:properties] are identified by an ASCII string
and the device name. Tango attributes are also configured using
properties. This {term}`database <Tango Database>` is also used to store device network addresses
(CORBA {abbr}`IORs (Interoperable Object Reference)`), list of classes hosted by a device server process and
list of devices for each class in a device server process. The database
ensures the uniqueness of device name and of aliases. It also links device
name and its list of aliases.

Tango uses [MariaDB](https://mariadb.org) as its SQL-database.
The database is accessed via a classical Tango device hosted in a device
server. Therefore, client access the database via Tango commands
requested on the database device.

## The controlled access

:::{warning}
This prevents accidental changes only and is not secure against malicious actors.
:::

Tango also provides a controlled access system called {term}`Tango Access Control`.
It’s a simple controlled access system and does not provide encrypted communication or
sophisticated authentication. It simply defines which user (based on
computer login authentication) is allowed to do which command (or
write attribute) on which device and from which host. The information
used to configure this controlled access feature is stored in the Tango
database and accessed by a specific Tango device server which is not the
classical Tango database device server described in the previous
section. Two access levels are defined:

- Everything is allowed for this user from this host
- The write-like calls on the device are forbidden and according to
  configuration, a command subset is also forbidden for this user from
  this host

## The Application Programming Interfaces

### Rules of the API

While it is true that Tango clients can be programmed using only the CORBA
API, CORBA knows nothing about Tango. This means clients have to know all
the details of retrieving {abbr}`IORs (Interoperable Object Reference)` from the Tango database, the additional
information to send on the wire, the Tango version control etc. These
details can and should be wrapped in the Tango Application Programming
Interface (API). The API is implemented as a library in C++ and as a
package in Java. [PyTango](inv:pytango:std#index) has been implemented on top
of the C++ API. The API is what makes Tango clients easy to write.

The APIs consist of the following basic classes:

%[glossary_term][AttributeProxy]
%The AttributeProxy is a placeholder on the client side with exactly the same interface that a real
%{term}`Attribute <attribute>` exposes. Only when an operation on an AttributeProxy is performed, a connection
%to the Attribute of a real Device is attempted and on success the operation is performed. In case the Attribute
%of the real Device cannot be reached, a client-side Tango exception is raised.

%[glossary_term][DeviceProxy]
%The DeviceProxy is a placeholder on the client side with exactly the same interface that a real {term}`Device
%<device>` exposes. Only when an operation on a DeviceProxy is performed, a connection to the real Device is
%attempted and on success the operation performed. In case the real Device cannot be reached, a client-side
%Tango exception is raised.

%[glossary_term][client]
%In Tango a client is either a {term}`DeviceProxy` or an {term}`AttributeProxy` instance created by a program.

- `DeviceProxy` which is a *proxy* to the real {term}`device`
- `AttributeProxy` which is a *proxy* to an {term}`Attribute <attribute>` of a real device
- `DeviceData` to encapsulate data to send/receive from/to device via
  commands
- `DeviceAttribute` to encapsulate data to send/receive from/to device via
  attributes
- `Group` which is a *proxy* to a group of devices

:::{note}
In Tango the term client usually refers to either an {term}`AttributeProxy` or to a {term}`DeviceProxy`.
:::

In addition to these main classes, many other classes allow interfacing
to all Tango features. The following figure is a drawing of a
typical client/server application using Tango.

```{image} device-server-model/archi.png
```

The database is used during the server and client startup phase to establish
a connection between client and server.

### Communication between client and server using the API

With the API, it is possible to request commands to be executed on a
device or to read/write device attribute(s) using one of the two
communication models implemented. These two models are:

1. The synchronous model where the client waits (and is blocked) for the
   server to send the answer or until a timeout is reached.
2. The asynchronous model. In this model, the clients sends the request
   and immediately returns. It is not blocked. It is free to do whatever
   it has to do like updating a graphical user interface. The client has
   the choice to retrieve the server answer by checking if the reply has
   arrived by calling an API specific call or by requesting that a
   callback method is executed when the client receives the server
   response.

### Tango events

On top of the two communication models previously described, Tango offers
an event system. The standard Tango communication paradigm is a
synchronous/asynchronous two-way call. In this paradigm the call is
initiated by the client who contacts the server. The server handles the
client’s request and sends the answer to the client or throws an
exception which the client catches. This paradigm involves two calls to
receive a single answer and requires the client to be active in
initiating the request. If the client has a permanent interest in a
value it is obliged to poll the server for an update in a value every
time. This is not efficient in terms of network bandwidth usage nor in terms
of client programming.

For clients which are permanently interested in values, the event-driven
communication paradigm is a more efficient and natural way of
programming. In this paradigm the client registers its interest once in
an event (value). After that the server informs the client every time
the event has occurred. This paradigm avoids the client polling and frees
it for doing other things, which is faster and makes efficient use of the
network.

ZMQ is a library allowing users to create communicating systems. It implements
several well known communication pattern including the Publish/Subscribe
pattern, which is the basis of the new Tango event system. Using this
library, a separate notification service is not needed and event
communication is available with only client and server processes simplifying
the overall design.

The following figure is a schematic of the Tango event system:

```{image} device-server-model/event_schematic_zmq.png
```

[^fn:command]: In contrary to the `state_handler` method of the TACO device server
    model which is not specific to each command.

[^fn:attribute]: Tango attributes were known as signals in the TACO device server
    model

[^fn:properties]: Properties were known as resources in the TACO device server model
