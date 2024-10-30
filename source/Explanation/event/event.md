(events-tangoclient)=

# Events

## Introduction

Events are a critical part of any distributed control system. Their aim
is to provide a communication mechanism which is fast and efficient.

The standard CORBA communication paradigm is a synchronous or
asynchronous two-way call. In this paradigm the call is initiated by the
client who contacts the server. The server handles the client’s request
and sends the answer to the client or throws an exception which the
client catches. This paradigm involves two calls to receive a single
answer and requires the client to be active in initiating the request.
If the client has a permanent interest in a value it is obliged to poll
the server for an update in a value every time. This is not efficient in
terms of network bandwidth nor in terms of client programming.

For clients who are permanently interested in values, the event-driven
communication paradigm is a more efficient and natural way of
programming. In this paradigm the client registers its interest once in
an event (value). After that the server informs the client every time
the event has occurred. This paradigm avoids the client polling, frees
it for doing other things, is fast and makes efficient use of the
network.

The rest of this chapter explains how the TANGO events are implemented
and the application programmer’s interface.

## Event definition

TANGO events represent an alternative channel for reading TANGO device
attributes. Device attributes values are sent to all subscribed clients
when an event occurs. Events can be an attribute value change, a change
in the data quality or a periodically sent event. The clients continue
receiving events as long as they stay subscribed. Most of the time, the
device server polling thread detects the event and then pushes the
device attribute value to all clients. Nevertheless, in some cases, the
delay introduced by the polling thread in the event propagation is
detrimental. For such cases, some API calls can be used to directly push the event.

Until TANGO release 8, the notifd event implementation of the CORBA
Notification service was used to dispatch events. Starting with TANGO 8,
this CORBA Notification service has been replaced by the ZMQ library
which implements a Publish/Subscribe communication model well adapted to
TANGO events communication.

Alarm events are only available from TANGO release 10 and do not support the
notifd event implementation.

## Event types

The following nine event types have been implemented in TANGO :

1. **change** - an event is triggered and the attribute value is sent
   when the attribute value changes significantly. The exact meaning of
   significant is device attribute dependent. For analog and digital
   values this is a delta fixed per attribute, for string values this is
   any non-zero change i.e. if the new attribute value is not equal to
   the previous attribute value. The delta can either be specified as a
   relative or absolute change. The delta is the same for all clients
   unless a filter is specified (see below).  
   Change events also triggered in the following cases :

    1. When a spectrum or image attribute size changes.
    2. At event subscription time
    3. When the polling thread receives an exception during attribute
       reading
    4. When the polling thread detects that the attribute quality factor
       has changed.
    5. The first good reading of the attribute after the polling thread
       has received exception when trying to read the attribute
    6. The first time the polling thread detects that the attribute
       quality factor has changed from INVALID to something else
    7. When a change event is pushed manually from the device server
       code. (*DeviceImpl::push_change_event()*).
    8. By the methods Attribute::set_quality() and
       Attribute::set_value_date_quality() if a client has subscribed
       to the change event on the attribute. This has been implemented
       for cases where the delay introduced by the polling thread in the
       event propagation is not authorized.

2. **periodic** - an event is sent at a fixed periodic interval. The
   frequency of this event is determined by the *event_period* property
   of the attribute and the polling frequency. The polling frequency
   determines the highest frequency at which the attribute is read. The
   event_period determines the highest frequency at which the periodic
   event is sent. Note if the event_period is not an integral number of
   the polling period there will be a beating of the two
   frequencies [^footnote-1]. Clients can reduce the frequency at which they
   receive periodic events by specifying a filter on the periodic event
   counter.

3. **archive** - an event is sent if one of the archiving conditions is
   satisfied. Archiving conditions are defined via properties in the
   database. These can be a mixture of delta_change and periodic.
   Archive events can be send from the polling thread or can be manually
   pushed from the device server code
   (*DeviceImpl::push_archive_event()*).

4. **alarm** - an "alarming" subset of change events to allow clients to monitor
   when attributes' quality factors are either *Tango::ATTR_WARNING* or
   *Tango::ATTR_ALARM*, without receiving unneeded events relating to value
   changes.  An event is considered to be alarming if one of the following is
   true:

    1. The attribute quality factor transitions to or from:
       - *Tango::ATTR_WARNING*
       - *Tango::ATTR_ALARM*.
    2. The event contains an exception and the previous event did not contain an
    exception.
    3. The event contains an exception which is different from the
    exception in the previous event.
    4. The event does not contain an exception and the previous event did contain
    an exception.

   Alarm events are triggered in the following circumstances:

    1. At event subscription time as part of the subscription command

    2. When the polling thread detects an alarming event as defined above

    3. When an alarm event is pushed manually from the device server
       code. (*DeviceImpl::push_alarm_event()*).

    4. When a change event is pushed manually from the device server code
       (*DeviceImpl::push_change_event()*) and the following is true:

       > 1. the AutoAlarmOnChangeEvent CtrlSystem property is defined and not the case-insensitive string "false".
       > 2. the attribute is not configured to push manual alarm events (*DeviceImpl::set_alarm_event()* with the implemented flag set to false).
       > 3. the event is considered to be alarming as defined above

    5. By the methods Attribute::set_quality() and
       Attribute::set_value_date_quality() when the following is true:

       > 1. a change event would be sent from these methods
       > 2. the AutoAlarmOnChangeEvent CtrlSystem property is defined and not the case-insensitive string "false".
       > 3. the attribute is not configured to push manual alarm events (*DeviceImpl::set_alarm_event()* with the implemented flag set to false).
       > 4. the quality factor change is considered to be alarming as defined above

5. **attribute configuration** - an event is sent if the attribute
   configuration is changed.

6. **data ready** - This event is sent when coded by the device server
   programmer who uses a specific method of one of the Tango device
   server class to fire the event
   (*DeviceImpl::push_data_ready_event()*). The rule of this event is
   to inform a client that it is now possible to read an attribute. This
   could be useful in case of attribute with many data.

7. **user** - The criteria and configuration of these user events are
   managed by the device server programmer who uses a specific method of
   one of the Tango device server class to fire the event
   (*DeviceImpl::push_event()*).

8. **device interface change** - This event is sent when the device
   interface changes. Using Tango, it is possible to dynamically
   add/remove attribute/command to a device. This event is the way to
   inform client(s) that attribute/command has been added/removed from a
   device. Note that this type of event is attached to a device and not
   to one attribute (like all other event types). This event is
   triggered in the following case :

    1. A dynamic attribute or command is added or removed. The event is
       sent after a small delay (50 mS) in order to eliminate the risk of
       events storm in case several attributes/commands are added/removed
       in a loop
    2. At the end of admin device RestartServer or DevRestart command
    3. After a re-connection due to a device server restart. Because the
       device interface is not memorized, the event is sent even if it is
       highly possible that the device interface has not changed. A flag
       in the data propagated with the event inform listening
       applications that the device interface change is not guaranteed.
    4. At event re-connection time. This case is similar to the previous
       one (device interface change not guaranteed)

9. **pipe** - This is the kind of event which has to be used when the
   user want to push data through a pipe. This kind of event is only
   sent by the user code by using a specific method
   (*DeviceImpl::push_pipe_event()*). There is no way to ask the Tango
   kernel to automatically push this kind of event.

The first four are automatically generated by the TANGO library or fired by the
user code. Events number 5 and 8 are only automatically sent by the library and
events 6, 7 and 9 are fired only by the user code.

## Application Programmer’s Interface

How to setup and use the TANGO events ? The interfaces described here
are intended as user friendly interfaces to the underlying CORBA calls.
The interface is modeled after the asynchronous *command_inout()*
interface so as to maintain coherency. The event system supports **push
callback model** as well as the **pull callback model.**

The two event reception modes are:

- **Push callback model** : On event reception a callbacks method gets
  immediately executed.
- **Pull callback model** : The event will be buffered the client until
  the client is ready to receive the event data. The client triggers
  the execution of the callback method.

The event reception buffer in the **pull callback model**, is
implemented as a round robin buffer. The client can choose the size when
subscribing for the event. This way the client can set-up different ways
to receive events.

- Event reception buffer size = 1 : The client is interested only in
  the value of the last event received. All other events that have been
  received since the last reading are discarded.
- Event reception buffer size > 1 : The client has chosen to keep an
  event history of a given size. When more events arrive since the last
  reading, older events will be discarded.
- Event reception buffer size = ALL_EVENTS : The client buffers all
  received events. The buffer size is unlimited and only restricted by
  the available memory for the client.

### Configuring events

The attribute configuration set is used to configure under what
conditions events are generated. A set of standard attribute properties
(part of the standard attribute configuration) are read from the
database at device startup time and used to configure the event engine.
If there are no properties defined then default values specified in the
code are used.

#### change

The attribute properties and their default values for the change event
are :

1. **rel_change** - a property of maximum 2 values. It specifies the
   positive and negative relative change of the attribute value w.r.t.
   the value of the previous change event which will trigger the event.
   If the attribute is a spectrum or an image then a change event is
   generated if any one of the attribute value’s satisfies the above
   criterium. If only one property is specified then it is used for the
   positive and negative change. If no property is specified, no events
   are generated.
2. **abs_change** - a property of maximum 2 values.It specifies the
   positive and negative absolute change of the attribute value w.r.t
   the value of the previous change event which will trigger the event.
   If the attribute is a spectrum or an image then a change event is
   generated if any one of the attribute value’s satisfies the above
   criterium. If only one property is specified then it is used for the
   positive and negative change. If no properties are specified then the
   relative change is used.

#### periodic

The attribute properties and their default values for the periodic event
are :

1. **event_period** - the minimum time between events (in
   milliseconds). If no property is specified then a default value of 1
   second is used.

#### archive

The attribute properties and their default values for the archive event
are :

1. **archive_rel_change** - a property of maximum 2 values which
   specifies the positive and negative relative change w.r.t. the
   previous attribute value which will trigger the event. If the
   attribute is a spectrum or an image then an archive event is
   generated if any one of the attribute value’s satisfies the above
   criterium. If only one property is specified then it is used for the
   positive and negative change. If no properties are specified then no
   events are generate.
2. **archive_abs_change** - a property of maximum 2 values which
   specifies the positive and negative absolute change w.r.t the
   previous attribute value which will trigger the event. If the
   attribute is a spectrum or an image then an archive event is
   generated if any one of the attribute value’s satisfies the above
   criterium. If only one property is specified then it is used for the
   positive and negative change. If no properties are specified then the
   relative change is used.
3. **archive_period** - the minimum time between archive events (in
   milliseconds). If no property is specified, no periodic archiving
   events are send.

### C++ Clients

This is the interface for clients who want to receive events. The main
action of the client is to subscribe and unsubscribe to events. Once the
client has subscribed to one or more events the events are received in a
separate thread by the client.

Two reception modes are possible:

- On event reception a callbacks method gets immediately executed.
- The event will be buffered until the client until the client is ready
  to receive the event data.

The mode to be used has to be chosen when subscribing for the event.

#### Subscribing to events

The client call to subscribe to an event is named
*DeviceProxy::subscribe_event()* . During the event subscription the
client has to choose the event reception mode to use.

**Push model**:

```{code-block} cpp
:linenos: true

int DeviceProxy::subscribe_event(
             const string &attribute,
             Tango::EventType event,
             Tango::CallBack *callback,
             bool stateless = false);
```

The client implements a callback method which is triggered when the
event is received. Note that this callback method will be executed by a
thread started by the underlying ORB. This thread is not the application
main thread. For Tango releases before 8, a similar call with one extra
parameter for event filtering is also available.

**Pull model**:

```{code-block} cpp
:linenos: true

int DeviceProxy::subscribe_event(
             const string &attribute,
             Tango::EventType event,
             int event_queue_size,
             bool stateless = false);
```

The client chooses the size of the round robin event reception buffer.
Arriving events will be buffered until the client uses
*DeviceProxy::get_events()* to extract the event data. For Tango
releases before 8, a similar call with one extra parameter for event
filtering is also available.

On top of the user filter defined by the *filters* parameter, basic
filtering is done based on the reason specified and the event type. For
example when reading the state and the reason specified is change the
event will be fired only when the state changes. Events consist of an
attribute name and the event reason. A standard set of reasons are
implemented by the system, additional device specific reasons can be
implemented by device servers programmers.

The stateless flag = false indicates that the event subscription will
only succeed when the given attribute is known and available in the
Tango system. Setting stateless = true will make the subscription
succeed, even if an attribute of this name was never known. The real
event subscription will happen when the given attribute will be
available in the Tango system.

Note that in this model, the callback method will be executed by the
thread doing the *DeviceProxy::get_events()* call.

#### The CallBack class

In C++, the client has to implement a class inheriting from the Tango
CallBack class and pass this to the *DeviceProxy::subscribe_event()*
method. The CallBack class is the same class as the one proposed for the
TANGO asynchronous call. This is as follows for events :

```{code-block} cpp
:linenos: true

class MyCallback : public Tango::CallBack
{
   .
   .
   .
   public:
   void push_event(Tango::EventData *);
   void push_event(Tango::AttrConfEventData *);
   void push_event(Tango::DataReadyEventData *);
   void push_event(Tango::DevIntrChangeEventData *);
   void push_event(Tango::PipeEventData *);
}
```

where EventData is defined as follows :

```{code-block} cpp
:linenos: true

class EventData
{
   DeviceProxy       *device;
   string            attr_name;
   string            event;
   DeviceAttribute   *attr_value;
   bool              err;
   DevErrorList      errors;
}
```

AttrConfEventData is defined as follows :

```{code-block} cpp
:linenos: true

class AttrConfEventData
{
   DeviceProxy       *device;
   string            attr_name;
   string            event;
   AttributeInfoEx   *attr_conf;
   bool              err;
   DevErrorList      errors;
}
```

DataReadyEventData is defined as follows :

```{code-block} cpp
:linenos: true

class DataReadyEventData
{
   DeviceProxy       *device;
   string            attr_name;
   string            event;
   int               attr_data_type;
   int               ctr;
   bool              err;
   DevErrorList      errors;
}
```

DevIntrChangeEventData is defined as follows :

```{code-block} cpp
:linenos: true

class DevIntrChangeEventData
{
   DeviceProxy            device;
   string                 event;
   string                 device_name;
   CommandInfoList        cmd_list;
   AttributeInfoListEx    att_list;
   bool                   dev_started;
   bool                   err;
   DevErrorList           errors;
}
```

and PipeEventData is defined as follows :

```{code-block} cpp
:linenos: true

class PipeEventData
{
   DeviceProxy       *device;
   string            pipe_name;
   string            event;
   DevicePipe        *pipe_value;
   bool              err;
   DevErrorList      errors;
}
```

In push model, there are some cases (same callback used for events
coming from different devices hosted in device server process running on
different hosts) where the callback method could be executed concurently
by different threads started by the ORB. The user has to code his
callback method in a **thread** **safe** manner.

#### Unsubscribing from an event

Unsubscribe a client from receiving the event specified by *event_id*
is done by calling the *DeviceProxy::unsubscribe_event()* method :

```{code-block} cpp
:linenos: true

void DeviceProxy::unsubscribe_event(int event_id);
```

#### Extract buffered event data

When the pull model was chosen during the event subscription, the
received event data can be extracted with *DeviceProxy::get_events().*
Two possibilities are available for data extraction. Either a callback
method can be executed for every event in the buffer when using

```{code-block} cpp
:linenos: true

int DeviceProxy::get_events(
             int event_id,
             CallBack *cb);
```

Or all the event data can be directly extracted as EventDataList,
AttrConfEventDataList , DataReadyEventDataList,
DevIntrChangeEventDataList or PipeEventDataList when using

```{code-block} cpp
:linenos: true

int DeviceProxy::get_events(
             int event_id,
             EventDataList &event_list);

int DeviceProxy::get_events(
             int event_id,
             AttrConfEventDataList &event_list);

int DeviceProxy::get_events(
             int event_id,
             DataReadyEventDataList &event_list);

int DeviceProxy::get_events(
             int event_id,
             DevIntrChangeEventDataList &event_list);

int DeviceProxy::get_events(
             int event_id,
             PipeEventDataList &event_list);
```

The event data lists are vectors of EventData, AttrConfEventData,
DataReadyEventData or PipeEventData pointers with special destructor and
clean-up methods to ease the memory handling.

```{code-block} cpp
:linenos: true

class EventDataList:public vector<EventData *>
class AttrConfEventDataList:public vector<AttrConfEventData *>
class DataReadyEventDataList:public vector<DataReadyEventData *>
class DevIntrChangeEventDataList:public vector<DevIntrChangeEventData *>
class PipeEventDataList:public vector<PipeEventData *>
```

#### Example

Here is a typical code example of a client to register and receive
events. First, you have to define a callback method as follows:

```{code-block} cpp
:linenos: true

class DoubleEventCallBack : public Tango::CallBack
{
   void push_event(Tango::EventData*);
};


void DoubleEventCallBack::push_event(Tango::EventData *myevent)
{
    Tango::DevVarDoubleArray *double_value;
    try
    {
        cout << "DoubleEventCallBack::push_event(): called attribute "
             << myevent->attr_name
             << " event "
             << myevent->event
             << " (err="
             << myevent->err
             << ")" << endl;


         if (!myevent->err)
         {
             *(myevent->attr_value) >> double_value;
             cout << "double value "
                  << (*double_value)[0]
                  << endl;
             delete double_value;
         }
    }
    catch (...)
    {
         cout << "DoubleEventCallBack::push_event(): could not extract data !\n";
    }
}
```

:::{note}
If the event is an error event (myevent->err == true), the attr_value field in myevent EventData object will be empty (null pointer).
The same applies for some other kinds of events. For example, attr_conf field in AttrConfEventData object will be
a null pointer in case of error event (if the err field is true).
As a consequence, the device server programmer should always check the err field before trying to extract the
EventData::attr_value or AttrConfEventData::attr_conf fields associated to the event.
:::

Then the main code must subscribe to the event and choose the push or
the pull model for event reception.

**Push model**:

```{code-block} cpp
:linenos: true

DoubleEventCallBack *double_callback = new DoubleEventCallBack;

Tango::DeviceProxy *mydevice = new Tango::DeviceProxy("my/device/1");

int event_id;
const string attr_name("current");
event_id = mydevice->subscribe_event(attr_name,
                         Tango::CHANGE_EVENT,
                         double_callback);
cout << "event_client() id = " << event_id << endl;

// The callback methods are executed by the Tango event reception thread.
// The main thread is not concerned of event reception.
// Whatch out with synchronisation and data access in a multi threaded environment!

sleep(1000); // wait for events

mydevice->unsubscribe_event(event_id);
```

**Pull model**:

```{code-block} cpp
:linenos: true

DoubleEventCallBack *double_callback = new DoubleEventCallBack;
int event_queue_size = 100; // keep the last 100 events

Tango::DeviceProxy *mydevice = new Tango::DeviceProxy("my/device/1");

int event_id;
const string attr_name("current");
event_id = mydevice->subscribe_event(attr_name,
                         Tango::CHANGE_EVENT,
                         event_queue_size);
cout << "event_client() id = " << event_id << endl;

// Check every 3 seconds whether new events have arrived and trigger the callback method
// for the new events.

for (int i=0; i < 100; i++)
{
    sleep (3);

    // Read the stored event data from the queue and call the callback method for every event.
    mydevice->get_events(event_id, double_callback);
}

event_test->unsubscribe_event(event_id);
```

[^footnote-1]: note: the polling is de-correlated with the hours/minutes/seconds 
to avoid polling peaks when there is an hour/minute/second change.