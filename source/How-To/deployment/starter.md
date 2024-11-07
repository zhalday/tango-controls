(starter)=

# The Starter device

{audience}`all`

## Introduction

The Starter device can be used to control other device servers running
on the same host.

Possible use cases are:

- start all device servers on system startup,
- get list of all started device servers,
- start or stop a device server,
- get logs from a device server.

[Astor](#introduction to astor) is a graphical client for Starter devices.

## Installation

There are several ways to install the Starter device server:

- [as a part of Tango source distribution](#debian-compile-tango-source-distribution),
- [from Starter source](https://gitlab.com/tango-controls/starter),
- [using a package manager ](#linux-debian-installation)
  (e.g. [tango-starter for debian](https://packages.debian.org/buster/tango-starter)),

## Configuration

General recommendations for Starter configuration:

- there should be only one instance of a Starter device server running on a host,
- the instance name can be arbitrary,
- the Starter device server provides a *Starter* class,
- the *member* part of a Starter device name must match the short name
  of the host.
- the *domain/family* part of a Starter device name should be
  "tango/admin" in order for the Starter device to be detected by Astor.

An example how to define Starter device using *tango_admin* tool:

```bash
host=$(hostname -s)
tango_admin --add-server Starter/$host Starter tango/admin/$host
Starter $host
```

:::{note}
The requirement for *member* part of the name to match the hostname
can be disabled by setting environment variable `DEBUG` to `true`.
The starter will be visible in Astor under the name specified in *member*.
:::

## Usage

The Astor GUI can be used to
[start a new Tango device server](inv:astor:std#add_server)
using the Starter device.

Alternatively, the Starter interface can be used directly, e.g. to start
a device server:

```python
import tango
starter = tango.DeviceProxy("tango/admin/tangobox")
starter.command_inout("DevStart", "TangoTest/test")
```

The Starter device will use the paths from the `StartDsPath` property
when looking for an executable of a device server to start. The paths are
searched in the order in which they appear in the property.
If the property is empty, Starter device server's working directory is used
when searching for executables.

## Autostarting Starter

The Starter device server can be automatically started during system startup
using a service manager of choice. It can then start any other device servers.

Following are example configuration files for different service managers.

### systemd

Follow [instructions for systemd integration ](#systemd-integration).

### System V init

Follow [instructions in the installation guide ](#howto-sysv-init).

### NSSM (Windows)

Follow [NSSM configuration instructions in the installation guide for Windows ](#windows-starter-nssm).

## References

- [Starter documentation](http://www.esrf.fr/computing/cs/tango/tango_doc/ds_doc/tango-ds/System/starter/index.html),
- [Starter in the Device Servers Catalogue](https://www.tango-controls.org/developers/dsc/ds/423/),
- [Starter source code repository](https://github.com/tango-controls/starter).
