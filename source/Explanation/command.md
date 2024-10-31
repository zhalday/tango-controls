(tango-command-model)=
# Command

An action to the Tango device is the closest concept of a Command in Tango. Commands are well-suited for sending orders to a device, such as switching from one mode of operation to another. For example, switching a power supply on or off is typically done via a command.

## Description

Each device class implements a list of commands. Commands are essential because they serve as the primary controls for managing a device. Commands have a fixed calling syntax, consisting of one input argument and one output argument. Argument types must be chosen from a set of predefined data types: all simple types (boolean, short, long (32 bits), long (64 bits), float, double, unsigned short, unsigned long (32 bits), unsigned long (64 bits), and string), along with arrays of simple types and arrays of strings and longs or strings and doubles.

Commands can execute any sequence of actions. They can be executed synchronously (the requester is blocked until the command ends) or asynchronously (the requester sends the request and is called back when the command ends).

## The Default Commands

There are three default commands that every device must respond to in order to enhance standard behavior in a TANGO control system. These commands are **State**, **Status**, and **Init**.

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
