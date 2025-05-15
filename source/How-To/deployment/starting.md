(starting-tango)=

# Starting a Tango control system

```{tags} audience:all
```

## With a database

Starting the Tango control system simply means starting its {term}`database <Tango Database>`
device server on a well defined host using a well defined port. Use the
host name and the port number to build the {term}`TANGO_HOST` environment
variable. See the [](#running-cpp-device-server) section
on how to do this. Note that the underlying database server must
be started before the Tango database device server. The Tango database
server connects to database server using a default login name set to `root`. You
can change this behaviour with the `MYSQL_USER` and `MYSQL_PASSWORD`
environment variables. Define them before starting the database server.
All tango environment variables can also be set in the {term}`tangorc` configuration file.

An example tango rc file `/etc/tangorc`:

```{code} ini
MYSQL_USER=dbuser
MYSQL_PASSWORD=secret
TANGO_HOST=my-hostname.eu:10000
```

If you are using the Tango administration graphical tool called
[Astor](#astor-manual), you also need to start a specific Tango device server called
[Starter](#Starter) on each host where Tango device server(s) are running. This Starter
device server is able to start even before the Tango database device
server is started. In this case, it will enter a loop in which it
periodically tries to access the Tango database device. The loop exits
and the server starts only if the database device access succeeds.

## Without a database

When used without a database, there is no additional process to start.
Simply start a device server using the `-nodb` option (and eventually the
`-dlist` option) on a specific port using `-ORBendPoint`. See [](#device-server-without-database) to find
information on how to write and start a Tango device server without using the
database.

## With a file used as a database

When used with a {term}`File Database`, there is no additional process to
start. Simply start a device server using the `-file` option specifying the
file and `-ORBendPoint` for the port. See [](#device-server-with-filedatabase)
to find information on how to start Tango device server using a database on file.

## With TAC (Tango Access Control)

:::{warning}
This is client side only and **not** secure. Use that only to prevent accidental changes to tango device servers
and not for security.
:::

Using the Tango controlled access means starting a specific device
server called `TangoAccessControl`. By default, this server has to be
started with the instance name set to 1 and its device name is
`sys/access_control/1`. The command to start this device server is:

```{code}
  TangoAccessControl 1
```

This server connects to MariaDB using a default login name set to `root`.
As mentioned above, you can change this behaviour with the `MYSQL_USER` and `MYSQL_PASSWORD`
environment variables. Define them before starting the controlled access
device server. This server also uses the `MYSQL_HOST` environment
variable if you need to connect it to some MySQL server running on
another host. The syntax of this environment varaible is `host:port`. The port
is optional and if it is not defined, the MariaDB default port is used
(3306). If it is not defined at all, a connection to the localhost is
made. This controlled access system uses the Tango database to retrieve
user rights and it is not possible to run it in a Tango control system
running without a database.
