# CORBA

```{tags} audience:developers, lang:all
```

Below are the 10 important things you should know about CORBA. More detail is provided [below](corba-intro) for those that are interested.

01. **You don’t need to know {term}`CORBA` to work with TANGO**
02. CORBA is the acronym for **C**ommon **O**bject **R**equest **B**roker **A**rchitecture and it is a standard defined by the [Object Management Group (OMG)](http://www.omg.org)
03. CORBA enables communication between software written in different languages and running on different computers
04. CORBA applications are composed of many objects; objects are running software that provides functionalities and that can represent something in the real world
05. Every object has a type which is defined with a language called IDL (Interface Definition Language)
06. An object has an interface and an implementation: this is the essence of CORBA because it allows *interoperability*.
07. CORBA allows an application to request an operation to be performed by a distributed object and for the results of the operation to be returned back to the application making the request.
08. CORBA is based on a *Remote Procedure Call* model
09. The TANGO Device is a CORBA Object
10. The TANGO Device Server is a CORBA Application


(corba-intro)=

## An introduction to CORBA

{term}`CORBA` is a definition of how to write object request brokers (ORB). The
definition is managed by the Object Management Group ([OMG home page]).
Various open-source and proprietary implementations exist for CORBA for nearly all operating systems.
CORBA uses a programming language independent definition language (called the IDL) to define network object
interfaces. Language mappings are defined from IDL to a variety of programming languages e.g. C++, Java, C, Python.
Within an interface, CORBA defines two kinds of actions available to the outside world.
These actions are called `attributes` and `operations`.

`Operations` are all the actions offered by an interface. For instance,
within an interface for a Thermostat class, operations could be the
action to read the temperature or to set the nominal temperature.

An `attribute` defines a pair of operations a client can call to send or
receive a value. For instance, the position of a motor can be defined as
an attribute because it is data that you only set or get. A read-only
attribute defines a single operation the client can call to receive a
value. In case of error, an operation is able to throw an exception to
the client, attributes cannot raises exception except system exception
(due to a network fault for instance).

Intuitively, the IDL interfaces correspond to C++ classes and the IDL operations
correspond to C++ member functions and attributes as a way to read/write
public member variables. Nevertheless, the IDL only defines the interface to
an object and says nothing about the object implementation. The IDL is only a
descriptive language. Once the interface is fully described in the IDL
language, a compiler (from IDL to C++, from IDL to Java...) generates
code to implement this interface. Obviously, you still have to write how
operations are implemented.

The act of invoking an operation on an interface causes the ORB to send
a message to the corresponding object implementation. If the target
object is in another address space, the ORB runtime sends a remote
procedure call to the implementation. If the target object is in the
same address space as the caller, the invocation is accomplished as an
ordinary function call to avoid the overhead of using a networking
protocol.

For the curious the tango-idl file is available [here](https://gitlab.com/tango-controls/tango-idl/-/blob/main/include/tango.idl?ref_type=heads).
