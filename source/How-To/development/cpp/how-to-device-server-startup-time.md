# How to reconnect to the Tango HOST at device server startup time

```{tags} audience:developers, lang:c++
```

The following C++ snippet shows how to allow the {term}`Device Server` to start before the {term}`Tango Host`
is available. In this mode the device server will wait until it can reach the tango host. This mode of operation
does not make sense to combine with the {term}`File Database` as that is always immediately available.

Set `_daemon` and `_sleep_between_connect` from `Tango::Util` before initialization in the `main` function.
This function is located in `main.cpp` when the device server was generated with {term}`Pogo`:

```{code-block} cpp
:linenos: true

  int main(int argc, char *argv[])
  {
    // Set an automatic retry on database connection
    //----------------------------------------------
    Tango::Util::_daemon = true;
    Tango::Util::_sleep_between_connect = 5;

    // Initialize the device server
    //--------------------------------
    tg = Tango::Util::init(argc, argv);

    ...
  }
```

The device server will retry to connect to the tango host in case of failures
periodically. The retry interval is here set to 5 seconds, it defaults to 60 seconds.
