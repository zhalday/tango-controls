# Attribute alarms

{audience}`all`

Tango provides an automatic way of defining alarms. An alarm
condition will switch the attribute quality factor to alarm and the
device state will automatically switched to ALARM in certain
conditions.  Four properties are available for alarm purpose.


  > For example the voltage of a powersupply set via a DAC and read via an
  > ADC convertor. Both values can be different due to various factors such
  > as internal resistor or noise on the ADC. Additionally 
  > the powersupply may need a certain time to establish its
  > output voltage when changing the set point. The Tango alarm system is able to handle the acceptable noise threshold and the time the device needs to
  > establish the voltage after the writing of the setpoint (time
  > constant). 


## The level alarms

This alarm is defined for all Tango attribute read type and for
numerical data type. The action of this alarm depend on the attribute
value when it is read :

- If the attribute value is below or equal the attribute configuration
  **min_alarm** parameter, the attribute quality factor is switched to
  Tango::ATTR_ALARM and if the device state is Tango::ON, it is
  switched to Tango::ALARM.
- If the attribute value is below or equal the attribute configuration
  **min_warning** parameter, the attribute quality factor is switched
  to Tango::ATTR_WARNING and if the device state is Tango::ON, it is
  switched to Tango::ALARM.
- If the attribute value is above or equal the attribute configuration
  **max_warning** parameter, the attribute quality factor is switched
  to Tango::ATTR_WARNING and if the device state is Tango::ON, it is
  switched to Tango::ALARM.
- If the attribute value is above or equal the attribute configuration
  **max_alarm** parameter, the attribute quality factor is switched to
  Tango::ATTR_ALARM and if the device state is Tango::ON, it is
  switched to Tango::ALARM.

If the attribute is a spectrum or an image, then the alarm is set if any
one of the attribute value satisfies the above criterium. By default,
these four parameters are not defined and no check will be done.

The following figure is a drawing of attribute quality factor and device
state values function of the the attribute value.

(fig-7.1)=

:::{figure} attribute-alarms/alarm.png
:alt: Level alarm

Figure 7.1: Level alarm
:::

If the min_warning and max_warning parameters are not set, the
attribute quality factor will simply change between Tango::ATTR_ALARM
and Tango::ATTR_VALID function of the attribute value.

:::{warning}
The behaviour described above is only
correct in the case the device’s method
*Tango::Device\_\[X\]Impl::dev_state()* is executed*.* In case of
overwrite of the dev_state() in the device code, it is recommended to
finish the method by calling DeviceImpl::dev_state();
:::

:::{warning}
**min_warning** *and* **max_warning** : lower and upper bound
for WARNING (deprecated since version 8)
:::

## The Read Different than Set (RDS) alarm

This alarm is defined only for attribute of the Tango::READ_WRITE and
Tango::READ_WITH_WRITE read/write type and for numerical data type. This is very useful to handle maximum noise in constant time.

This alarm configuration is done with two attribute configuration parameters:
- **delta_val** and **delta_t**  Valid for a writeable attribute. Define a
  maximum difference between the set_value and the read_value of an
  attribute after a standard time. By default, these two parameters are
  not defined and no check will be done.


When the attribute is read (or when the device state is requested), if
the difference between its read value and the last written value is
something more than or equal to an authorized delta and if at least a
certain amount of milli seconds occurs since the last write operation,
the attribute quality factor will be set to Tango::ATTR_ALARM and if
the device state is Tango::ON, it is switched to Tango::ALARM.

If the attribute is a spectrum or an image, then the alarm is set if any one of
the attribute value’s satisfies the above criterium. 
