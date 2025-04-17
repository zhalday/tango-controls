```{tags} audience:administrators
```

(access-control)=

# Use the Tango controlled access system

%[glossary_term][Tango Access Control]
%A device server that manages user's rights to perform read/write requests
%on a particular device.

## User rights definition

Within the Tango control system, you give rights to a user. The 'user' is
the name used to log in to the computer where the application
trying to access a device is running. There are two kinds of users within
the Tango control system:

1. Users with defined rights
2. Users without any rights defined in the control system. These
   users will have the rights associated with the pseudo-user called *All
   Users*

The control system manages two kinds of rights:

- Write access: all types of requests are allowed on the
  device
- Read access: only read access is allowed meaning that
  *write_attribute*, *write_read_attribute* and *set_attribute_config*
  network calls are forbidden. Executing a command is also forbidden
  except for commands defined as **Allowed commands**. Getting a device
  state or status using the `command_inout` call is always allowed. The
  definition of the allowed commands is done at the device class level.
  Therefore, all devices belonging to the same class will have the same
  *allowed commands* set.

The rights given to a user are determined from checks at two levels:

1. At the host level: You define from which hosts the user may have
   write access to the control system by specifying the host name. If
   the request comes from a host which is not defined, the right will be
   read access only. If nothing is defined at this level for the user, the
   rights of the *All Users* user will be used. It is also possible to
   specify the host by its IP address. You can define a host family
   using wildcards in the IP address (eg. 160.103.11.\* meaning any host
   with an IP address starting with 160.103.11). Only IP V4 is supported.
2. At the device level: You define on which device(s) request are
   allowed using the device name. Device families can be specified using wildcards
   in the device name like *domain/family/\**

The control system is doing the following checks when a
client try to access a device:

- Get the user's name

- Get the host IP address

- If rights are defined at the host level for this specific user and this IP
  address then give the user temporary write access to the control system

- If nothing is specified for this specific user on this host, give
  the user temporary access rights equal to the host access rights of
  the *All User* user.

- If the temporary right given to the user is write access to the
  control system then check what rights are defined at the device level:

  - If there is a right defined for the device to be accessed (or
      for the device family), give user that defined right

  - Otherwise if no right is defined at the device level for this user then check:

    - If rights are defined for the *All Users* user for this device,
        give this right to the user
    - Otherwise, give the user read Access only for this device

- Otherwise the default access right will be read Access

Then, when the client tries to access the device, the following
algorithm is used:

- If right is read access

  - If the call is a write type call, refuse the call

  - If the call is a command execution

    - If the command is one of the command defined in the *allowed
      commands* for the device class, send the call
    - Else, refuse the call

All these checks are done during the DeviceProxy instance constructor
except those related to the device class *allowed commands* which are
checked during the `command_inout` call.

To simplify the rights management, give the *All Users* user host access
right to all hosts (.\*.\*.\*) and read access to all devices (/\*/\*).
With such a set-up for this user, each new user without any rights
defined in the control access will have only read access to all
devices on the control system from any hosts. Then, on request,
gives write access to specific user on specific host (or family) and on
specific device (or family).

The access rights are managed using the Tango
[Astor](inv:astor:std#index) tool which provides a graphical interface
to grant/revoke user rights and to define device class *allowed
commands* set. The following screenshot shows an example of the Astor window:

```{image} access-control/control.png
:alt: access-control
```

In this example, the user *taurel* has write access to the device
*sr/d-ct/1* and to all devices belonging to the domain *fe* but only from
the host *pcantares*. They have read access to all other devices but always
only from the host *pcantares*. The user *verdier* has write access to the
device *sys/dev/01* from any host on the network *160.103.5* and Read Access
to all the remaining devices from the same network. All the other users
have read access only from any host.

## Running a Tango control system with the controlled access

All the users rights are stored in two tables of the Tango database. A
dedicated device server called **TangoAccessControl** accesses these
tables without using the classical Tango database server. This
TangoAccessControl device server must be configured with only one
device. The property **Services** belonging to the free object
**CtrlSystem** is used to run a Tango control system with controlled
access. This property is an array of strings with each string describing
the services running in the control system. For controlled access, the
service name is *AccessControl*. The service instance name has to be
defined as *tango*. The device name associated with this service must be
the name of the TangoAccessControl server device. For instance, if the
TangoAccessControl device server device is named
*sys/access_control/1*, one element of the Services property of the
CtrlSystem object has to be set to: *AccessControl/tango:sys/access_control/1*.

If the service is defined but without a valid device name corresponding
to the TangoAccessControl device server, all users from any host will
have write access (simulating a Tango control system without controlled
access). Note that this device server connects to the MariaDB database and
therefore may need the MariaDB connection related environment variables
`MYSQL_USER` and `MYSQL_PASSWORD` - see [database environment variables](reference-env-var-db).

Even if a controlled access system is running, it is possible to by-pass
it if, in the environment of the client application, the environment
variable `SUPER_TANGO` is defined to true. If for one reason or another,
the controlled access server is defined but not accessible, the device
right checked at that time will be read access.
