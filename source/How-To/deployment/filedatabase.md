(device-server-with-filedatabase)=

# Running a device server with using the FileDatabase

```{tags} audience:administrators, audience:developers
```

%[glossary_term][File database]
% TODO

For device servers not able to access the Tango database (most of the
time due to network route or security reason), it is possible to start
them using file instead of a real database. This is done via the device
server

-file=\<file name>

command line option. In this case,

- Getting, setting and deleting class properties
- Getting, setting and deleting device properties
- Getting, setting and deleting class attribute properties
- Getting, setting and deleting device attribute properties

are handled using the specified file instead of the Tango database. The
file is an ASCII file and follows a well-defined syntax with predefined
keywords. The simplest way to generate the file for a specific device
server is to use the [Jive tool](inv:jive:std#index).
The Tango database is not only used to store
device configuration parameters, it is also used to store device network
access parameter (the CORBA IOR). To allow an application to connect to
a device hosted by a device server using file instead of database, you
need to start it on a pre-defined port, and you must use one of the
underlying ORB option called *endPoint* like

myserver myinstance_name -file=/tmp/MyServerFile -ORBendPoint
giop:tcp::\<port number>

to start your device server. The device name passed to the client
application must also be modified in order to refect the non-database
usage. See [device naming ](#tango-object-naming) to learn about Tango device name syntax.
Nevertheless, using this Tango feature prevents some other features to
be used :

- No check that the same device server is running twice.
- No device or attribute alias name.
- In case of several device servers running on the same host, the user
  must manually manage a list of already used network port.
