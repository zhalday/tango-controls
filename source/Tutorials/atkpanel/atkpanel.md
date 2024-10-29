(atkpanel-manual)=

# ATKPanel

{audience}`all`

```{toctree}
:maxdepth: 2

self
```

## Overview

AtkPanel is a generic control panel application. It can be used to control any
Tango device. It supports most of Tango features and data types.
Using AtkPanel you can view and set attribute values, execute commands, test
the device and access diagnostic data.

:::{figure} img/atkpanel-annotated.png
:alt: AtkPanel main window

AtkPanel 5.5 main window
:::

1. Menu bar
2. Device state
3. Device name
4. Commands drop-down
5. Device status
6. Device attributes
7. Attribute switcher

By default AtkPanel opens the scalar attribute view. If your device has
attributes of non-scalar types, they will appear on the attribute switcher on
the bottom of the window.

:::{figure} img/atkpanel.png
:alt: Scalar attributes view

Scalar attributes view
:::

:::{figure} img/array.png
:alt: Double array attribute view

Double array attribute view
:::

:::{figure} img/bool-array.png
:alt: Boolean array attribute view

Boolean array attribute view
:::

:::{figure} img/image.png
:alt: Image attribute view

Image attribute view
:::

You can run a command by selecting the command name from the command drop-down
list.

:::{figure} img/commands.png
:alt: Command drop-down list

Command drop-down list
:::

(device-testing)=

## Device testing

By selecting {guilabel}`View > Test device` from the menu you can open the
device testing panel. In this panel you can check how the device is reponding
to different commands and attribute values and how much time the requests take.

:::{figure} img/test-commands.png
:alt: Test commands view

Test commands view
:::

:::{figure} img/test-attrs.png
:alt: Test attributes view

Test attributes view
:::

:::{figure} img/test-pipe.png
:alt: Test pipes view

Test pipes view
:::

:::{figure} img/test-admin.png
:alt: Test admin view

Test admin view
:::

On the {guilabel}`Admin` tab of {guilabel}`Test Device` window you can set the
device's administrative configuration such as value source, timeout, etc.

## Trends

By choosing {guilabel}`View > Numeric & State Trend` or
{guilabel}`View > Boolean Trend` you can see the numeric & state or boolean
trend of selected attributes.

:::{figure} img/trend.png
:alt: Numeric & State trend

Numeric & State trend
:::

:::{figure} img/bool-trend.png
:alt: Boolean trend

Boolean trend
:::

You can add attributes to the trend by right-clicking the attribute and
selecting the desired axis. You can plot the data on X and two Y axes.

## Error History

The {guilabel}`View > Error history` menu option opens the list of recent Tango
errors that occured with the device.

:::{figure} img/error-history.png
:alt: Error history

Error history
:::

## Diagnostics

The {guilabel}`View > Diagnostic` menu option provides an overview on device
diagnostic information. You can check the device interface version, events and
polling statistics and command execution counts.

:::{figure} img/diagnostic-device.png
:alt: Device diagnostics

Device diagnostics
:::

:::{figure} img/diagnostic-attr.png
:alt: Attribute diagnostics

Attribute diagnostics
:::

:::{figure} img/diagnostic-polled-attr.png
:alt: Polled attribute diagnostics

Polled attribute diagnostics
:::

:::{figure} img/diagnostic-command.png
:alt: Command diagnostics

Command diagnostics
:::

## Preferences

From the {guilabel}`Preferences` menu you can tweak AtkPanel refreshing, set
the timeout and switch between {guilabel}`Operator View` and
{guilabel}`Expert View`. In {guilabel}`Expert View` you can see the attributes
that have display level set to {code}`EXPERT`.

:::{figure} img/preferences-menu.png
:alt: AtkPanel Preferences

AtkPanel Preferences
:::
