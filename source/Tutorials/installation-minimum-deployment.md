(tutorial-deployment)=

# Example deployment of a Tango Controls System

```{tags} audience:administrators, audience:developers
```

There are different tasks that need to be performed in a Tango Cotnrols System. One can categorise the tasks as follows:

- {term}`Tango Host <tango host>`: Keep the configuration of all components in the Tango Controls system permanently stored and make it available through its [API](#tangodb-explanation).
- Run Tango Applications: Execute CLI programmes. e.g.{program}`tango_admin` and {program}`iTango`, or GUI programmes, e.g. {program}`Jive` and {program}`Synoptic`.
- Run Tango {term}`Device Server(s) <device server>`: Execute the Tango Device Server that host Tango {term}`Devices <device>`.
- Tango development: Implement {term}`Device Classes <device class>` for Tango Devices and Tango {term}`clients <client>`.

:::{tip}
It is possible that all of the tasks above are done on the same computer at the same time.
:::

:::{hint}
**Tango Host, Databaseds**

In order to allow clients to connect to components in a Tango Controls system, i.e. connect to Tango {term}`Tango device servers <device server>` and their {term}`Tango devices <device>`, such a system needs to have at least one {term}`Tango Host <tango host>`. The `Tango Host`'s responsibility is maintain a catalog of the Tango `device servers` and `devices` that have been configured to run in the system. A `Tango Host` typically runs the {term}`DataBaseds <databaseds>` `device server`. This `device server` provides the configuration information about the Tango Controls system to the `device servers`, `devices` and clients in the system. Usually clients will make use of the {term}`TANGO_HOST` environment variable which contains information about the host name or IPv4 address and the port on which the `Databaseds` is listening. The `TANGO_HOST` environment variable consists of a host and a port part, spearated by a column:

*host_name_or_IPv4_address:port*, example: `localhost:10000`
:::

Simple Tango Controls systems can consist of just a single computer that acts as `Tango Host` and runs at the same time only one or a few `device servers` with only a couple `devices`. A complex system on the other hand can easily consist of tens of thousands of `device servers` and their`devices` that are spread out over multiple Tango Controls systems, each with their own `Tango Host` but still allowing clients to connect to every `device` in every individual Tango Controls system.

## Tango Host Role

The central role of a Tango control system is Tango Host role, it is created by running the `DataBaseds` `device server`. This `device server` needs either a MariaDB or a MySQL database backend to act as permanent storage for the `device server`.

The recommended way of running device servers is to use the [Starter](#Starter) service.

- a Database server (MariaDB or MySQL)

:::{warning}
root password for database can be different from the computer root password.
This password should not be empty. tango database password for tango database can be empty.
:::

- an official Oracle Java JRE (Java Runtime Environment) >= 1.7
- a Tango database. It will ask for a port number, this port will be the one used by the server for Tango requests. The hostname has then to be known from all the computers which will access to Tango Host. It is mandatory to install this tango database **before** every tango client.

## Tango development Role

This role is to develop applications and device servers.
To play this role, you need:

- the libtango headers for development
- pytango to allow accessing Tango through Python
- an official Oracle Java JRE (Java Runtime Environment) >= 1.7 for development with Java

## Tango applications Role

This role is to run CLI and GUI applications.
To play this role, you need:

- an official Oracle Java JRE (Java Runtime Environment) >= 1.7 for Java applications
- the libtango java tools (astor, atkpanel, jive, pogo, etc.)
- pytango to allow accessing Tango through Python (if using Python device servers)

## Tango device servers Role

This role is to run device servers (drivers):
The recommended way of running device servers is to use {program}`Starter` service.

To play this role, you need:

- a Tango Starter service
- a TangoTest device server to allow testing
- an official Oracle Java JRE (Java Runtime Environment) >= 1.7 for Java device servers

## Every roles

Whatever the role, every computer needs:

- the libtango offline documentation

- the liblog4j package for logging

- to set an environment variable `TANGO_HOST` to the Tango Host and the port, for example

  ```console
  TANGO_HOST=mycomputer:10000
  ```

  `mycomputer` is the hostname on which is installed Tango Host, and `10000`
  is the port defined during the installation of Tango database.

:::{warning}
The choosen port should be defined according to network rules and it should
especially be compatible with authorized ports.
:::

## Single computer

Installing Tango on a single machine means all roles described above (Tango Host, Tango applications, Tango device servers, Tango development) will be played by the same computer.

The software needed are described in each role.

In this installation type, a `TANGO_HOST` environment variable has to be set to `TANGO_HOST=HOSTNAME:PORT` where HOSTNAME is the name of the computer and PORT is the port on which the server will wait for requests. This will be used to send Tango request.
This `TANGO_HOST` environment variable should be loaded at each startup.

## Multiple computers

When installing several computers, one should install one Tango host and some clients computers.

Those clients can play different roles (Client computers, Device servers running, and Development).

Moreover, it is possible to start several Tango Host within the same Tango control system in order to keep the control system working if one of them dies.
This configuration is described in section [Multiple database servers within a Tango control system](#multiple-db-hosts).

## Multiple control systems

Several Tango control systems can be used.
It means every Tango control systems will have its own Tango Host which will store its own device servers configuration.

In this environment, Tango Host and Tango clients installation is the same as described upside, but `TANGO_HOST` environment variable has to be set on each client according to which server will be used for device servers configuration.
The hostnames of the Tango Hosts have then to be known from all the computers which will access to them.

For example, if `testserver` and `productionserver` have been installed as Tango Hosts, each one will propose Tango database as a service, and client can be configured as followed:

- testclient1 with `TANGO_HOST=testserver:10000`
- testclient2 with `TANGO_HOST=testserver:10000`
- operatorclient with `TANGO_HOST=productionserver:10000`
- developerclient with `TANGO_HOST=productionserver:10000`
- dsclient with `TANGO_HOST=productionserver:10000`

In this configuration, one can decide to change `TANGO_HOST` value on a client to use another server. However, this will need to restart every device running on this client.

## No database

It is possible to run a device server on some computer without a Tango database.

:::{warning}
A configuration without SQL database can be useful for testing purpose. However, it will not benefit the major part of the Tango functionnalities.
:::

See section [Running a device server without SQL database](#device-server-without-database) to understand how to use this configuration and what are the limitations.
