(device-server-with-filedatabase)=

# Run a device server with the File Database

```{tags} audience:administrators, audience:developers
```

%[glossary_term][File Database]
% The File Database is a lightweight, file-based alternative for the {term}`Tango Database` for testing
% purposes and single device server setups.

For device servers not able to access the {term}`Tango Database` (most of the time due to network route or security
reasons) or just because it is more convenient for testing, it is possible to start device servers using a file
instead of a real Tango database.

The File Database has the following limitations:

- There's no check that the same device server is running twice
- There's no device or attribute alias name support
- If several device servers are running on the same host, the user
  must manually manage a list of network ports already in use

To use the File Database, pass the following command line option to the device server:

`-file=<file name>`

In this case the getting, setting and deletion of all properties are handled using the specified file instead of
the Tango database. The file is a plaintext file and follows a well-defined syntax with predefined keywords
and is called a [property file](#property-file-syntax). The simplest way to generate the file for a specific device
server is to use [Jive](inv:jive:std#index).

The Tango database is not only used to store device configuration parameters, it is also used to store device
network access parameters, for example the {term}`Interoperable Tango Reference`. Therefore to allow an
application to connect to a device hosted by a device server using a file instead of the standard database,
you need to start it on a pre-defined port using one of the underlying ORB options called *endPoint*. For example, to start your device server:

`myserver myinstance_name -file=path/serverFile -ORBendPoint giop:tcp::<port>`

Assuming the device `id12/rb/1` runs on host `fish` with port `1234`, clients can then connect to it via the {term}`Tango Resource Locator (TRL) <Tango Resource Locator>`:

```text
tango://fish:1234/id12/rb/1#dbase=no
```
