(tango-admin)=

# Tango Admin utility

%[glossary_term][tango_admin]
%Command line utility for administrative tasks related to the {term}`TangoDB`

```{tags} audience:administrators
```

The Tango Database can be maintained using a command-line interface with the {term}`tango_admin` tool.

The following features are available:

- Ping the {term}`tango database server <TangoDB>`
- Check if a {term}`device`/{term}`device server` is defined
- Create/Delete a server
- Create a {term}`property`
- List server/devices
- Unexport devices

## Tango Admin help

```bash
tango_admin --help
```

Output:

```text
Usage:
 --help  		Prints this help
 --ping-database	[max_time (s)] Ping database
 --check-device <dev>    Check if the device is defined in DB
 --check-device-exported <dev>    Check if the device is exported in DB
 --add-server <exec/inst> <class> <dev list (comma separated)>   Add a server in DB
 --delete-server <exec/inst> [--with-properties]   Delete a server from DB
 --check-server <exec/inst>   Check if a device server is defined in DB
 --server-list  Display list of server names
 --server-instance-list <exec>   Display list of server instances for the given server name
 --add-property <dev> <prop_name> <prop_value (comma separated for array)>    Add a device property in DB
 --delete-property <dev> <prop_name>   Delete a device property from DB
 --tac-enabled Check if the TAC (Tango Access Control) is enabled
 --ping-device <dev> [max_time (s)] Check if the device is running
 --ping-network [max_time (s)] [-v] Ping network
 --unexport-device <dev> Unexport a device from DB.  USE WITH CARE.
```
This is the output of version 1.24.

## Examples

(tango-admin-add-device-server)=

### Adding a device server

```text
# For python this is the device server source file name without `.py` extension,
# for C++ this is the executable name
executable=fancyMotor

class=fancyMotorClass

instance=1
device=vacuum/innerCircle/valve1

tango_admin --add-server "${executable}/${instance}" $class $device
```

### Adding a device server property

```text
device=vacuum/innerCircle/valve1

tango_admin --add-property $device RemotePort 127.0.0.1
```

### Checking if a device server is alive

```text
tango_admin --check-device sys/database/2
```

### Checking if a device server is exported

```text
tango_admin --check-device-exported sys/tg_test/1
```
