# Generate events in a device server

```{tags} audience:developers, lang:c++
```

The server is the origin of events. It will fire events as soon as
they occur. For a detailed explanation of the different types of events
in Tango please see the [events section](#events-tangoclient).
Standard events (*change*, *periodic* and *archive*) are
detected automatically in the polling thread and fired immediately.
The *periodic* events can only be handled by the polling
thread. The *change*, *data ready* and *archive* events can also be manually pushed
from the device server code. To allow a client to subscribe to events
of attributes that are not polled the server has to declare that events are pushed
from the code. Four methods are available for this purpose:

:::::{tab-set}

::::{tab-item} C++

```{code} cpp
:number-lines: 1

  Attr::set_change_event(bool implemented, bool detect = true);
  Attr::set_archive_event(bool implemented, bool detect = true);
  Attr::set_alarm_event(bool implemented, bool detect = true);
  Attr::set_data_ready_event(bool implemented);
```

For example:
```{code} cpp
:number-lines: 1
  // Create a new read-only, short attribute
  Tango::Attr *at = new Tango::Attr("some_attribute", Tango::DEV_SHORT, Tango::READ);

  // Indicate that the following events will be push manually
  // for this attribute
  at->set_change_event(true)
  at->set_archive_event(true)
  at->set_alarm_event(true)
  at->set_data_ready_event(true)
```

::::
::::{tab-item} Python

```{code} Python
:number-lines: 1

  Attribute.set_change_event(bool implemented, bool detect = True)
  Attribute.set_archive_event(bool implemented, bool detect = True)
  Attribute.set_alarm_event(bool implemented, bool detect = True)
  Attribute.set_data_ready_event(bool implemented)
```
For example:
```{code} Python
:number-lines: 1
  # Create a new read-only, short attribute
  at = attribute(
    dtype=int, access=AttrWriteType.READ
  )

  # Indicate that the following events will be push manually
  # for this attribute
  at.set_change_event(True)
  at.set_archive_event(True)
  at.set_alarm_event(True)
  at.set_data_ready_event(True)
```

::::
:::::

where `implemented=true` indicates that events are pushed manually
from the code and `detect=true` triggers verification of the event
using the same event properties defined for the polling thread.
Note that when `detect=false`, no value checking is done on the pushed
value.

The class `DeviceImpl` also supports the first two methods with an
additional parameter `attr_name` defining the attribute name:

:::::{tab-set}

::::{tab-item} C++

```{code} cpp
:number-lines: 1

  DeviceImpl::set_change_event(string attr_name, bool implemented, bool detect = true);
  DeviceImpl::set_archive_event(string attr_name, bool implemented, bool detect = true);
  DeviceImpl::set_alarm_event(string attr_name, bool implemented, bool detect = true);
  DeviceImpl::set_data_ready_event(string attr_name, bool implemented);
```

For example:
```{code} cpp
:number-lines: 1

  // Constructor
  TestDevice::TestDevice(Tango::DeviceClass *cl, std::string &s): TANGO_BASE_CLASS(cl, s.c_str())
  {
    init_device()
  }
  ...


  void TestDevice::init_device()
  {
    // Indicate that the following events will be push manually for the attribute
    // named "some_attribute"
    this->set_change_event("some_attribute", true);
    this->set_archive_event("some_attribute", true);
    this->set_alarm_event("some_attribute", true);
    this->set_data_ready_event("some_attribute", true);
  }


```

::::
::::{tab-item} Python

```{code} Python
:number-lines: 1

  DeviceImpl.set_change_event(str attr_name, bool implemented, bool detect = True)
  DeviceImpl.set_archive_event(str attr_name, bool implemented, bool detect = True)
  DeviceImpl.set_alarm_event(str attr_name, bool implemented, bool detect = True)
  DeviceImpl.set_data_ready_event(str attr_name, bool implemented)
```
For example:
```{code} Python
:number-lines: 1

  class TestDevice(Device):

    def init_device(self):

      super().init_device()

      # Indicate that the following events will be push manually for the attribute
      # named "some_attribute"
      self.set_change_event("some_attribute", True)
      self.set_archive_event("some_attribute", True)
      self.set_alarm_event("some_attribute", True)
      self.set_data_ready_event("some_attribute", True)
```

::::
:::::


To push events manually from the code a set of data type dependent
methods can be used:


:::::{tab-set}

::::{tab-item} C++

```{code} cpp
:number-lines: 1

  DeviceImpl::push_change_event(string attr_name, ...);
  DeviceImpl::push_archive_event(string attr_name, ...);
  DeviceImpl::push_alarm_event(string attr_name, ...);
  // ctr = Optional "counter"
  DeviceImpl::push_data_ready_event(string attr_name, Tango::DevLong ctr = 0);
```
where the `ctr` is an optional counter, which will be passed within the event.

For example:
```{code} cpp
:number-lines: 1

  void sendEventTest
  {
    Tango::DevDouble v{10};
    // Push an alarm event for the attribute "some_attribute"
    this->push_alarm_event("some_attribute", &v);
    // Push a change event for the attribute "some_attribute"
    this->push_change_event("some_attribute", &v);
    // Push an archive event for the attribute "some_attribute"
    this->push_archive_event("some_attribute", &v);
    // Push a 'data ready' event for the attribute "some_attribute"
    this->push_data_ready_event("some_attribute");
  }


```

::::
::::{tab-item} Python

```{code} Python
:number-lines: 1

  DeviceImpl.push_change_event(str attr_name, ...)
  DeviceImpl.push_archive_event(str attr_name, ...)
  DeviceImpl.push_alarm_event(str attr_name, ...)
  DeviceImpl.push_data_ready_event(str attr_name, int ctr = 0)
```
where the `ctr` is an optional counter, which will be passed within the event.

For example:
```{code} Python
:number-lines: 1

def sendEventTest(self):
  # Push an alarm event for the attribute "some_attribute"
  self.push_change_event("some_attribute", 10)
  # Push a change event for the attribute "some_attribute"
  self.push_archive_event("some_attribute", 10)
  # Push an archive event for the attribute "some_attribute"
  self.push_alarm_event("some_attribute", 10)
  # Push a 'data ready' event for the attribute "some_attribute"
  self.push_data_ready_event("some_attribute", 10)
```

::::
:::::


See the appropriate API for all available interfaces.
- C++: [C++ API documentation](https://tango-controls.gitlab.io/cppTango/)
- Python: [PyTango API documentation](inv:pytango:std:doc#api)

For non-standard events a single call exists for pushing the data to the
CORBA Notification Service (omniNotify). Clients who are subscribed to
this event have to know what data type is in the DeviceAttribute and
unpack it accordingly.

To push non-standard events, the following api call is available to
all device servers:


:::::{tab-set}

::::{tab-item} C++

```{code} cpp
:number-lines: 1

  DeviceImpl::push_event(string attr_name,
               vector<string> &filterable_names,
               vector<double> &filterable_vals,
               ...);
```

::::

::::{tab-item} Python

```{code} python
:number-lines: 1

  DeviceImpl.push_event(str attr_name,
               Sequence[str] filterable_names,
               Sequence[double] filterable_vals,
               ...)
```

::::
:::::

where `attr_name` is the name of the attribute and `filterable_names`
and `filterable_vals` represent any data which can be used
by clients to filter on.

Here is a typical example of what a server will
need to do to send its own events. This attribute is readable
and an event is sent if its value is positive when it is read. On top of
that, this event is sent with one filterable field called *value* which is
set to the attribute value.

:::::{tab-set}

::::{tab-item} C++
```{code} cpp
:number-lines: 1

  void MyClass::read_Sinusoide(Tango::Attribute &attr)
  {
    ...
       struct timeval tv;
       gettimeofday(&tv, NULL);
       sinusoide = 100 * sin( 2 * 3.14 * frequency * tv.tv_sec);

       if (sinusoide >= 0)
       {
          vector<string> filterable_names;
          vector<double> filterable_value;

          filterable_names.push_back("value");
          filterable_value.push_back((double)sinusoide);

          push_event(attr.get_name(),filterable_names, filterable_value);
       }
    ...
 }
```
line 13-14 : The filter pair name/value is initialised

line 16 : The event is pushed

::::

::::{tab-item} Python

```{code} python
:number-lines: 1

  def read_Sinusoide(self, attr):
    ...

    time_of_day = datetime.datetime.now.timestamp()
    sinusoide = 100 * sin( 2 * 3.14 * frequency * time_of_day)

    if sinusoide >= 0:
      filterable_names = ["value"]
      filterable_value = [sinusoide]

      push_event(attr.get_name(), filterable_names, filterable_value)

    ...
```

line 8-9 : The filter pair name/value is initialised

line 11: The event is pushed

::::
:::::
