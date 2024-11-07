% How-To try

# How to PyTango

```{tags} audience:developers, lang:python
```

A list of short recipes for common tasks.

## Installation notes

See the [PyTango installation guide](inv:pytango:std:label#installation).

## Before anything else

Import the PyTango module in python.

```{code-block} python
import tango
```

## Using the DeviceProxy object

**Getting the polling buffer values**

Only for polled attributes we can get the last N read values. the
polling buffer depth is managed by the admin device.

```{code-block} python
dp = tango.DeviceProxy('some/tango/device')
dp.attribute_history('cpustatus', 10)
```

### Get/Set polled attributes

```{code-block} python
def get_polled_attributes(dev_name):
    dp = tango.DeviceProxy(dev_name)
    attrs = dp.get_attribute_list()
    periods = [(a, dp.get_attribute_poll_period(a)) for a in attrs]
    return dict((a, p) for a, p in periods if p)

[plc4.poll_attribute(a, 5000) for k, v in periods if v]
```

### Modify the polling of attributes

```{code-block} python
 import re

 period = 10000
 devs = tango.Database().get_device_exported('some/tango/devices*')
 for dev in devs:
     dp = tango.DeviceProxy(dev)
     attrs = sorted([a for a in dp.get_attribute_list() if re.match('(Output|Temperature)_[0-9]$',a)])
     [dp.poll_attribute(a,period) for a in attrs]
     print('\n'.join(dp.polling_status()))
```

### Events

Creating an event callback

```{code-block} python
# The callback must be a callable or an object with a push_event(self, event) method

def callback_function(event):
    print(event)
```

Configuring an event

```{code-block} python
# From the client side
# subscribe_event(attr_name, event_type, cb_or_queuesize, filters=[], stateless=False, extract_as=tango._tango.ExtractAs.Numpy)
event_id = tango.DeviceProxy.subscribe_event(attributeName, tango.EventType.CHANGE_EVENT, callback_function, [], True)

# From inside the device server, if it will manually push events (not using server-side polling)
self.set_change_event('State', True, True)

# when an event needs to be pushed manually
self.push_change_event('State', True, True)

```

## Device Server Internal Objects

### Forcing in which host the device is exported

This environment variable must be set before launching the device:

```{code-block} console
$ export OMNIORB_USEHOSTNAME=10.0.0.10
```

### Creating a Device Server from ipython

Having defined your device in MyDS.py:

```{code-block} python
from MyDS import *
py = tango.Util(['MyDS.py', 'InstanceName'])
py.add_TgClass(MyDSClass, MyDS, 'MyDS')
U = tango.Util.instance()
U.server_init()
U.server_run()
```

### Modify internal polling

:::{note}
It doesn't work at *init_device()*; must be done later on in a *hook* method.
:::

```{code-block} python
 U = tango.Util.instance()
 dserver = U.get_dserver_device()
 admin = tango.DeviceProxy(dserver.get_name())
 dir(admin)
     [
         StartPolling
         StopPolling
         AddObjPolling
         RemObjPolling
         UpdObjPollingPeriod
         DevPollStatus
         PolledDevice
     ]

 polled_attrs = {}
 for st in admin.DevPollStatus(name):
     lines = st.split('\n')
     try:
        polled_attrs[lines[0].split()[-1]] = lines[1].split()[-1]
     except tango.DevFailed:
        pass

 type_ = 'command' or 'attribute'
 for aname in args:
    if aname in polled_attrs:
        admin.UpdObjPollingPeriod([[200], [name, type_, aname]])
    else:
        admin.AddObjPolling([[3000], [name, type_, aname]])
```

### Get all polling attributes

The polling of the attributes is recorded in the **property_device**
table of the tango database in the format of a list like
*\[ATTR1, PERIOD1, ATTR2, PERIOD2, ...\]*

The list of polled attributes can be accessed using this method of admin
device:

```{code-block} python
dp = tango.DeviceProxy('dserver/myServerClass/id22')
polled_attrs = [a.split('\n')[0].split(' ')[-1] for a in dp.DevPollStatus('domain/family/member-01')]
```

### Get the device class object from the device itself

```{code-block} python
self.get_device_class()
```

### Get the devices inside a Device Server

```{code-block} python
def get_devs_in_server(self,MyClass=None):
     """
     Method for getting a dictionary with all the devices running in this server
     """
     MyClass = MyClass or type(self) or DynamicDS
     if not hasattr(MyClass, '_devs_in_server'):
         MyClass._devs_in_server = {}  # This dict will keep an access to the class objects instantiated in this Tango server
     if not MyClass._devs_in_server:
         U = tango.Util.instance()
         for klass in U.get_class_list():
             for dev in U.get_device_list_by_class(klass.get_name()):
                 if isinstance(dev, DynamicDS):
                     MyClass._devs_in_server[dev.get_name()]=dev
     return MyClass._devs_in_server
```

### Identify each attribute inside read_attr_hardware()

```{code-block} python
def read_attr_hardware(self,data):
    self.debug("In DynDS::read_attr_hardware()")
    try:
        attrs = self.get_device_attr()
        for d in data:
            a_name = attrs.get_attr_by_ind(d).get_name()
            if a_name in self.dyn_attrs:
                self.lock.acquire()  # This lock will be released at the end of read_dyn_attr
                self.myClass.DynDev=self  # VITAL: It tells the admin class which device attributes are going to be read
                self.lock_acquired += 1
        self.debug(f'DynamicDS::read_attr_hardware(): lock acquired {self.lock_acquired} times')
    except Exception as e:
        self.last_state_exception = f'Exception in read_attr_hardware: {e}'
        self.error(f'Exception in read_attr_hardware: {e}')
```

### Device server logging (using Tango logs)

See the [PyTango logging docs](inv:pytango:std:label#logging).

### Adding dynamic attributes to a device

```{code-block} python
 self.add_attribute(
     tango.Attr( #or tango.SpectrumAttr
         new_attr_name,tango.DevArg.DevState,tango.AttrWriteType.READ, #or READ_WRITE
         #max_size or dyntype.dimx #If Spectrum
         ),
     self.read_new_attribute, #(attr)
     None, #self.write_new_attribute #(attr)
     self.is_new_attribute_allowed, #(request_type)
     )
```

## Using Database Object

```{code-block} python
# use the TANGO_HOST environment variable/tangorc config file
db = tango.Database()

# Using a specified host and port
db = tango.Database("other-db-host", 10000)
```

### Register a new device server

```{code-block} python
 dev = f'SR{sector:02}/VC/ALL'
 klass = 'PyStateComposer'
 server = klass + '/' + dev.replace('/', '_')

 di = tango.DbDevInfo()
 di.name, di._class, di.server = device, klass, server
 db.add_device(di)
```

### Remove "empty" servers from database

```{code-block} python
 tango = tango.Database()
 [tango.delete_server(s)
     for s in tango.get_server_list()
     if all(d.lower().startswith('dserver') for d in tango.get_device_class_list(s))
 ]
```

### Force unexport of a failing server

You can check using db object if a device is still exported after killed

```{code-block} python-console
>>> bool(db.import_device('dserver/HdbArchiver/11').exported)
True
```

You can unexport this device or server with the following call:

```{code-block} python
db.unexport_server('HdbArchiver/11')
```

It would normally allow you to restart the server again.

### Get all servers of a given class

```{code-block} python
 class_name = 'Modbus'
 list_of_names = ['/'.join((class_name,name)) for name in db.get_instance_name_list(class_name)]
```

Differences between DB methods:

```{code-block} python
get_instance_name_list(exec_name)  # return names of **instances**
get_server_list()  # returns list of all **executable/instance**
get_server_name_list()  # returns names of all **executables**
```

### Get all devices of a server or a given class

The command is:

```{code-block} python
 db.get_device_class_list(server_name)
 # returns: ['device/name/family', 'device_class'] * num_of_devs_in_server
```

The list returned includes the admin server
(*dserver/exec_name/instance*) that must be pruned from the result:

```{code-block} python
 list_of_devs = [dev for dev in db.get_device_class_list(server_name) if '/' in dev and not dev.startswith('dserver')]
```

### Get all devices of a given class from the database

```{code-block} python
 import operator
 list_of_devs = reduce(operator.add,(list(dev for dev in db.get_device_class_list(n) \
     if '/' in dev and not dev.startswith('dserver')) for n in \
     ('/'.join((class_name,instance)) for instance in db.get_instance_name_list(class_name)) \
     ))
```

### Get property values for a list of devices

```{code-block} python
 db.get_device_property_list(device_name,'*')  # returns list of available properties
 db.get_device_property(device_name,[property_name])  # returns {property_name : value}
```

```{code-block} python
 prop_names = db.get_device_property_list(device_name)
     ['property1','property2']
 dev_props = db.get_device_property(device_name,prop_names)
     {'property1':'first_value' , 'property2':'second_value' }
```

### Get the history (last ten values) of a property

```{code-block} python-console
 >>> [ph.get_value().value_string for ph in tango.get_device_property_history('some/alarms/device','AlarmsList')]
 [['MyAlarm:a/gauge/controller/Pressure > 1e-05', 'TempAlarm:a/nice/device/Temperature_Max > 130'],
```

### Get the server for a given device

```{code-block} python-console
 >>> print(db.get_server_list('Databaseds/*'))
 ['DataBaseds/2']
 >>> print(db.get_device_name('DataBaseds/2', 'DataBase'))
 ['sys/database/2']
 >>> db_dev=tango.DeviceProxy('sys/database/2')
 >>> print(db_dev.command_inout('DbImportDevice', 'et/wintest/01'))
 ([0, 2052], ['et/wintest/01', 'IOR:0100000017000xxxxxx', '4',
 'WinTest/manu', 'PCTAUREL.esrf.fr', 'WinTest'])
```

### Get the Info of a not running device (exported, host, server)

```{code-block} python
 def get_device_info(dev):
     vals = tango.DeviceProxy('sys/database/2').DbGetDeviceInfo(dev)
     di = dict((k,v) for k,v in zip(('name', 'ior', 'level', 'server', 'host', 'started', 'stopped'), vals[1]))
     di['exported'], di['PID'] = vals[0]
     return di
```

### Set property values for a list of devices

**Attention** , Tango property values are always inserted as lists!
{property_name : **\[** property_value **\]**}

```{code-block} python-console
>>> prop_name, prop_value = 'Prop1', 'Value1'
[db.put_device_property(dev,{prop_name:[prop_value]}) for dev in list_of_devs]
```

### Get Starter Level configuration for a list of servers

```{code-block} python
 [(si.name, si.mode, si.level) for si in [db.get_server_info(s) for s in list_of_servers]]
```

### Set Memorized Value for an Attribute

```{code-block} python
 db.get_device_attribute_property('tcoutinho/serial/01/Baudrate',['__value'])
 db.put_device_attribute_property('tcoutinho/serial/01/Baudrate',{'__value':VALUE})
```

## Useful constants and enums

```{code-block} python-console
 In [3]:tango.ArgType.values
 Out[3]:
{0: tango._tango.CmdArgType.DevVoid,
 1: tango._tango.CmdArgType.DevBoolean,
 2: tango._tango.CmdArgType.DevShort,
 3: tango._tango.CmdArgType.DevLong,
 4: tango._tango.CmdArgType.DevFloat,
 5: tango._tango.CmdArgType.DevDouble,
 6: tango._tango.CmdArgType.DevUShort,
 7: tango._tango.CmdArgType.DevULong,
 8: tango._tango.CmdArgType.DevString,
 9: tango._tango.CmdArgType.DevVarCharArray,
 10: tango._tango.CmdArgType.DevVarShortArray,
 11: tango._tango.CmdArgType.DevVarLongArray,
 12: tango._tango.CmdArgType.DevVarFloatArray,
 13: tango._tango.CmdArgType.DevVarDoubleArray,
 14: tango._tango.CmdArgType.DevVarUShortArray,
 15: tango._tango.CmdArgType.DevVarULongArray,
 16: tango._tango.CmdArgType.DevVarStringArray,
 17: tango._tango.CmdArgType.DevVarLongStringArray,
 18: tango._tango.CmdArgType.DevVarDoubleStringArray,
 19: tango._tango.CmdArgType.DevState,
 20: tango._tango.CmdArgType.ConstDevString,
 21: tango._tango.CmdArgType.DevVarBooleanArray,
 22: tango._tango.CmdArgType.DevUChar,
 23: tango._tango.CmdArgType.DevLong64,
 24: tango._tango.CmdArgType.DevULong64,
 25: tango._tango.CmdArgType.DevVarLong64Array,
 26: tango._tango.CmdArgType.DevVarULong64Array,
 28: tango._tango.CmdArgType.DevEncoded,
 29: tango._tango.CmdArgType.DevEnum,
 30: tango._tango.CmdArgType.DevPipeBlob,
 31: tango._tango.CmdArgType.DevVarStateArray}

In [4]: tango.AttrWriteType.values
Out[4]:
{0: tango._tango.AttrWriteType.READ,
 1: tango._tango.AttrWriteType.READ_WITH_WRITE,
 2: tango._tango.AttrWriteType.WRITE,
 3: tango._tango.AttrWriteType.READ_WRITE,
 4: tango._tango.AttrWriteType.WT_UNKNOWN}

In [5]: tango.AttrWriteType.values[3] is tango.READ_WRITE
Out[5]: True
```

## Using Tango Groups

This example uses PyTangoGroup to read the status of all devices in a Device Server

```{code-block} python
 server_name = 'VacuumController/AssemblyArea'
 group = tango.Group(server_name)
 devs = [d for d in tango.Database().get_device_class_list(server_name) if '/' in d and 'dserver' not in d]
 for d in devs:
     group.add(d)

 answers = group.command_inout('Status', [])
 for reply in answers:
     print(f'Device {reply.dev_name()} Status is:')
     print(reply.get_data())
```

## Passing Arguments to Device command_inout

When type of Arguments is *special* like **DevVarLongStringArray** the
introduction of arguments is something like:

```{code-block} python
 api.manager.command_inout('UpdateSnapComment', [[40], ['provant, provant...']])
```

## Using asynchronous commands

```{code-block} python
 import time

 cid = self.modbus.command_inout_asynch(command, arr_argin)
 while True:
     self.debug('Waiting for asynchronous answer ...')
     time.sleep(0.1)
     try:
         result = self.modbus.command_inout_reply(cid)
         self.debug(f'Received: {result}')
         break
     except tango.DevFailed as e:
         self.debug(f'Received DevFailed: {e}')
         if e.args[0]['reason'] != 'API_AsynReplyNotArrived':
            raise RuntimeException(f'Weird exception received!: {e}')
```

## Setting Attribute Config

```{code-block} python
 for server in astor.values():
     for dev in server.get_device_list():
         dp = server.get_proxy(dev)
         attrs = dp.get_attribute_list()
         if dev.rsplit('/')[-1].lower() not in [a.lower() for a in attrs]: continue
         conf = dp.get_attribute_config(dev.rsplit('/')[-1])
         conf.format = "%1.1e"
         conf.unit = "mbar"
         conf.label = f"{dev}-Pressure"
         print('setting config for {dev}/{conf.name}')
         dp.set_attribute_config(conf)
```
