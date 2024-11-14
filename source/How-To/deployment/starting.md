(starting-tango)=

# Starting a Tango control system

```{tags} audience:all
```

## Without database

When used without database, there is no additional process to start.
Simply starts device server using the -nodb option (and eventually the
-dlist option) on specific port. See [](#run-without-sql-db) to find
information on how to start/write Tango device server not using the
database.

## With database

Starting the Tango control system simply means starting its database
device server on a well defined host using a well defined port. Use the
host name and the port number to build the TANGO_HOST environment
variable. See [environment variable](#running-cpp-device-server) to find how starting a device server on a
specific host. Obviously, the underlying database software (MySQL) must
be started before the Tango database device server. The Tango database
server connects to MySQL using a default logging name set to root. You
can change this behaviour with the MYSQL-USER and MYSQL-PASSWORD
environment variables. Define them before starting the database server.

If you are using the Tango administration graphical tool called
[Astor](#astor-manual), you also need to start a specific Tango device server called
[Starter](#Starter) on each host where Tango device server(s) are running. This starter
device server is able to start even before the Tango database device
server is started. In this case, it will enter a loop in which it
periodically tries to access the Tango database device. The loop exits
and the server starts only if the database device access succeed.

## With file used as database

When used with database on file, there is no additional process to
start. Simply starts device server using the -file option specifying
file name port. See [Device server using file as database](#device-server-with-filedatabase)
to find information on how
to start Tango device server using database on file.

## With the controlled access

Using the Tango controlled access means starting a specific device
server called TangoAccessControl. By default, this server has to be
started with the instance name set to 1 and its device name is
sys/access_control/1. The command line to start this device server is:

```{code} cpp
:number-lines: 1

  TangoAccessControl 1
```

This server connects to MySQL using a default logging name set to root.
You can change this behaviour with the MYSQL_USER and MYSQL_PASSWORD
environment variables. Define them before starting the controlled access
device server. This server also uses the MYSQL_HOST environment
variable if you need to connect it to some MySQL server running on
another host. The syntax of this environment varaible is host:port. Port
is optional and if it is not defined, the MySQL default port is used
(3306). If it is not defined at all, a connection to the localhost is
made. This controlled access system uses the Tango database to retrieve
user rights and it is not possible to run it in a Tango control system
running without database.
