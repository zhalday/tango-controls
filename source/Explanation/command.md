(tango-command-model)=
# Command

%[glossary_term][command]
%A command is an operation a user may invoke on a device (eg. `SwitchOn`, `SwitchOff`). It also relates to a specific method in OOP (Object-Oriented Programming). Tango Controls allows a command to get input argument (argin) and to return a value (argout). List of available commands for a certain device is defined by its {term}`device class`. See the [command section](<#tango-command-model>) of this documentation for more details.

A command is associated with an action. *On, Off, Start, Stop* are commons examples. Commands are well-suited for sending orders to a device, such as switching from one mode of operation to another. For example, switching a power supply on or off is typically done via a command.

## Description

Each device class implements a list of commands. Commands are essential because they serve as the primary controls for managing a device. Commands have a fixed calling syntax, consisting of **one** input argument and **one** output argument. Argument types must be chosen from a set of predefined data types which include:
- void, boolean, short, long, long64, float, double, string, unsigned short, unsigned long, unsigned long64
- *1D array of the followings types :* char, short, long, long64, float, double, unsigned short, unsigned long, unsigned long64, string
- State: enumeration, representing the different states described in the section on [Device State ](#device-state).
- 2 particular types: longstringarray and doublestringarray. These are structures including one array of long/double and one array of string.

The list of data types is fixed. If you need to add your own data type then use the DevEncoded type and encode your own data type. Or you can use the DevPipe communication channel (available since Tango 9).

Commands can execute any sequence of actions. They can be executed synchronously (the requester is blocked until the command ends) or asynchronously (the requester sends the request and is called back when the command ends).

## The Default Commands

There are three default commands that every device must respond to in order to enhance standard behavior in a Tango control system. These commands are **State**, **Status**, and **Init**.

### State Command

The default behavior of the State command is to return the current state of a device, with one exception: if the result of the command is **ON** and in an **ALARM** state, Tango will:

- Read all attribute(s) with an alarm level defined,
- Change the device state to **ALARM** if any attribute read value is above/below the alarm level,
- Return the device state.

:::{note}
This behavior can be redefined by the implementer of the device. It is recommended to check the device documentation for exact behavior.
:::

:::{note}
There is no difference in behavior between the State command and the State attribute. In both cases, the resulting state is the same.
:::

### Status Command

The Status command returns a text message that provides detailed information about the state of the device. The default behavior of the Status command follows the same logic as the default behavior of the [State command](#state-command). When the device state is **ALARM**, the command will return the device status along with a list of all attributes that are in an alarm condition.

:::{note}

This behavior can be redefined by the implementer of the device. It is recommended to check the device documentation for exact behavior.
:::

:::{note}
There is no difference in behavior between the Status command and the Status attribute. In both cases, the resulting status is the same.
:::

### Init Command

The Init command is used to reinitialize a device without losing its network connection. The behavior of this command should reload any resources owned by the device, similar to how they are loaded after the device's initial startup.
