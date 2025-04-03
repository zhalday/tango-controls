% This is file to keep glossary
% Glossary terms can also be added in the section that they refer to and will be picked up during
% the automated generation of the glossary during 'make html'.
%
% To add a glossary definition in place put '%[glossary_term][<term_name>]' on the line above the
% glossary description.
%
% E.g. To add a Hello World definition:
%    %[glossary_term][Hello World]
%    %A standard greeting in programming
%
% Note: removing the '%' in front of the definition will mean the definition is also displayed
%       within that section if this is desired.

(glossary)=

# Glossary

```{tags} audience:all
```

```{glossary}
:sorted:

Tango Core
  Tango Core is a set of main tools, libraries and specifications of the Tango Controls framework. It consists of libraries and API definitions for C++, Java and Python as well as tools to manage the system: [Astor](#astor-manual), [Jive](inv:jive:std#index), etc.

SCADA
  It is an abbreviation standing for Supervisory Control and Data Acquisition.

attribute quality
  A value returned by an {term}`attribute` has a runtime quality factor which is an enumeration describing
  the state of the read value (one of VALID, INVALID, ALARM, CHANGING, WARNING).

dynamic attribute
  A {term}`device` may create attributes for which the configuration is determined during device initialization or even at runtime. This kind of attributes is called *dynamic*.

device state
  A {term}`device` may be in a certain state which is determined at runtime. The state of a {term}`device` may reflect the state of a piece of equipment it interfaces with or be determined in another way. The behaviour is defined by the {term}`device class` which implements a {term}`state machine`. The state may define attributes', commands' and  pipes' operations available at that moment. Tango Controls has a set of allowed states the device may be in; these are: ON, OFF, CLOSE, OPEN, INSERT, EXTRACT, MOVING, STANDBY, FAULT, INIT, RUNNING, ALARM, DISABLE, and UNKNOWN.

state machine
  A state machine for a {term}`device class` defines the operations (commands', attributes' and pipes' access) available in different {term}`states <device state>` of a {term}`device`.

Tango Host
  Each Tango Controls system/deployment has to have at least one running DataBaseds {term}`device server`.
  The machine on which DataBaseds {term}`device server` is running has the role of a so called {term}`Tango Host`.
  *DataBaseds* is a device server providing configuration information to all other components of the system as
  well as a runtime catalog of the components/devices. It allows (among other things) client applications to find
  devices in distributed environment.

CORBA
  The underlying technology for network operations is [CORBA](https://en.wikipedia.org/wiki/Common_Object_Request_Broker_Architecture).
  This software package allows Tango to work with multiple programming languages as the network interface itself is
  defined in a markup language from which the code is generated from. For Tango the interface is defined in the
  [tango-idl](https://gitlab.com/tango-controls/tango-idl) repository.

Interoperable Tango Reference
  Unique identifier for referencing remote device servers, based on the {term}`CORBA` [IOR](https://en.wikipedia.org/wiki/Interoperable_Object_Reference)

tangorc
  Tango configuration file holding various settings in the format `key=value`. This can be created globally in
  `/etc/tangorc` for unix-like OSes and in `${TANGO_ROOT}/tangorc` for Windows. Or for the current user only
  in `~/.tangorc` for unix-like OSes (not available for Windows). Environment variables with the same name
  override the entries from the files and the per-user file overrides the gobal one.
```
