(getting-started)=
# Getting Started

```{tags} audience:all, lang:all
```

In this section we will guide you step-by-step to help you getting started with Tango-Controls.

## First steps
Some first steps might include:
- Reading through the {doc}`Overview </Explanation/overview>` section will provide you with the basic information on Tango Controls. It will help you understand some of the key concepts behind Tango Controls.

- Start with either a preconfigured virtual machine or try installing a basic Tango controls set up on your own computer - see [trying Tango Controls ](#howto-try-tango).

- Installing Tango Controls on your own system following instructions from the [Installation guides ](#getting-started-installation).

- Start connecting your devices to Tango Controls :
    - browse the [Device Classes Catalogue](http://www.tango-controls.org/developers/dsc/) to find device servers
    for your equipment
    - read [how to start a device server ](#howto-start-device-server)
    - or read {doc}`../development/cpp/first-device-class` and follow a guide [How to write your device class ](#how-to-write-first-device-class) if your device is not yet supported by any existing {term}`device server`.

- Writing your first client following instruction from {doc}`../development/general/first-client`.

- Learn how to use some of the tools provided in Tango:
    - [Jive](inv:jive:std#index)
    - [ATKPanel](#atkpanel-manual)
    - [Astor](#astor-manual)
    - [JDraw](#jdraw-manual)
    - [Pogo](#pogo-documentation)

- Explore the content of the [Tango Controls web page]

% • what is necessary to have a minimum tango control system on a single machine or on several hosts sharing a single tango database, etc...

% • how and what to install it on a single machine, on a set of machine sharing the same database server.

% • How to try it.

% • Integrating exiting device servers, declaring classes in device servers, declaring devices, running several instances...

% • Playing with generic tools.

% • How to develop your own device class.

% • How to make a device server from one or several device classes

## Specific how to guides
```{toctree}
:maxdepth: 1
:caption: How to:

how-to-try-tango
end-user-apps
how-to-start-device-server
```

[Tango Controls web page]: https://www.tango-controls.org
