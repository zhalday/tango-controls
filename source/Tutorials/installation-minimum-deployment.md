(tutorial-deployment)=

# Example deployment of a Tango Controls System

```{tags} audience:administrators, audience:developers
```

There are different tasks that need to be performed in a Tango Cotnrols system. One can categorise the tasks as follows:

- {term}`Tango Host <tango host>`: Keep the configuration of all components in the Tango Controls system permanently stored and make it available through its [API](#tangodb-explanation).
- Run Tango Applications: Execute CLI programmes. e.g.{program}`tango_admin` and {program}`iTango`, or GUI programmes, e.g. {program}`Jive` and {program}`Synoptic`.
- Run Tango {term}`Device Server(s) <device server>`: Execute the Tango Device Server that host Tango {term}`Devices <device>`.
- Tango development: Implement {term}`Device Classes <device class>` for Tango Devices and Tango {term}`clients <client>`.

:::{tip}
It is possible that all of the tasks above are done on the same computer at the same time.
:::

:::{hint}
**Tango Host, Databaseds**

In order to allow clients to connect to components in a Tango Controls system, i.e. connect to Tango {term}`Tango device servers <device server>` and their {term}`Tango devices <device>`, such a system needs to have at least one {term}`Tango Host <tango host>`. The `Tango Host`'s responsibility is maintain a catalog of the Tango `device servers` and `devices` that have been configured to run in the system. A `Tango Host` typically runs the {term}`DataBaseds <databaseds>` `device server`. This `device server` provides the configuration information about the Tango Controls system to the `device servers`, `devices` and clients in the system. Usually clients will make use of the {term}`TANGO_HOST` environment variable which contains information about the host name or IPv4 address and the port on which the `Databaseds` is listening. The `TANGO_HOST` environment variable consists of a host and a port part separated by a column:

*host_name_or_IPv4_address:port*, example: `localhost:10000`
:::

Simple Tango Controls systems can consist of just a single computer that acts as `Tango Host` and runs at the same time only one or a few `device servers` with only a couple `devices`. A complex system on the other hand can easily consist of tens of thousands of `device servers` and their`devices` that are spread out over multiple Tango Controls systems, each with their own `Tango Host` but still allowing clients to connect to every `device` in every individual Tango Controls system.

## Starter

Having to start many `device servers` in a larger Tango Controls system can turn into a laborious task that takes much longer than one would want it to. Fortunately Tango comes with some batteries included and it provides the [Starter](#Starter) `device server`. One can think of it as a boot-strapping device server that is able to start and stop other device servicers on the same host. Usually one puts `Starter` under control of one of the init systems of the OS.

## Example for a very small installation

Here we give an example for a very small installation:

- A `Tango Host`. It will require a port number on that host which will be used by `Databaseds` for Tango requests. The hostname needs to be resolveable by all computers that run Tango software in this Tango Controls system or the host's IP address needs to be known by the same computers. It is mandatory to start the `Databaseds` **before** any other Tango program.
- A different computer on which a cppTango, JTango or PyTango `device server` will run. On the same computer can also run clients.
- - On that computer:
- - - cppTango and/or JTango and/or PyTango
- - - Oracle Java JRE (Java Runtime Environment) >= 1.7 to run Tango's Java tools or JTango code.
- - - Python >= 3.9 in order to run PyTango (clients or `devices` and `device servers`).

:::{note}
An even smaller Tango Controls installation could even be a single computer. One could run everything on it. `Device servers` with their `devices`, the `TangoDB` and even JTango GUIs or PyTango clients.
:::

## Multiple Tango Controls systems

Tango makes it easy to bridge the apparent boundary betweeen Tango Controls systems. This boundary exists because every individual Tango Controls system will always have its own `TangoDB` that manages the `device servers` and `devices`. But clients can easily cross this boundary. One just needs to address a `device` or `attribute` by its full {term}`Tango Resource Locator (TRL)<Tango Resource Locator>`.

## No database

It is possible to run a `device server` on without a {term}`TangoDB`. This can come handy for very small deployments that do not require the entire set of Tango functionality or when one wants to test something. Running a Tango system without a `TangoDB` is not advised.

:::{warning}
Running a Tango system without a `TangoDB` can be useful for testing purposess. However, the lack of a TangoDB will remove core functionality of Tango.`
:::

See section [Running a device server without SQL database](#device-server-without-database) to understand how to use this configuration and what the limitations are.
