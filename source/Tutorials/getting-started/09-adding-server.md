# Adding a new server to the Tango Database

In the [previous lesson](08-running-db) you saw how to run a Tango {term}`Databaseds`.
You could start `TangoTest` because the {term}`device` `sys/tg_test/1` and the `test` {term}`device server instance` were already defined in the database.

## Adding a server

If you want to run a new server, you first have to add the device and instance to the database.
Let's add our MegaCoffee3k server using `tango-admin`.


```console
(tango-tut) $ tango_admin --add-server MegaCoffee3k/test MegaCoffee3k sys/coffee/1
(tango-tut) ➜  tango-tut echo $?
0
```

:::{note}
The `tango_admin` command isn't very verbose. Even in case of failure, it won't print any error message. You need to print the return code to check if it succeeded (0) or not. If you set an invalid `TANGO_HOST`, the command will fail:

```console
(tango-tut) ➜  tango-tut TANGO_HOST=unknown:10000 tango_admin --add-server MegaCoffee3k/test MegaCoffee3k sys/coffee/1
(tango-tut) ➜  tango-tut echo $?
255
```
:::

Given the example from the [first steps](01-first-steps), you can run it using:

```{literalinclude} 01-first-steps/python/main.py
:caption: main.py
:language: python
```

```console
(tango-tut) $ python main.py test
Ready to accept request
```

`test` is the name of the instance you defined above.

If you try to start the server with another instance name, you'll get an error:

```console
(tango-tut) $ python main.py foo
The device server MegaCoffee3k/foo is not defined in database. Exiting!
```

You can't start a server which isn't defined in the database.

## Adding properties

If you take the example from [device properties](07-device-properties), and run it with `python main.py test`, you'll get the same error as when running PyTango's `test_context` the first time.

```{literalinclude} 07-device-properties/python/main.py
:caption: main.py
:language: python
```

This server requires a mandatory property that you need to define in the database. Let's add the `host` property using `tango_admin`:

```console
(tango-tut) $ tango_admin --add-property sys/coffee/1 host localhost
```

Now that the property is defined, you can start the server:

```console
(tango-tut) $ python main.py test
init_device before super: None:None @ None
init_device after super: localhost:9788 @ None
Ready to accept request
```

This server is using other properties. Let's change the port value using Jive.
Open Jive. Go to the `sys/coffee/1` device properties and click `New property`.
Enter `port` in the pop-up window.

```{image} 09-adding-server/img/jive-add-new-property.png
:alt: Jive Add new property
:align: center
```

Press `OK`. Click on the new property value column and enter the new value to overwrite the default.

```{image} 09-adding-server/img/jive-add-property-value.png
:alt: Jive Add property value
:align: center
```

Click `Apply`.

For the server to read the new property, you could just restart it.
Another way is to run the `Init` command. Let's do that from Jive as you have it opened.

```{image} 09-adding-server/img/jive-init.png
:alt: Jive Init command
:scale: 50%
:align: center
```

In the terminal where you started the Tango server, you should see the following output:

```console
init_device before super: localhost:9788 @ None
init_device after super: localhost:9700 @ None
```

The port defined in the database overwrites the default value defined in the code.

You saw that a server shall be defined in the database before to start it.
We used `tango_admin`, a simple command line tool, but it can also be done using [Jive](inv:jive:std#servers) or [json2tango](https://gitlab.com/MaxIV/lib-maxiv-dsconfig#json2tango).
