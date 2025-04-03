# Running a Tango Database

So far, we have been running our Tango device server, using PyTango's `test_context` utility to run with `nodb`.
This is very useful during development but has some limitations.
You can't interact with your server using jive for example.

The official [Tango Database](https://gitlab.com/tango-controls/TangoDatabase) is written in C++ and requires MariaDB as backend.

PyTango contains its own [Database implementation](inv:pytango:std#databaseds), which should work as a drop-in replacement. It stores data using SQLite so it has no external dependencies, making it easier to run. This is what we will use in this tutorial.

:::{warning}
This implementation is in an experimental state, and has not been extensively tested for compatibility or for performance. Don’t use it for anything mission critical!
:::


## Running PyTango Database Device Server

Using our existing environment with pytango 10:

```console
(tango-tut) $ TANGO_HOST=localhost:10000 python -m tango.databaseds.database 2
Ready to accept request
```

That's it!

If you already have a {term}`Databaseds` running on port 10000, you can pick another port (like 11000).

:::{note}
The previous command will create a file named `tango_database.db` in the current directory.
This is the file containing the SQLite database.
You can change the name of that file with the `PYTANGO_DATABASE_NAME` environment variable.
:::

::::{admonition} Bonus tip: `pytango-db`
:class: dropdown, tip
The PyTango Database Device Server code has been forked to a separate [repository](https://gitlab.com/tango-controls/incubator/pytango-db) for easier development.
It makes it easy to use even if you don't work with pytango 10.

Install `pytango-db` globally with pixi:

```console
$ pixi global install pytango-db
Global environments as specified in '~/.pixi/manifests/pixi-global.toml'
└── pytango-db: 0.3.0 (installed)
    └─ exposes: PyDatabaseds
```

In a terminal, run:

```console
$ TANGO_HOST=localhost:10000 PyDatabaseds 2
Ready to accept request
```
::::

## Checking the Database Device Server

### Using pytango from the command line

Start the python interpreter after setting the `TANGO_HOST` variable to point to the running Database server.

```console
(tango-tut) ➜  tango-tut TANGO_HOST=localhost:10000 python
```

To interact with a Tango Database from PyTango, you use the [tango.Database](inv:pytango:py:class#tango.Database) class, which provides methods for all database commands.

Try it and query the database for some general information about the tables:

```python-console
>>> import tango
>>> db = tango.Database()
>>> print(db.get_info())
TANGO Database tango_database.db

Running since ...2025-04-10 13:17:37

Devices defined = 8
Devices exported = 2
Device servers defined = 4
Device servers exported = 1

Device properties defined = 0 [History lgth = 0]
Class properties defined = 53 [History lgth = 0]
Device attribute properties defined = 0 [History lgth = 0]
Class attribute properties defined = 0 [History lgth = 0]
Object properties defined = 0 [History lgth = 0]
```

If this worked, you connected properly to a Tango Database!
Otherwise, see the troubleshooting tip below.

::::{admonition} Troubleshooting errors when instantiating tango.Database()
:class: dropdown, tip

If you forgot to set the `TANGO_HOST` variable or set it to an invalid value,
instantiating `tango.Database()` will raise an exception:

```python-console
>>> db = tango.Database()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/username/tango-tut/.pixi/envs/default/lib/python3.12/site-packages/tango/db.py", line 92, in __Database____init__
    return Database.__init_orig__(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PyTango.DevFailed: DevFailed[
DevError[
    desc = TANGO_HOST env. variable not set, set it and retry (e.g. TANGO_HOST=<host>:<port>)
  origin = Tango::Database::Database(CORBA::ORB_var) at (/Users/runner/miniforge3/conda-bld/cpptango_1742400675684/work/src/client/dbapi_base.cpp:78)
  reason = API_TangoHostNotSet
severity = ERR]
```

To use `tango.Database()` without arguments, make sure to export the `TANGO_HOST` variable.

You can also pass the hostname and port directly to the `Database()` class.

```python-console
>>> db = tango.Database("localhost", 10000)
```
::::

Many more commands are available. You can for example list the servers registered in the database:

```python-console
>>> db.get_server_list()
DbDatum(name = 'server', value_string = ['DataBaseds/2', 'DataBaseds/pydb-test', 'TangoAccessControl/1', 'TangoTest/test'])
```

See the [Database API](inv:pytango:py:class#tango.Database) for more information.

### Using Jive

Another way to interact with the Tango Database is using [Jive](inv:jive:std#index).

Jive is a java application and it's already installed in our pixi environment for this tutorial.

::::{admonition} Bonus tip: Install Jive globally
:class: dropdown, tip
As Jive is a very common tool and standalone java application, you might want to install it globally to not depend on a specific environment. You can use `pixi global` for that purpose.

```console
$ pixi global install jive
Global environments as specified in '/Users/username/.pixi/manifests/pixi-global.toml'
└── jive: 7.45 (installed)
    └─ exposes: jive
```

That will make the `jive` command available globally, without having to activate any environment.
::::

As before with PyTango, you need to set the `TANGO_HOST` variable to tell the application where the Database is running.

```console
(tango-tut) $ TANGO_HOST=localhost:10000 jive
```

You should be able to see the predefined servers in the database: `DataBaseds`, `TangoAccessControl` and `TangoTest`.

You can access `sys/database/2`, but `sys/tg_test/1` isn't exported because `TangoTest` isn't running.

```{image} 09-running-db/img/jive-tangotest-not-exported.png
:alt: Jive TangoTest not exported
:align: center
```

::::{admonition} Troubleshooting errors when starting Jive
:class: dropdown, tip

If you get the following error when running `jive`, then the database isn't running on the given port or host. Check that you used the same `TANGO_HOST` when starting the database and Jive.

```{image} 09-running-db/img/jive-no-tangodb.png
:alt: Jive Connection to Database failed
:align: center
```

::::

### Running TangoTest

Now that we have a Tango Database running, we can start `TangoTest` (the `test` instance is already defined in the database).

In another terminal, run:

```console
(tango-tut) $ TANGO_HOST=localhost:10000 TangoTest test
```

As you started `TangoTest` after Jive, you have to refresh the tree:

```{image} 09-running-db/img/jive-refresh-tree.png
:alt: Jive Refresh tree
:scale: 50%
:align: center
```

You can now test the device by sending commands or reading/writing attributes.

```{image} 09-running-db/img/jive-test-device.png
:alt: Jive Test device
:scale: 50%
:align: center
```

```{image} 09-running-db/img/jive-tangotest-status.png
:alt: Jive TangoTest status
:scale: 50%
:align: center
```

You can of course use PyTango [DeviceProxy](inv:pytango:py:class#tango.DeviceProxy) to check the status or any attribute:

```python-console
>>> import tango
>>> dp = tango.DeviceProxy("sys/tg_test/1")
>>> dp.Status()
'The device is in RUNNING state.'
>>> dp.double_scalar
161.10643365358285
```

If you don't need `TangoTest`, you can enter `CTRL-C` in your terminal to stop it.

## Summary

You now know how to start a Tango `DatabaseDS` for local development and how to interact with it using PyTango or Jive.
We'll see next how to add a new device to the database.
