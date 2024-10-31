(tango-command-model)=
# Command

An action to the Tango device is the closest concept of Command in Tango.
Command are well adapted to send order to a device like switching from one mode of
operation to another mode of operation. For example, switching on/off a power supply is typically done via a command.

## Description 

Each device class implements a list of commands. Commands are very
important because they are the client’s major dials and knobs for
controlling a device. Commands have a fixed calling syntax - consisting
of one input argument and one output argument. Arguments type must be
chosen in a fixed set of data types: All simple types (boolean, short,
long (32 bits), long (64 bits), float, double, unsigned short, unsigned
long (32 bits), unsigned long (64 bits) and string) and arrays of simple
types plus array of strings and longs and array of strings and doubles).

Commands can execute any sequence of actions.
Commands can be executed synchronously (the requester is blocked until the command ended) or
asynchronously (the requester send the request and is called back when
the command ended).


## The default commands

It exists three default commands that every devices must to respond to, to increase the standard behavior in a TANGO control system.
These commands are **State**, **Status**, **Init**.

(state-command)=
### State command

The default behavior of the State command is to return the current state of a device, with one exception. If the result of the command is ON and ALARM state, then Tango will:
- read all the attribute(s) with an alarm level defined
- changing the device state to ALARM if any of the attribute read value is above/below the alarm level.
- returns the device state.

:::{note}
This behaviour can redefined by the implementer of the device. Better to check the documentation of the device for the exact behaviour.
:::

:::{note}
There no difference in behaviour between the 
State command and the State attribute. In both case, the resulting state is the same.
:::

### Status command

The Status command returns a text message which should inform in details the state of the device. 
The default behavior of the Status command follows the same logic of the default behaviour of the (State command)[#state-command]. When the device state is ALARM, the command will return the device status with the addition of the list of  all the attributes which are in alarm condition.

:::{note}
This behaviour can redefined by the implementer of the device. Better to check the documentation of the device for the exact behaviour.
:::

:::{note}
There no difference in behaviour between the Status command and the Status attribute. In both case, the resulting status is the same.
:::

### Init command

The Init command is used to re-initialize a device without losing its
network connection. The behaviour of this command should reload any resource own by the device in the same way as after the initial start up of the device.

