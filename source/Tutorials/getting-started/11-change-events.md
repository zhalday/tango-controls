# Change events

So far, every time you needed a value from a device you had to explicitly ask for it.
But what if you want to be notified automatically when something changes?
In Tango, this is done with {term}`events`.

The most common type is the **change event**: the device pushes a notification to all
subscribed clients whenever a value changes.  No more polling!

In this example, a `LedDevice` runs on a Raspberry Pi and controls a physical LED.
Two attributes demonstrate change events in practice:

- `ledOn` — a boolean that tracks whether the LED is on or off.
  A change event is pushed every time the LED is switched.
- `randomNumber` — a float that is updated on demand.
  A change event is only pushed when the new value differs from the previous one by
  more than `0.001` (the `abs_change` threshold).

:::{note}
This example requires a Raspberry Pi with an LED wired between GPIO pin 17 (the default)
and ground via a current-limiting resistor.  The GPIO pin can be changed with the
`gpio_pin` {term}`device property`.
:::

:::::{tab-set}

::::{tab-item} Python
```{literalinclude} 11-change-events/python/main.py
:caption: main.py
:language: python
:lines: 4-
:emphasize-lines: 19-20,29-32,38,44-45
```
::::

::::{tab-item} C++
Sorry, still TODO!
::::

::::{tab-item} Java
Sorry, still TODO!
::::

:::::

## Declaring that events will be pushed

Before clients can subscribe to change events, the device must declare its intent to push
them.  This is done in `init_device` by calling `set_change_event`:

```python
self.set_change_event("ledOn", True, False)
self.set_change_event("randomNumber", True, True)
```

The three arguments are:

1. **attribute name** — which attribute will push the event.
2. **implemented** — `True` means the device will push events manually from code (not
   relying on polling).
3. **detect** — when `True`, Tango compares the pushed value against the last one and
   only forwards the event to clients if the change exceeds the configured threshold
   (e.g. `abs_change`).  When `False`, every call to `push_change_event` is forwarded
   unconditionally.

For `ledOn` (a boolean), any state flip is meaningful, so `detect=False` is used and the
event is pushed on every call to `SetLed`.

For `randomNumber`, `detect=True` is combined with `abs_change=0.001` declared on the
attribute itself.  Tango will silently discard the event if the new value is within
`0.001` of the last forwarded value.

## Pushing events from commands

Inside `SetLed` and `GenerateRandomNumber`, the event is fired with `push_change_event`:

```python
self.push_change_event("ledOn", self._led_on)
self.push_change_event("randomNumber", self._random_number)
```

The device state is also kept in sync: `DevState.ON` when the LED is on,
`DevState.OFF` when it is off.

## Subscribing to events from a client

[Run this example](#tut-01-run-server-no-db),
and in a second terminal, subscribe to the change events:

```python-console
>>> import tango

>>> dp = tango.DeviceProxy("test/nodb/leddevice")

>>> results = []
>>> def on_event(event):
...     results.append(event.attr_value.value)

>>> led_id = dp.subscribe_event("ledOn", tango.EventType.CHANGE_EVENT, on_event)
>>> rnd_id = dp.subscribe_event("randomNumber", tango.EventType.CHANGE_EVENT, on_event)

>>> dp.SetLed(True)    # LED turns on — change event fires immediately
>>> dp.SetLed(False)   # LED turns off — another change event fires
>>> dp.GenerateRandomNumber()  # fires only if new value differs by > 0.001

>>> results
[True, False, 0.7342819...]

>>> dp.unsubscribe_event(led_id)
>>> dp.unsubscribe_event(rnd_id)
```

Subscribing returns an integer event ID that you can later pass to `unsubscribe_event`
to stop receiving notifications.

:::{tip}
You can inspect the event configuration of an attribute at any time:

```python-console
>>> config = dp.get_attribute_config("randomNumber")
>>> config.events.ch_event.abs_change
'0.001'
```
:::

## Key takeaways

- **Change events replace polling.** Instead of clients repeatedly reading an attribute,
  the device pushes a notification the moment the value changes.

- **Declare intent in `init_device`.** Call `self.set_change_event(attr, True, detect)`
  for every attribute that will push events.

- **Push from the command that causes the change.** Call `self.push_change_event(attr, value)`
  at the point where the value actually changes — usually inside a command.

- **`detect=False` — push unconditionally.** Every `push_change_event` call is forwarded
  to clients.  Use this for boolean or discrete values (like `ledOn`) where any flip is
  meaningful.

- **`detect=True` + `abs_change` — let Tango filter.** Tango compares the new value
  against the last forwarded value and only fires the event if the difference exceeds
  `abs_change`.  Use this for continuous values (like `randomNumber`) to avoid flooding
  clients with noise from tiny fluctuations.

- **Keep state and device state in sync.** When a command changes hardware, update both
  the internal variable (`self._led_on`) and the Tango device state
  (`self.set_state(DevState.ON/OFF)`) so every client sees a consistent picture.

- **GPIO pin as a device property.** Hard-coding hardware addresses is fragile.
  Exposing the pin number as a {term}`device property` (with a sensible default) makes
  the same device class reusable across different wiring configurations.
