# Run a device server with an active Windows firewall

```{tags} audience:administrators, audience:developers
```

When running Tango {term}`device servers <device server>` on a Windows
PC with an active firewall you might have some problems trying to
reconnect to a restarted server. In some cases the client will never reconnect.

This behavior is due to the device server port being automatically closed
when the process stops running. In this case the client only receives a
timeout exception on the blocked port instead of the expected "connection
failed" exception which would trigger a reconnection.

When a device server is restarted it will dynamically open another port and new
clients are able to connect to the new port, however old clients might not.

To overcome this problem, start your device server with a fixed port
(port 11000 in this example):

```console
TangoTest win -ORBendPoint giop:tcp11000
```

and open the fixed port in the firewall with:

```console
Netsh firewall add portopening TCP 11000 TangoTest
```

You can verify the open ports for the firewall with:

```console
Netsh firewall show portopening
```

which should yield the the following output:

```output
Port configuration for Domaine profile:

Port     Protocol    Mode       Name

-----------------------------------------------------------------------------

11000    TCP         Enable     TangoTest
```
