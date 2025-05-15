(user-loop)=

# Device server with user defined event loop

```{tags} audience:developers, lang:c++
```

Sometimes, it could be useful to write your own process event handling loop. For instance, this feature can be
used in a device server process where the ORB is only one of several components that must perform event
handling. A device server with a graphical user interface for example must allow the GUI to handle windowing events
in addition to allowing the ORB to handle incoming requests. These types of device servers therefore perform
non-blocking event handling. They turn the main thread of control over each of the various event-handling
sub-systems while not allowing any of them to block for significant amount of time. The `Tango::Util` class
has a method called `server_set_event_loop()` to deal with such a case. This method has only one argument
which is a function pointer. This function does not receive any argument and returns a boolean. If this
boolean is true, the device server process exits. The device server core will call this function in a loop
without any sleeping time between the call. It is therefore the user's responsibility to implement in this
function some kind of sleeping mechanism in order not to make this loop too CPU consuming. The code of this
function is executed by the device server main thread.

The following piece of code is an example of how this feature can be used.

```{code} cpp
:number-lines: 1

  bool my_event_loop()
  {
     some_sleeping_time();

     bool ret = handle_gui_events();

     // DS will exit when returning true
     return ret;
  }

  int main(int argc,char *argv[])
  {
     Tango::Util *tg;
     try
     {
        // Initialise the device server
        //----------------------------------------
        tg = Tango::Util::init(argc, argv);

        tg->set_polling_threads_pool_size(5);

        // Create the device server singleton
        //        which will create everything
        //----------------------------------------
        tg->server_init(false);

        tg->server_set_event_loop(my_event_loop);

        // Run the endless loop
        //----------------------------------------
        TANGO_LOG << "Ready to accept request" << endl;
        tg->server_run();
     }
     catch (std::bad_alloc&)
     {
     ...
```

The device server main event loop is set at line 27 before the call to
the Util::server_run() method. The function used as server loop is
defined between lines 1 and 9.
