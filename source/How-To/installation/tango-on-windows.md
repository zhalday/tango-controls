# Windows

{audience}`developers, administrators`

If you need a full-fledged installation on Windows with Tango Database and JAVA tools like Jive,
ATK, etc. use the Windows Installer. If you are just looking for precompiled cppTango libraries, head over
to the [](#cppTango-windows-binaries) section.

We don't describe compiling cppTango from source here as that is very involved and rarely needed. Head over to the
[cppTango repository](https://gitlab.com/tango-controls/cppTango/-/blob/main/INSTALL.md?ref_type=heads#building-on-windows) for
the gritty details.

The packages are tested and build against Windows 10, but should work on earlier versions as well.

## Tango installer package

Download the `Windows installer` from the [TangoSourceDistribution
releases](https://gitlab.com/tango-controls/TangoSourceDistribution/-/releases) page and execute it.

This packages includes a lot of the default tango tools, but not the MariaDB/MySQL database server.

### Configure the `TANGO_HOST` environment variable

For Windows 10 and 11 you need to do:

  - From the Desktop, right-click the very bottom left corner of the screen to get the `Task Menu`.
  - From the `Task Menu`, click `System`.
  - Click the `Advanced System Settings` link in the left column.
  - In the System Properties window, click on the `Advanced` tab,
    then click the `Environment Variables` button near the bottom of that tab.
  - In the `Environment Variables` window click the `New` button.
  - In the field `Name` write `TANGO_HOST`.
  - In the field `Value` write proper value.

If it is the only computer in the Tango System provide `localhost:10000`.

If there is a `Tango Host` already running on some other computer in your deployment and you have provided proper
address and port in the `TANGO_HOST` you may start using client and management applications like `Jive`,
`Jdraw`/`Synoptic`. In other case you have to configure the system to perform a role of `Tango Host`.

## Tango Host role

To make a computer become a Tango Host you need to:

### Install MariaDB server

You may use community version available from <https://mariadb.com/downloads>.

It is suggested to create dedicated `tango` user with *DB Admin* priviledges during installation.
In the installation wizard on a tab `Accounts and Roles` select button `Add User`
and create a dedicated user.

Set up environment variables providing credentials to access MariaDB:

  - Open `Command Line`

  - Invoke command: `%TANGO_ROOT%\\bin\\dbconfig.exe`

    :::{note}
    This lets you set up two environment variables
    `MYSQL_USER` and `MYSQL_PASSWORD` used to access the MariaDB server. You can check if variables
    were set correctly, if not you can set it manually. It's recommended to restart computer after operation.
    You may use `root` credentials provided upon MariaDB installation if it is your development workstation.
    For production environment it is
    suggested to create an additional user with `DB Admin` privileges. On Windows you may use `MariaDB Installer`
    from `Start` menu and select the option `Reconfigure` for MariaDB Server.
    Please refer to: <http://dev.MariaDB.com/doc/refman/5.7/en/adding-users.html>
    :::

  - Populate database with an initial Tango configuration:

      - Open `Command Line`

      - Add MariaDB client to be available in the PATH. For version 5.7 the command should be:
        `set PATH=%PATH%;"C:\\Program Files\\MariaDB\\MariaDB Server 5.7\\bin"`

        :::{note}
        Adjust the path according to your MariaDB version and the path where it is installed.
        :::

      - Invoke `cd "%TANGO_ROOT%\\share\\tango\\db\\"`

      - Call `create_db.bat`

- Start a `DataBaseds` `device server`:

    - Open a new command line window.

    - In the command line call `"%TANGO_ROOT%\\bin\\start-db.bat"`.

      :::{note}
      To make your Tango installation operational you have to have this `DataBaseds` running permanently.
      You may either add the command above to `Autostart` or run it as a service.
      :::

- Make `DataBaseds` run as a service
    :::{note}
    The proposed solution uses NSSM tool which works on all versions of Windows but you may find some other tools
    available including native srvany.exe.
    :::

    - Download NSSM from <http://nssm.cc/>

    - Unpack the file to some convenient location. It is suggested to copy proper (32bit or 64bit) version to the
      Tango bin folder `%TANGO_ROOT%\\bin\\`.

    - Open `Command Line` as `Administrator`.

    - Change current path to where the `nssm` is unpacked or copied, eg. `cd "%TANGO_ROOT%\\bin"`.

    - Invoke `nssm.exe install Tango-DataBaseds`. This will open a window where you can define service parameters.

      - In the Application tab provide information as follows (adjust if your installation path is different).

        ```{image} tango-on-windows/databaseds-as-service-01.png
        ```

      - In the Environment tab provide variables with credentials used for accessing the MariaDB, like:

        ```{image} tango-on-windows/databaseds-as-service-02.png
        ```

      - Click `Install Service`.

      - Invoke `nssm.exe start Tango-DataBaseds` to start the service.

      - Test if everything is ok. Use `Start` menu to run Jive or in command line call
        `"%TANGO_ROOT%\\bin\\start-jive.bat"`.

## Running Device Servers

The recommended way of running device servers is to use [Starter](#Starter) service.
Then you may use `NSSM` as for `DataBaseds`.
Assuming you have downloaded it and copied to the Tango bin folder please follow:

- Open Command Line as Administrator (if it is not yet open)

- Prepare folder for `Device Servers` executable:

:::{note}
To let your device servers start with `Starter` service their executables have to be in a path without
spaces. This is a limitation of the current `Starter` implementation.
:::

- Create a directory for `Device Servers`. Let it be `C:\\DeviceServers\\bin`
  with `mkdir c:\\DeviceServers\\bin`
- Change to the Tango bin directory with command (`cd "%TANGO_ROOT%\\bin"`)
- Copy `TangoTest` `device server` to the newly crated folder:
  `copy TangoTest.exe c:\\DeviceServers\\bin`

- Add entry about the Starter device server you will start on your computer:
  - Start a tool called `Astor`. You may use either Windows `Start` menu or
    call `tango-astor.bat`

  - In `Astor` window select menu `&Command --> Add a New Host`

  - In the form that appears provide your `Host name` and `Device Servers PATH`.

    ```{image} tango-on-windows/starter-01.png
    ```

  - Accept with `Create`

  - Go back to `Command Line`

(windows-starter-nssm)=

- Install Starter service:

  : - Invoke `nssm.exe install Tango-Starter`.

    - In the Application tab provide information as follows:

      ```{image} tango-on-windows/starter-as-service-01.png
      ```

    Adjust if your installation path is different. In `Arguments` exchange `pg-dell-new` with the proper name
    of your host.

    - In the Environment tab provide TANGO_HOST variable, like:

      ```{image} tango-on-windows/starter-as-service-02.png
      ```

    - Click `Install service`

    - Start the service: `nssm.exe start Tango-Starter`.

    - Go back to `Astor`.

    - After a while you will see a green led next to your host name:

      ```{image} tango-on-windows/starter-02.png
      ```

- Run `TangoTest` device server:

  You may test the configuration by starting prefigured TangoTest device.

  - Start `Astor` if it is not running.

    ```{image} tango-on-windows/device-server-01.png
    ```

  - Double Click on your computer name to open `Control Panel`. It opens a window as below:

    ```{image} tango-on-windows/device-server-02.png
    ```

  - Click `Start new`.

  - In the open window select {menuselection}`TangoTest/test`:

    ```{image} tango-on-windows/device-server-03.png
    ```

  - Click `Start Server`.

  - In the open window select `Controlled by Astro -> Yes`, and `Startup Level -> Level 1`.

    ```{image} tango-on-windows/device-server-04.png
    ```

  - When you click `OK` it should start the server. After a while you should see:

    ```{image} tango-on-windows/device-server-05.png
    ```

- Running your `Device Servers <device server>`:
  : - You need to copy an executable to the folder configured for `Starter`. In our example it is
      `C:\\DeviceServers\\bin`.
    - Then use `Astor`. After opening `Control panel` for your computer (double clicking on a label)
      and selection `Start New`...
    - Select `Create New Server` and follow a wizard.

(cppTango-windows-binaries)=

## cppTango binaries for windows

There are zip and msi packages available. Download the appropriate package from the [cppTango release](https://gitlab.com/tango-controls/cppTango/-/releases) page.
If in doubt you should prefer the `XXX_x64_shared_release.zip` packages. If you need opentelemetry support, you currently have to use the `static` packages.

Regarding linkage against the Visual Studio runtime libraries, the static cppTango library links **statically**
against the VC libraries and the dynamic library links **dynamically** against it.
