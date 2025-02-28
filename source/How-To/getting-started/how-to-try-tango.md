(howto-try-tango)=

# How to try Tango Controls

```{tags} audience:developers, audience:all
```

There are several ways to try the Tango Controls System.

For a first quick look, you can download and run the [TangoBox Virtual Machine](#tangobox-vm-installation).
Alternatively, you can go ahead and install Tango on your system - see the [installation section](#getting-started-installation)
for a full set of instructions on how to do this on your chosen operating system.

It may also be worth looking at configuring the Tango components to run as services using systemd to automate the start up, please see [](#systemd-integration).

Assuming you have installed and configured Tango you can begin to use it.

(using-tango)=

## Play with Tango Controls

The Tango eco-system provides a lot of management applications and frameworks to visualize the data.
This section provides a quick overview of a basic use case for Tango Controls.

If you have set up a tango-starter systemd service then it will automatically add the new host,
however this can also be done manually using [**Astor**](#astor-manual).
This application is used to configure the Control System and its components.
It also provides a quick view of the statuses of all {term}`device servers<device server>` in the Tango DB.
To add a new host manually using Astor see: {ref}`astor-new-host`.

TangoTest this is a {term}`device class` that provides all types of attributes available in Tango Devices
and so can be used for testing purposes. Astor can be used to start this device server.
After opening the control panel for the specific host, you can start a new device server, e.g.:

:::{figure} how-to-try-tango/astor-tangotest.png
:align: center
:scale: 75 %
:::

Tango Starter also needs to be running. Further information is available on [starting a new Tango device server in Astor](inv:astor:std#add_server).

We can the open the [AtkPanel](#atkpanel-manual) from the [Jive](inv:jive:std#index) application
and view the attributes, properties, and all configuration settings for the selected device.

Open the Jive application by typing the command `jive` in a console. Then select the
{guilabel}`Monitor Device` option from the right-click menu on that {term}`Tango Device <device>`, e.g.:

:::{figure} how-to-try-tango/jive-tangotest.png
:align: center
:scale: 75 %
:::

Users can use the AtkPanel to [execute commands](#device-testing) on the selected TangoTest device.
Some useful commands one might try issuing for this device are:

- `SwitchStates` - changes the state of the device (e.g. from RUN to FAULT or FAULT to RUN)
- `DevType` - this is a DevType command example
- `State` - return the state of the device
- `CrashFromX` - simulate a crash of the device

The attributes shown in the AtkPanel are mostly real-time values. If instead a user wants to
view how the attribute value changes they can use the [Taurus framework](#taurus) widgets.

TangoTest has an attribute that is generated using a trigonometric functions, so it is easy to check if the device is working correctly.
Below is the `TaurusTrend` view of the `double_scalar_rww` TangoTest attribute:

:::{figure} how-to-try-tango/taurus-trend-example.png
:align: center
:scale: 75 %
:::

To run TaurusTrend uses a command:

```console
taurus trend sys/tg_test/1/double_scalar_rww
```

Taurus also has a custom device panel (similar to the AtkPanel) which can be started with:

```console
taurus device sys/tg_test/1/double_scalar_rww
```

The [Tango Archiving System](#hdbpp-manual) can be used to store the attribute value changes long term.
