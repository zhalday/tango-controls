```{raw} latex
\clearpage
```

# Write your first Tango client

```{tags} audience:developers, lang:all
```

Below is an example of how to write a client to connect to a Tango device and
interact with it:

:::::{tab-set}

::::{tab-item} C++

```{code} cpp
:number-lines: 1

  /*
   * Example of a client using the Tango C++ api.
   */
  #include <tango.h>

  using namespace Tango;

  int main(unsigned int argc, char **argv)
  {
      try
      {
        // Create a connection to a Tango device
        DeviceProxy *device = new DeviceProxy("sys/tg_test/1");

        // Ping the device
        device->ping();

        // Execute a command on the device and extract the reply as a string
        string db_info;
        DeviceData cmd_reply;
        cmd_reply = device->command_inout("DbInfo");
        cmd_reply >> db_info;
        cout << "Command reply " << db_info << endl;

        // Read a device attribute (string data type)
        string spr;
        DeviceAttribute att_reply;
        att_reply = device->read_attribute("StoredProcedureRelease");
        att_reply >> spr;
        cout << "Database device stored procedure release: " << spr << endl;
      }
      catch (DevFailed &e)
      {
        Except::print_exception(e);
        exit(-1);
      }
  }
```

::::

::::{tab-item} Python

```{code} python
:number-lines: 1

'''
Example of a client using the Tango Python api (PyTango).
'''
import tango

try:
    # Create a connection to a Tango device
    tango_test = tango.DeviceProxy("sys/tg_test/1")

    # Ping the device
    print(f"Ping: {tango_test.ping()}")

    # Execute a command on the device and extract the reply as a string
    result = tango_test.command_inout("DbInfo", "First hello to device")
    print(f"Result of execution of DbInfo command = {result}")

    # Read a device attribute (string data type)
    procedure_release = tango_test.read_attribute("StoredProcedureRelease")
    print(f"Database device stored procedure release = {procedure_release.value}")

except DevFailed as df:
    print(f"Failure: {df}")
```
::::
