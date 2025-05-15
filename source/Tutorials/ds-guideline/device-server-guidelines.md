(ds-guidelines)=

# Guidelines for developing a Tango Device Server

```{tags} audience:developers, lang:all
```

This chapter describes guidelines for developing {term}`device servers <device server>`.
The {term}`Tango Device Server Model <TDSOM>` is flexible and permits different interpretations
of how to implement Device Servers,
however there is a recommended way of using Tango to implement device servers.
This chapter will document some of the best practices from experienced developers
for device development.

This chapter focuses on:

1. Device Server design consideration
2. Implementation good practices

These guidelines apply to features available in Tango v8 or higher.

# Tango Concepts

Some understanding of the basic Tango concepts is required to make use of
this tutorial. Please refer to the [](#explanation-index) section if further
information on these concepts is required.


# Tango Device Design

## Elements of general design

### Reusability

In a Tango control system, each device is a software component and
potentially reusable.

It is necessary to:

- Systematically evaluate prior to the coding of a device, the
  possibility of reusing a device available in the code
  repositories (Tango Controls community, local repository), in order to
  avoid several implementations of the same equipment.
- Design the device to be as reusable/extensible as possible because it may
  interest other developers in the community.

:::{topic} As such, the device must be:
:class: hint

- Configurable: (e.g. no port number “hard coded”, but use of a
  parameter via a property),
- Self-supporting: the device must be usable outside the private
  programming environment (e.g. all the necessary elements to use the
  device (compile, link) must be provided to the community). The use of
  the {abbr}`GPL (GNU General Public License)` should be considered, and the use of proprietary libraries
  should be avoided if possible,
- Portable: the device code must be (as far as possible) independent
  of the target platform unless it depends on platform specific
  drivers,
- Documented in English
:::

### Generic interface programming

The device must be as generic as possible which means the definition of
its interface should:

- Reflect the service rather than its underlying implementation. For
  example, a command named `WriteRead` reflects the communication
  service of a bus (type: message exchange), while a command named
  `NI488_Send` reflects a specific implementation of the supplier.
- Show the general characteristics (attributes and commands) of a
  common type of equipment that it represents. For example, a command
  `On` reflects the action of powering on a PowerSupply , while a
  command named `BruckerPSON` reflects a specific implementation which
  must be avoided.

The device interface must be service oriented, and not implementation
oriented.

### Abstract interfaces

### Singleton device

Tango allows a device server to host several devices which are
instantiations of the same Tango class.

However, in particular cases some technical constraints may forbid this.
In such a case, the Device Server programmer should anticipate
this in the device design phase and add, for example, a static variable
to count device instances and detect this misconfiguration. For
example, it can authorize the creation of a second instance (within the
meaning of the device creation) but systematically put the state to
`FAULT` (in the method `init_device`) and indicate the problem in the
Status.

In the case where technical constraints prohibit the deployment of
multiple instances of a Tango device within the same device server, the
developer has to ensure that only one instance can be created and
inform the user with a clear message in case more than one
device is configured in the database.

### Device states

When designing the device, you should clearly define the state machine
that will reflect the different states in which the device can be, and
also the associated transitions.

The state machine must follow these rules:

- At any time, the device state must reflect the internal state of the
  system it represents.
- The state should represent any change made by a client’s request.
- The device behaviour is specified and documented.


## Device interface definition

A Tango Device must be “self-consistent”. In the case where it represents a subset
of the control system, it must enable access to all of the associated
features (unless otherwise specified). The limit of its
“responsibilities”, meaning “separation of concerns”, is clearly
defined: 1 Device = 1 microservice = 1 element of the system. The analogy
with object-oriented programming is straightforward.

A Device is a **microservice** made available to any number of unspecified
clients. Its implementation and/or behaviour **must not make
assumptions about the nature and the number of its potential
clients**. In all cases, reactivity must be ensured (i.e. the
response time of the device must be minimised).

The first step in designing a device is to define the commands and the
attributes using Pogo (use {program}`Pogo` to define the Tango interface).

Except in (very) particular cases, always use an attribute to expose the
data produced by the device. The command concept exists
(see [Device Commands ](#device-commands))
but its use as an attribute substitute is prohibited. For example, a motor
must be moved by writing its associated ‘position’ attribute instead of
using a ‘GotoPosition’ command.

The choice will be made following these rules:

- Attribute: used for all values that are presented to the “client”. **It is
  imperative to use the attributes and to not use Tango commands that
  would act like a get/set couple.**
- Command: used for every action. In most cases this is a void-void type.

Any deviation from these rules must be justified in the description of
the attribute or command.

## Service availability

From the operator's perspective, the “**response time**” or
“**reactivity**” (i.e. the device is always responsive) is **the** reference
metric to describe the performance of a device. Ideally, the device
implementation must ensure the service availability regardless of the
external client load or the internal load. For the end user, it is
always very unpleasant to suffer a Tango timeout and receive an
exception instead of the expected response.

The response time of the device should be minimised and in all cases it
should be lower than the default Tango timeout of **3 seconds**.

If the action to be performed takes longer than that, execution should
be done asynchronously in the Tango class and its progress reported
in the state/status.

Several technical solutions are available to the device developer to
ensure service availability:

- Use the Tango polling mechanism,
- Use a threading mechanism, managed by the developer.

## Tango polling mechanism

### Polling interest

The polling mechanism is detailed in the Tango documentation
[Device Polling ](#device-polling).

Tango implements a mechanism called *polling* which alleviates the
problem of equipment response time (which is usually the weak point in
terms of performance). The response time of a GPIB link or a RS-232 link
is usually one to two orders of magnitude higher than the performance of
the Tango code executed by a client request.

### Polling limitations

From the perspective of the device activity, the polling is in direct
competition with client requests. The client load is therefore competing
with the polling activity.

This means that any polling activity has to be tuned in order to keep some
free time for the device to answer client requests. Do not try to poll a device
object with a polling period of 200 ms if the object access time
is 300 ms (*even if Tango implements some algorithm to minimize the bad
behavior of such badly tuned polling*).

For polled Tango device objects (attribute or command), client reading
does not generate any activity on the device whatever the number of clients.
The data are returned from the so-called polling buffer instead of
coming from the device itself. Therefore, an obvious rule is to poll the
key device object (state attribute, pressure attribute for a vacuum
valve...).

The recommendation for device polling tuning is to keep the device free
40% of time.

Let's take an example: for a power supply device, you want to poll the
device state and its current attribute, which for such a device are the
device key objects.

- State access needs 100 ms while current attribute reading needs 50
  ms.
- Because, you want to poll these two objects, the time required on the
  device by the polling mechanism will be 150 ms (100 + 50).
- In order to keep the 40% ratio, tune the polling period for this
  device to 250 ms.
- The device is then occupied by the polling mechanism during 150 ms
  (60 %) but free for other client activity for 100 ms (40 %).

Device polling is easily tunable at run time using the Jive and/or Astor
Tango tools.

### Threading mechanism

*Threading* is another possible solution for the load problem as a thread
(managed by the device developer) supports communication with the
material (*polling* or other) and the data obtained are put in the
“cache”. You can now produce the “last known value” to the client at any
time and optimize the response time. This approach, however, has a limit
as it is necessary to reread the value of the hardware to assure clients that the
returned value is the system “current state”.

For a C++ device, the implementation of a threading mechanism can be
done via the *DeviceTask* class from the *Yat4Tango library*. This class
owns a thread associated with a FIFO message list. Processing messages
can be synchronous or asynchronous.

See a complete C++ example of this in the
[AttributeSequenceWriter](https://gitlab.synchrotron-soleil.fr/software-control-system/tango-devices/softwaresystem/attributesequencewriter).

If the design of the Tango class requires threading, follow these rules:

- if it requires a simple thread, in C++ the recommendation is to use a C++11 thread,
- if it requires an acquisition thread with message exchanges then in C++ the recommendation is to
  use the `Yat4Tango::DeviceTask` class.

# Tango device implementation

## General rules

### Language

The Tango Controls community is international and the code can be
shared with the community, so it is recommended to use English for documenting a
device development.

English will be used for:

- The interfaces definition (attributes and commands),
- The device documentation (online help for command usage and
  attributes description),
- The comments inserted in the code by the developer,
- The error messages,
- The name of variables and internal methods added by the developer.

The choice of the language used for the user’s documentation of the
device server (“Device Server User’s Guide”) is left free, to focus on
the editorial quality. In the case of a joint development with another
institute, English will be used.

### Types

The types used for the device interface definition are Tango types
(`Tango::DevDouble`, `Tango::DevFloat` …). These types are presented by Pogo
and are not modifiable.

The types used by the developer in their own code are left free to choose
as long as they are not platform specific. Standard types of the
language used (Boolean, int, double …), Tango types or types from a
common library (Yat, Yat4Tango for C++) can potentially be used.

Direct conversions from the C++ type long to `Tango::DevLong` are only
supported on 32-bit platforms and should be avoided.

### Generated code

The automatically generated code by Pogo must not be modified by the
developer.

The developer must include their own code in the specified “PROTECTED REGION”
parts.

## Device interface

(naming-rules)=

### Naming rules

Having homogeneous conventions for naming attributes, commands and
properties is a good way to promote the reuse of device servers inside the Tango
collaboration.

It makes the development carried out by another institute easier to
understand and integrate into another Control System.

#### Class name

The Tango class name is obtained by concatenating the fields that
it is compose of – each field beginning with a capital letter:

Eg : {samp}`MyDeviceClass`

#### Device attributes

The device command and attribute names must be explicit and should
enable a quick understanding of the nature of the attribute or the command.

- Eg: for a power supply, you would have an attribute {samp}`{outputCurrent}`
  (not OC1) or a command {samp}`{ActivateOutput1}` (not ActO1).

The nomenclature recommendations are detailed in the section [Naming Rules ](#naming-rules).

:::{topic} **The attribute naming recommendations are**:
:class: hint

- Name composed of at least two characters,
- Only alphanumeric characters are allowed (no underscore, no dashes),
- Start with a **lowercase** letter,
- In case of a composite name, each sub-words must be capitalized
  (except the first letter),
- Prohibit any use of vague terms (eg: readValue).
:::

(device-commands-1)=

#### Device Commands

The recommendations are the same as those proposed for an attribute, except for the first letter of the name.

:::{topic} **The command naming recommendations are:**
:class: hint

- Name composed of at least two characters,
- Only alphanumeric characters are allowed (no underscore, no dashes),
- Start with a **uppercase** letter,
- In case of a composite name, each sub-words must be capitalized,
- Prohibit any use of vague terms (eg: Control).
:::

#### Device properties

The recommendations are the same as those proposed for a command.

:::{topic} **The property naming recommendations are:**
:class: hint

- Name composed of at least two characters,
- Only alphanumeric characters are allowed (no underscore, no dashes),
- Start with a **uppercase** letter,
- In case of a composite name, each sub-words must be capitalized,
- Prohibit any use of vague terms (eg: Prop1).
:::

### Device attributes nomenclature

It is a good practice that a particular signal type is always named in a
similar way in various device servers.

For example the intensity of a current should always be named
{samp}`{intensity}` (and not “**intens**”,
“**current**”,”**I**” depending on
the device server).

This allows the user to quickly make the link between the software
information and the physical sensor and reciprocally.

### Data types choice

Always use data types consistent with the underlying information.

- Unsigned integer must be used for the physical quantities that are
  suitable.

  - Eg: A number of samples `numSamples`, where negative values have no
    meaning, will be a `Tango::DevULong` (unsigned integer 32 bits) and
    not a `Tango::DevLong` (signed integer 32 bits).
  - Similarly, in such a case, the use of a floating point number should
    be prohibited as non-integer values also have no meaning in this context.s

- This rule is also applicable to input/output arguments of commands.

### Interface level choice

The choice between the *Expert* or the *Operator* level for an interface
must be thought through.

Only necessary commands for a nominal control of the
equipment must be accessible at the *Operator* level. The commands for
fine control of the equipment (eg: metrology, maintenance, unit test)
must only be accessible at the *Expert* level.

## Pogo use

### Device generation

The use of Pogo is mandatory for creating or modifying the device
interface.

Tango is constantly evolving but this tool will support all or part of the
porting associated to the kernel and the consequences on the IDL
interface.

In addition, it simplifies maintenance/development operations.

Every command, attribute, property or device state must be fully
documented; this documentation is done via the Pogo tool.

When creating an attribute with Pogo, the entire
configuration of the attribute must be fully filled in by the developer
(maximum possible) to avoid ambiguities.

Similarly, the states and their transitions must be described with
precision and clarity.

In fact:

- In operation, this documentation will be the reference for
  understanding the device behaviour. Remember that the operator will
  have this information with the generic tools (like {guilabel}`Test
  Device` from {program}`Jive`).

- The html documentations generated by {program}`Pogo` can also be accessed from a
  local server (particular to the institute).

- Consider also filling in the alarm values.

  - E.g. set the alarm values according to the specifications of the
    power supply, i.e., 0-24V for the voltage, or 0-3A for the output
    current.

Example for a temperature reading:

:::{figure} media/image9.png
:::

### Attributes generation in C++

In C++, Pogo automatically generates **pointers** to the data associated
with the attributes values (i.e. a pointer is generated for the read
part). The use of these pointers is not mandatory. The developer is free
to use their own data structure in the attribute value affectation.

## Internal device implementation

### Separation between the Tango interface and the internal system function

Don’t forget that the Tango interface is only a means to insert a microservice
in a control system. Therefore, it is necessary to think about the internal design
of the device like one would for any other application and just use Tango as an
interface on top of it.

As a rule of thumb if the code implemented within the Pogo markers is
too long it is good practice to move it to another class meaning the Pogo
generated methods will be only a few lines of code long.

In practice, it is necessary to avoid mixing the code generated by Pogo
and the code of the developer.

The Tango sub-class inherited from `Tango::DeviceImpl[_X]` instantiates
a class derived from the model object implementing the system, and
ensure the replacement between the external requests (clients) and the
implementation class(es).

In the choice of data structures, we are talking about those of the
developer’s object model, we will consider the technical constraints
imposed by Tango and/or the underlying layers (CORBA/ZMQ). The idea here is
to avoid copy and/or reorganisation of the data when transferred to the
client. For this, the developer needs to know/master the underlying
memory management mechanism (especially in C++). Please see the dedicated
section [](device-server-exchanging-data) for further details.

### Accessing the hardware: `always_executed_hook` vs. `read_attr_hardware`

It is essential to understand the concepts implemented by these two methods,
which are common methods for all Tango devices.

It is also necessary to clearly identify, in the design phase, the
possible consequences of implementing these two methods on the device
behaviour (remember that they are initially just empty shells generated
by Pogo).

- The `always_executed_hook()` method is called before each command
  is executed or before every read/write of an attribute (*but note, it is called
  **only once** when reading several attributes: see calling sequence
  below*).
- The `read_attr_hardware()` is called before every read of
  attribute(s)(*but note again, it is called **only once** when reading several
  attributes: see calling sequence below)*. This method aims to
  optimise (minimise) the equipment access in case of simultaneous
  reads of multiple attributes in the same request.

Given below is the calling sequence of these methods:

- *Command execution*

  - 1 – `always_executed_hook()`
  - 2 – `is_MyCmd_allowed()`
  - 3 – `MyCmd()`

- *Attribute reading*

  - 1 – `always_executed_hook()`
  - 2 – `read_attr_hardware()`
  - 3 – `is_MyAttr_allowed()`
  - 4 – `read_MyAttr()`

- *Attribute writing*

  - 1 – `always_executed_hook()`
  - 2 – `is_MyAttr_allowed()`
  - 3 – `write_MyAttr()`

- *Attributes reading*

  - 1 – `always_executed_hook()`
  - 2 – `read_attr_hardware()`
  - 3 – `is_MyAttr_allowed()`
  - 4 – `read_MyAttr()`

- *Attributes writing*

  - 1 – `always_executed_hook()`
  - 2 – `is_MyAttr_allowed()`
  - 3 – `write_MyAttr()`

This demonstrates why having “slow code” in the
`MyDevice::always_executed_hook` method can have serious consequences
on the device performance.

:::{note}
There is no obligation to use the `read_attr_hardware`
method; it depends on the equipment and its communication
channel (Ethernet, GPIB, DLL). Instead, one could have a call to the equipment in
the code of each attribute reading method.

For example, for an attribute “temperature”, of READ type, we can insert
the call to the equipment in the generated attribute reading method
`read_Temperature` instead of `read_attr_hardware`.
:::

### Static database as persistent data storage

The Tango database can (in some cases) be
used to ensure persistence of set values and to store the value as a property
(of device or attribute).

However, this practice should be reserved for special cases that don’t
require writing at high frequency. An over-solicitation of the Tango
database will penalize the entire control system.

It is therefore recommended to use a property for storage only for
methods that are performed rarely, compared to other functions.

One example is the storage of calibration operations results.

In the general case, we recommend to:

- Use a property to store configuration data,
- Use a memorized attribute to store values changing during the
  execution,
- Use a memorized attribute to store values that you want to re-inject
  during a new execution of the device.

### Device property vs memorized attributes

In some cases, you could be tempted to use a property for a {term}`memorized
attribute` and vice-versa. It is important to distinguish the function of
each, and use them wisely.

- The use of a property must be limited to configuration data which
  value doesn’t change at runtime (the IP address of equipment for
  example).

- The memorized attributes are reserved for physical quantities subject
  to change at runtime (*attribute read/write*) for which you want to
  retain (store) the value from one execution to the other.

  e.g. speed or acceleration on a motor.

:::{tip}
In the case you want to manually manage the memorization of the
attribute set points, you should use an attribute property called
`__value` (as natively done by Tango).
:::


## Device state management

### States choice

In Tango, the state is seen as an enumerated type with a
fix number of values - see the [](device-state) section for a full list of
allowed value. These states have an implicit default meaning and
are not equivalent.

Unless strictly specified, the developer is free to use the Tango
state she considers appropriate to the situation, with all the
subjectivity involved.

The only practice that ensures overall consistency is to use a limited
number of Tango states, especially for a family of equipment.

For example, it is recommended for an equipment of type motor, slit, monochromator
and more generally for any equipment that can change its position, to
use the “MOVING” state when the equipment is in “movement” toward his
set point.

### Semantics of non-nominal states

Although the developer is free to choose the device states, we must
define a common error state for all the devices.

In general, any dysfunction is associated with the state {samp}`{Tango::FAULT}`.

The use of the {samp}`{Tango::ALARM}` state should be reserved for very special
cases where it is necessary to define an intermediate state between
normal operation and fault. Its use must be documented via Pogo in order
to define the semantics.

In the case of a problem occurring at initialization, it is recommended
to set the device state to {samp}`{FAULT}`.

For the `init_device` method, we recommend:

- If the initialization method is long, thread it.
- The device state INIT must be used only in the start-up of the device.

The device states changes when the init execution is over.

Semantics recommended for {samp}`{FAULT}` and {samp}`{ALARM}` states are as follows:

- {samp}`{UNKNOWN}` (grey): communication problem with the equipment or the “sub”-devices which prevents the device to really know its real state
- {samp}`{FAULT}` (red): A problem which prevents the normal functioning (including during the initialization). Getting out from a FAULT state is possible only by repairing the cause of the problem and/or executing a Reset command.
- {samp}`{ALARM}` (orange): the device is functional but one element is out of range (bad parameters but not preventing the functioning, limit switch of a motor). An attribute is out of range.

### Managing state transitions

It is import to consider how state transitions are handled as a mis-managed
transition can cause misleading information to be transmitted to the client.

For example, consider the case of a motor system. The client can use a
*poll* (i.e. periodically read the state attribute of the motor) the motor
to get the motor state, e.g. `STANDBY, MOVING, FAULT`. This *could* lead
to inconsistent behaviour due to inappropriate management of the state.

A typical example is to launch an axis movement through the writing
of the position attribute. The motor should make the transition from
`STANDBY` to the `MOVING` state and the client will be expecting it
to be in the `MOVING` state.

However, this will only work if the device state is switched to `MOVING`
*before* the position write request returns. Otherwise, the client
could read back that the motor is still in the `STANDBY` state and
hence interpret that the move has ended even though it has not started.

This behaviour is illustrated in the figure below:

:::{figure} media/image4.jpeg
Example of State transitions
:::

:::{note}
The state transitions and the “associated guarantees” must be
documented. In the previous example, rereading the STANDBY state after
performing any movement must ensure that the required movement is
completed (and not that it has not yet been started!!).
:::


(state-machine-management)=
### State machine management

#### Pogo or developer code

Tango has a basic management of its state machine. `Is_allowed` methods
filter the external request depending on the current device state. The
developer must define the device behaviour (regarding its internal
state) via Pogo.

By default, any request (reading, writing, or command execution) is
authorized whatever the current device state is.

The example below illustrates two ways for the state machine management
of a device (here NITC01) in C++:

- Managing the “On” command via {program}`Pogo`
- Managing the reading of the attribute “temperature” directly in the
  code

:::{figure} media/image10.png
:::

:::{figure} media/image11.png
:::

However, the Pogo implementation is “basic”. If, for example, the
execution of the `On` command on a power supply is prohibited when the
current state is {samp}`{Tango::ON}`, then the Tango layer, generated by
Pogo, will systematically trigger an exception to the client. From the
operator perspective, this may be a surprise.

In such a case, it is recommended to authorize the command but to ignore
it.

#### Particular case : FAULT state

**The** {samp}`{Tango::FAULT}` **state shouldn’t prohibit everything.** The
attributes and/or commands that are valid and/or allows the device to
get out of the *Tango::FAULT* state must remain accessible.

For example, in some cases, when a device used several elementary
devices, its state is a combination of the elementary devices states. If
one of them is in “FAULT”, we must be able to execute commands on others
elementary devices, and, in all cases, have a command to get out of this
state.

The transition to a {samp}`{FAULT}` state needs reflection and a clear
definition of the device management in this state and the output
conditions of this state.

#### Init and error acknowledgement

A common mistake is to associate the generic command `MyDevice::Init` to
an acknowledgement mechanism for the current defect.

**The execution of the** `Init` **command must be reserved to the device
re-initialization** (hardware reconnection after a reboot or
reconfiguration following a property modification).

Any device that requires an acknowledgement mechanism must have a
dedicated command (like `Reset` or `AcknowledgeError`).

#### Other implementations

You can also create a specific state machine, without using Tango types,
in the interface class with the device. Thus, we use this state machine
to determine the Tango state of the device. The aims here is to define
an internal state machine (with a design pattern “state” for example)
then do a mapping with the existing Tango states to determine the device
state.

The developer also has the ability to override the {samp}`{State}` and {samp}`{Status}`
methods in order to centralize, in a unique method, the management of
the internal device state, which simplifies the update of this
fundamental information.

## Logging management

### The importance of rigorous logging management

The introduction of logging in the device code enables easy development,
debugging and the user understanding of the device operations.

The device developer must always use the facilities offered by the
*Tango Logging Service* to produce “Runtime” messages, facilitating the
understanding of the device operations. Implementations classes can
inherit `Tango::LogAdapter` to redirect the logs to the common
service.

The rules to follow are:

- Logs to the console are prohibited. The developer must use the logging
  stream proposed by Tango (there is a stream for every logging level, the
  levels being inclusive in the order specified below):
  *DEBUG_STREAM, INFO_STREAM, WARN_STREAM, ERROR_STREAM, FATAL_STREAM*
- It is important to use the right level of *logging*: on a higher
  level than DEBUG, the device should be a little wordy. Beyond the
  INFO level, it should produce only critical logs.

Recommendations of use:

- `DEBUG_STREAM`: developer information (route trace)
- `INFO_STREAM`: user information (measure, start/stop of a process)
- `WARN_STREAM`: warning (eg deprecated operation)
- `ERROR_STREAM`: general error
- `FATAL_STREAM`: fatal error, shutdown

It is important to use these *streams* early in the development as they
allow for easier debugging.

**You shouldn’t have to modify the code to add traces.** E.g. use a
`debug_stream` level for the input parameters, the display
of a conversion result, the return code from a DLL function…

It is also recommended to adopt a unified formalism for logs, for
example:

- “\<class_name>::\<method_name>() - \<text trace with parameter
  (eventually)>”

Example of using different logs levels in C++:

:::{figure} media/image12.png
:::

It is also possible to redirect the stream to a file (via Jive). This
can be useful in the case of “intermittent” bugs, for which a long log may
be required.

### Implementation

It is not mandatory, but it is highly recommended to add an attribute named
“log” in the device interface with a string spectrum type. This tracks all
the internal activity of the device (as defined in Tango Logging).

- In C++, the class `Yat4Tango::InnerAppender` implements this
  functionality based on a dynamic attribute (no need to use Pogo).
- This system facilitates the recovery of errors and therefore the
  diagnosis of problems. Problem solving will therefore be faster and optimized.
- This feature is particularly interesting for devices that
  manage automatic processes (for example, scanning) which involve other
  devices. The operator then has easy access through this “log”
  attribute to the behaviour and decisions taken by the device.

Example in C++ is shown below (look at the YAT documentation for further
explanations):

- In the header file of the device

  - Declaration of the service to use

    :::{figure} media/image13.png
    :::

- In the source code of the device

  - `init_device` method: initialization of the “innerAppender”

    :::{figure} media/image14.png
    :align: left
    :::

  - `delete_device` method: deletion of the “innerAppender”
    :::{figure} media/image15.png
    :align: left
    :::

## Error handling

### The importance of rigorous error handling

Error handling is often overlooked but good error handling means
easier debugging and maintenance. It is essential for good code quality.
These concepts are present in the section [](device-server-reporting-errors).

Below are some typical cases to avoid:

- A device doesn’t behave as expected but there is no indication why.
- The device is in {samp}`{FAULT}` state but the {samp}`{Status}` (the attribute) gives
  no indication on the problem nature, or worse, a bad indication (thus
  guiding the users in the wrong direction with a loss of time and energy).
- The error messages are written in the jargon of the developer or the
  system expert.

The developer has to ensure that:

- Any exception is caught, completed (so Tango allows it) and propagated
  using the `rethrow_exception` method,
- If an error occurs it must be logged using the Tango Logging Service
- The return code of a function is always analyzed,
- The device {samp}`{Status}` is always coherent with the {samp}`{State}`,
- The error messages are understandable for the end user and
  that they are supplemented by *logs* (*with the `ERROR` level - use of the
  `error_stream` macro*). The {samp}`{Status}` is the indicator that will help
  the user to find the reason for the error.
- All of the possible error situations are considered and handled.
  For example, in the use of communication sockets the developer should
  anticipate all the common communication problems such as a cable not
  connected, the equipment is off, a sub-devices did not start or is in
  a {samp}`{FAULT}` state.

### Implementation

On a more technical side, the Tango exceptions don’t provide numerical
identifier for discriminating exceptions. In the code, it isn’t possible
to distinguish two exceptions without having knowledge of the text (as a
string) conveyed by the said exception.

All exceptions are of type `Tango::DevFailed`. A DevFailed exception
consists of these fields:

- Reason: string, defining the error type

  - Aim: refer the **operator** to the root cause

- Description: string, giving a more precise description

  - Aim: refer the **expert** of this system to the root cause.

- Origin: string, method where the exception was thrown

  - Aim : refer the **computer scientist** to the location of the
    failure in the code

- Severity: enumeration (rarely uses)


### Standardized name for error types

To easily distinguish exceptions, it is recommended to use a finite
list of error types for the Reason field and specify in capital letters:

| **Standardized name for the error types** |
| ----------------------------------------- |
| OUT_OF_MEMORY                             |
| HARDWARE_FAILURE                          |
| SOFTWARE_FAILURE                          |
| HDB_FAILURE                               |
| DATA_OUT_OF_RANGE                         |
| COMMUNICATION_BROKEN                      |
| OPERATION_NOT_ALLOWED                     |
| DRIVER_FAILURE                            |
| UNKNOWN_ERROR                             |
| CORBA_TIMEOUT                             |
| Tango_CONNECTION_FAILED                   |
| Tango_COMMUNICATION_ERROR                 |
| Tango_WRONG_NAME_SYNTAX_ERROR             |
| Tango_NON_DB_DEVICE_ERROR                 |
| Tango_WRONG_DATA_ERROR                    |
| Tango_NON_SUPPORTED_FEATURE_ERROR         |
| Tango_ASYNC_CALL_ERROR                    |
| Tango_ASYNC_REPLY_NOT_ARRIVED_ERROR       |
| Tango_EVENT_ERROR                         |
| Tango_DEVICE_ERROR                        |
| CONFIGURATION_ERROR                       |
| DEPENDENCY_ERROR                          |
| NO_DEPENDENCY                             |


Below is an example of an exception message:

> **Reason**: DATA_OUT_OF_RANGE
>
> **Description**: {samp}`{AxisMotionAccuracy}` must be at least 1 motor
> step!
>
> **Origin**: `GalilAxis::write_attr_hardware`

The exception hierarchy defined by Tango is only available for
internal use (Tango core) and so the developer cannot inherit and define their
own inherited exceptions classes. This strong constraint is related to
the underlying CORBA IDL.

Further advice for managing exceptions:
- **Always keep the original exception.** It must be the first visible
item in the device status.
- If there is a succession of exceptions, the logic dictates that the
first exception has possibly generated all the others. By resolving the
first exception, the others can disappear.

For exception handling in `init_device` method:
- no exceptions should be propagated from the method `MyDevice::init_device`. Otherwise, **the device quits.** The device should be kept alive regardless of any failure.
- The code for this method must contain a try/catch block, which guarantees that no exception is propagated in this context.
- If an exception is thrown, the developer must set the device state to {samp}`{FAULT}` and update the {samp}`{Status}` to indicate the error nature. (*The goal is to understand easily why the device failed to initialize properly, while still allowing the operator to adjust this or these problems*)

Examples of error handling in C++:
- If an error occurs, always log it
- Always update *State* **AND** *Status*
- Manage the return code for function that have one
- Manage the exceptions for methods which can throw some

:::{figure} media/image16.png
:::

### Details for an attribute

Although Tango supports the notion of quality on an attribute value
({samp}`{Tango::VALID}`, {samp}`{Tango::INVALID}`, ...), only few clients use this
information to judge the validity of the data returned so it is best to not make
assumptions on the use of this to report an invalid value to the client. That is
to say that **forcing the attribute quality to {samp}`{Tango::INVALID}` is necessary
but not sufficient.**

For floating point values, it is possible to set the value to “NaN”, but there is
no equivalent for an integer. To avoid the handling of special cases, it
is recommended to throw an exception to indicate the data invalidity.

It is recommended to throw an exception for all invalid values,
regardless of their type. There is, however, two exceptions to this
rule: State and Status. For these two attributes, always return a value.

This solution has the disadvantage of showing a pop-up on the client side,
but this is the most effective method to indicate that the attribute
reading has failed.

### Details for the properties

#### Properties reading during device initialization

As it stands, the code generated by {program}`Pogo` doesn’t wrap the method
which ensures the reading of properties from the Tango database in a try/catch
block (see `MyDevice::init_device`). However, it may fail and cause
the generation of an exception. As mentioned above, the developer must
ensure that any exception thrown in the `init_device` method (or a
method called from it) is caught and **not propagated**.

In the case of a Tango exception during the {term}`properties <property>` reading, the developer
should systematically:

1. detect the error (catch it).
2. log it with level `ERROR`.
3. set the device to the `FAULT` state.
4. update the Status indicating the origin of the problem.

Example in C++ :

:::{figure} media/image17.png
:::

As a reminder, the default value for a property is defined with Pogo and
the value is stored in the database via the `put_property()` method.

#### Properties without default values

{program}`Pogo` allows a default value for a {term}`property` not present in the
Tango database to be defined.

For mandatory properties that have no default values, the developer
should systematically:

- detect the absence of the value in the database.
- log the problem explicitly with the level `ERROR` (indicate the
  missing property).
- set the device to the `FAULT` state.
- update the Status indicating the problem origin.

# Appendices

## About these guidelines

These guidelines originated within the collaborative framework
between SOLEIL and MAX-IV to define common software quality rules for
shared software between these 2 institutes. It has since been adopted by
the Tango Controls community and is maintained for and by the community.

The objectives are therefore to enhance the general software quality of
Device Servers developed by the various sites using Tango. This will
also facilitate the reusability of code between sites by providing
“reliable off-the-shelves” Tango servers in public repositories.

This document can be freely distributed (under the
Creative Commons license) to subcontractors, students, etc...

:::{note}
The content of this document is generally
independent of the programming language used. However, there are some
“C++ oriented” recommendations. For Java and Python refer to the relevant
documentation for language specific issues.
:::
