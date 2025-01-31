```{tags} audience:administrators
```

(multiple-db-hosts)=

# Use multiple database servers within a Tango control system

The database device server, TangoDatabase in most cases, serves as the {term}`Tango Host` in a control system. The
host name and port number of the database server is known via the {term}`TANGO_HOST` environment variable. If
you want to use several tango hosts in order to handle one being unreachable (either due to a network outage, a
crash or a hardware issue), use the following `TANGO_HOST` syntax:

```text
TANGO_HOST=<host_1>:<port_1>,<host_2>:<port_2>,<host_3>:<port_3>
```

All calls to the database server will switch automatically and transparently to a running
server in the given list if the one used is not reachable.
