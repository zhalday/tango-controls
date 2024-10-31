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

(configuring-events)=
## Configuring events

The attribute configuration set is used to configure under what
conditions events are generated. A set of standard attribute properties
(part of the standard attribute configuration) are read from the
database at device startup time and used to configure the event engine.
If there are no properties defined then default values specified in the
code are used.

### change

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

### periodic

The attribute properties and their default values for the periodic event
are :

1. **event_period** - the minimum time between events (in
   milliseconds). If no property is specified then a default value of 1
   second is used.

### archive

The attribute properties and their default values for the archive event
are :

1. **archive_rel_change** - a property of maximum 2 values which
   specifies the positive and negative relative change w.r.t. the
   previous attribute value which will trigger the event. If the
   attribute is a spectrum or an image then an archive event is
   generated if any one of the attribute value’s satisfies the above
   criteria. If only one property is specified then it is used for the
   positive and negative change. If no properties are specified then no
   events are generated.
2. **archive_abs_change** - a property of maximum 2 values which
   specifies the positive and negative absolute change w.r.t the
   previous attribute value which will trigger the event. If the
   attribute is a spectrum or an image then an archive event is
   generated if any one of the attribute value’s satisfies the above
   criteria. If only one property is specified then it is used for the
   positive and negative change. If no properties are specified then the
   relative change is used.
3. **archive_period** - the minimum time between archive events (in
   milliseconds). If no property is specified, no periodic archiving
   events are send.


[^footnote-1]: note: the polling is de-correlated with the hours/minutes/seconds 
to avoid polling peaks when there is an hour/minute/second change.