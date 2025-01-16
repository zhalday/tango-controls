# How to tune polling from inside device classes

```{tags} audience:developers, lang:all
```

It is possible to configure command or attribute polling from within a {term}`device class`, i. e. an instance
of `Tango::DeviceImpl`. The available functionality is similiar to the one found in `Tango::DeviceProxy`.

With them, you can:

  - Check if a command or attribute is polled
  - Start/Stop polling for a command or an attribute
  - Get or update the polling period for a polled attribute or command

:::::{tab-set}

::::{tab-item} C++
To display some information related to polling of the attribute named `TheAtt`:

```{code-block} cpp
:linenos: true

std::string att_name{"TheAtt"};
TANGO_LOG_DEBUG << "Attribute" << att_name;

if(is_attribute_polled(att_name))
{
   TANGO_LOG_DEBUG << " is polled with period " << get_attribute_poll_period(att_name) << " ms" << std::endl;
}
else
{
   TANGO_LOG_DEBUG << " is not polled" << std::endl;
}
```

To poll a command:

```{code-block} cpp
:linenos: true

poll_command("TheCmd", 250);
```

If the command is already polled, this method will update its polling
period to 250 ms.

Finally, to stop polling the same command:

```{code-block} cpp
:linenos: true

stop_poll_command("TheCmd");
```

All these DeviceImpl polling related methods are documented in the [DeviceImpl](https://tango-controls.gitlab.io/cppTango/10.0.0/classTango_1_1DeviceImpl.html) class documentation.

::::

::::{tab-item} Python

To display some information related to polling of the attribute
named `TheAtt` in a `DeviceImpl` class:

```{code-block} python
:linenos: true

att_name = "TheAtt"

if self.is_attribute_polled(att_name):
    print(f"{} is polled with period {} ms", att_name, self.get_attribute_poll_period(att_name))
else:
    print(f"{} is not polled", att_name)
```

To poll a command:

```{code-block} python
:linenos: true

self.poll_command("TheCmd", 250)
```

If the command is already polled, this method will update its polling
period to 250 ms.

Finally, to stop polling:

```{code-block} python
:linenos: true

self.stop_poll_command("TheCmd")
```

All these DeviceImpl polling related methods are documented in [DeviceImpl](inv:pytango:py:class#tango.LatestDeviceImpl).

::::

::::{tab-item} Java

The polling can be retrieved and modified from the DeviceManager class.

```{code-block} java
:linenos: true

import org.tango.server.annotation.Device;
import org.tango.server.annotation.DeviceManagement;
import org.tango.server.device.DeviceManager;
import fr.esrf.Tango.DevFailed;

@Device
public class Test {
    @DeviceManagement
    private DeviceManager deviceManager;
     ...
        final String attName = "TheAttr";
        if (deviceManager.isPolled(attName)) {
            System.out.println(attName + " is polled with period " + deviceManager.getPollingPeriod(attName) + " mS");
        } else {
            System.out.println(attName + " is not polled");
        }
        deviceManager.startPolling("TheCmd", 250);
        deviceManager.stopPolling("TheCmd")
        ...

   public void setDeviceManager(final DeviceManager deviceManager) {
        this.deviceManager = deviceManager;
    }
}
```

::::

:::::
