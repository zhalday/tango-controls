```{tags} audience:all
```

(tangodb-explanation)=

# Tango Database

%[glossary_term][Tango Database]
%A combination of the Tango device server *Databaseds* and a MariaDB backend. It provides static and runtime configuration information about Tango Controls components in a Tango Controls system. It is used by the *Databaseds* device server and constitutes the {term}`Tango Host`.

%[glossary_term][TANGO_HOST]
%An environment variable that specifies on which host and port a Databaseds device server is running. The host part and port are separated by a colon `:`. Commonly this is also referred to as the TangoDB.

%[glossary_term][TangoDB]
%A shorter way to say Tango Databaseds device server and its MariaDB backend.

%[glossary_term][Databaseds]
%The Tango device server of the :term:`TangoDB`.

The Tango Database, also referred to as TangoDB, is a service mainly used for name lookup and static and runtime configuration storage for the control system. The Tango Database itself is found by clients and servers via the environment variable `TANGO_HOST`. It is possible to run multiple databases for load-balancing and fault-tolerance, see [](#multiple-sql-dbs), and also to run servers without database, see [](#device-server-without-database).

The part of the Tango Database that offers an API is implemented as a [device server](#deviceserver) and should always be running. It is abbreviated as `TDB` in the following paragraphs.

## Name lookup

When a device server starts it registers itself with the TDB. For this to work the [device name](#tango-object-naming) has to be added to the TDB before with tools like [Jive](inv:jive:std#index) or [tango_admin](#tango-admin). This is called device exporting/unexporting, see the [RFC](https://gitlab.com/tango-controls/rfc/-/blob/main/6/Database.md#device-export-and-unexport-protocols) for the details. The device server unregisters itself automatically on shutdown from the TDB.

The device registration allows to abstract-away the location of the device server. So when the device server moves from `hostA` to `hostB` this is completely invisible to the client.

## Alias handling

It is possible to introduce alternative names for devices and attributes and this mapping is also stored in the TDB. See [Alias names](#alias-names) for an in-depth explanation and the [howto](#alias-howto) for some examples on how to use them.

## Configuration storage

The TDB can also act as a key-value store for storing persistent device server data. The `keys` are called [properties](#properties) in Tango and the `values` are strings. As the properties an be read by anyone, no sensitive data should be stored in them.

The previous values of properties are also kept in the database for informative purposes. The default depth of the history is `10` and can be controlled with the `historyDepth` device property. The history is deleted when a property is deleted.
