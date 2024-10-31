# Explanation

{audience}`all`

```{toctree}
:maxdepth: 2
:name: explainationtoc
:hidden: true

overview.md
simplified-data-model.md
data-model.md
history.md
deviceserver.md
attribute-alarms.md
archiving/index.md
attribute.md
command.md
development/index.md
device.md
event.md
pipe.md
polling.md
property.md
tangodb.md
rest-api.md
long-term-support.md
threading
naming
tangodb.md
```

Tango Controls is a toolkit for building distributed object based control systems.
Distributed objects are an implementation of the [Actor model](https://en.wikipedia.org/wiki/Actor_model).
Actors are primitives of concurrent computation which were proposed in the 70s
but have gained renewed interest with massively parallel architectures, IoT, cloud computing etc.

The distributed object in Tango Controls is called a {term}`device` and is
created as an object in a container process called a {term}`device server`.
The device server implements the network communication and links to the
configuration data base and clients.
Tango device servers and clients can be written in Python, C++ or Java.
Tango comes with a full set of tools for developing, supervising, monitoring and archiving.

The Tango Controls toolkit has been used to build the control systems of large
and small physics experiments like synchrotrons, lasers, wind tunnels and radio telescopes.
Tango can be used for a single device which requires remote control in a lab
or on the internet.
Tango can be used as a communication protocol for controlling anything remotely.
Tango is ideal for connecting things together and its uses are only limited by your imagination!

```{image} index/Ready.jpg
```

We are glad you are with us. Please have a look of all the in-depth explanation of Tango in the next pages.
