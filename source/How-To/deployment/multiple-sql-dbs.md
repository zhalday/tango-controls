{audience}`administrators`

(multiple-sql-dbs)=

# Multiple database servers within a Tango control system

Tango uses MySQL as database and allows access to this database via a
specific Tango device server. It is possible for the same Tango control
system to have several Tango database servers. The host name and port
number of the database server is known via the TANGO_HOST environment
variable. If you want to start several database servers in order to
prevent server crash, use the following TANGO_HOST syntax

TANGO_HOST=\<host_1>:\<port_1>,\<host_2>:\<port_2>,\<host_3>:\<port_3>

All calls to the database server will automatically switch to a running
servers in the given list if the one used dies.
