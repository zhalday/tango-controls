(systemd-integration)=

# Use Tango with systemd integration

```{tags} audience:administrators
```
It is useful to be able to automate the process of starting the necessary parts of the Tango Control System. For this purpose, it is recommended to create the system services.

In the case where Tango has been installed from a .deb package or is running in a Docker container, the package or the image provides thses services.

However, if Tango has been installed from scratch then the services and daemon have to be created manually.

There are a few server-side elements of the Tango environment that will want to be started in this way.

## Tango DB Service

Create a service to start the MariaDB database. This can be done by creating a file named **tango-db.service** under the `/etc/systemd/system/` directory. An example of the contents of this file is shown below:


:::{dropdown} tango-db.service
```ini
# /etc/systemd/system/tango-db.service
[Unit]
Description = Tango DB
Requires=mariadb.service
After=mariadb.service

[Service]
User=<user>
Environment=TANGO_HOST=<tango_host:port>
Environment=MYSQL_USER=<mysql_user>
Environment=MYSQL_PASSWORD=<mysql_pwd>
ExecStart=<path/to/DataBaseds> 2 -ORBendPoint giop:tcp::10000
# Give a reasonable amount of time for the server to start up/shut down
TimeoutSec=10

[Install]
WantedBy=tango.target
```

The above example starts MariaDB. If you are using a MySQL database then you will need to modify the above example with:

```ini
Requires=mysqld.service
After=mysqld.service
```

Replace:
- `<user>`: your username (e.g. tango)
- `<tango_host:port>`: TANGO_HOST varible as IP:PORT (e.g. localhost:10000)
- `<mysql_user>`: configured when setting up MariaDB/MySQL (e.g. root)
- `<mysql_pwd>`: configured when setting up MariaDB/MySQL (e.g. tango)
- `<path/to/DataBaseds>`: e.g. /usr/local/tango/bin/DataBaseds

:::

To have this service start automatically at machine boot time, run the `enable` command and then `start` the service:

```console
sudo systemctl enable tango-db
sudo systemctl start tango-db
```

```{note}
Note that if you later make changes to the .service file you will need to reload with:
```{code}
sudo systemctl daemon-reload
```

## Tango Access Control Service

Create a service to start the Tango access control. This can be done by creating a file named **tango-accesscontrol.service** under the `/etc/systemd/system/` directory. An example of the contents of this file is shown below:

:::{dropdown} tango-accesscontrol.service
```ini
# /etc/systemd/system/tango-accesscontrol.service
[Unit]
Description=TangoAccessControl device server
Wants=tango-db.service
After=tango-db.service

[Service]
Environment=TANGO_HOST=<tango_host:port>
Environment=MYSQL_USER=<mysql_user>
Environment=MYSQL_PASSWORD=<mysql_pwd>
ExecStart=<path/to/TangoAccessControl> 1

[Install]
WantedBy=tango.target
```

Replace:
- `<tango_host:port>`: TANGO_HOST varible as IP:PORT (e.g. localhost:10000)
- `<mysql_user>`: configured when setting up MariaDB/MySQL (e.g. root)
- `<mysql_pwd>`: configured when setting up MariaDB/MySQL (e.g. tango)
- `<path/to/TangoAccessControl>`: e.g. /usr/local/tango/bin/TangoAccessControl
:::

We also need to create a timer to make sure that the TangoDB is ready to accept requests before we start Tango access control. Create a file named **tango-accesscontrol.timer** under the `/etc/systemd/system/` directory. An example of the contents of this file is shown below:

:::{dropdown} tango-accesscontrol.timer
```ini
# /etc/systemd/system/tango-accesscontrol.timer
[Timer]
OnActiveSec=3

[Install]
WantedBy=tango.target
```
:::

To have this service and timer start automatically at machine boot time, run the `enable` command and then `start` the service:

```console
sudo systemctl enable tango-accesscontrol
sudo systemctl enable tango-accesscontrol.timer

sudo systemctl start tango-accesscontrol
```

```{note}
Note that if you later make changes to these files you will need to reload with:
```{code}
sudo systemctl daemon-reload
```

## Tango Starter Service

Create a service to start the Tango Starter. This can be done by creating a file named **tango-starter.service** under the `/etc/systemd/system/` directory. An example of the contents of this file is shown below:

:::{dropdown} tango-starter.service
```ini
# /etc/systemd/system/tango-starter.service
[Unit]
Description=Starter device server
After=tango-accesscontrol.service
Requires=tango-db.service
Requires=tango-accesscontrol.service

[Service]
Restart=always
RestartSec=10
User=<user>
Environment=TANGO_HOST=<tango_host:port>
ExecStart=<path/to/Starter> <device>

[Install]
WantedBy=tango.target
```

Replace:
- `<user>`: your username (e.g. tango)
- `<tango_host:port>`: TANGO_HOST varible as IP:PORT (e.g. localhost:10000)
- `<path/to/Starter>`: e.g. /usr/local/tango/bin/Starter
- `<device>`: name of the Starter device to start. See [](#Starter) on how to create this device.
:::

We also need to create a timer to make sure that the TangoDB is ready to accept requests before we start the Tango Starter device. Create a file named **tango-starter.timer** under the `/etc/systemd/system/` directory. An example of the contents of this file is shown below:

:::{dropdown} tango-starter.timer
```ini
# /etc/systemd/system/tango-starter.timer
[Timer]
OnActiveSec=3

[Install]
WantedBy=tango.target
```
:::

To have this service and timer start automatically at machine boot time, run the `enable` command and then `start` the service:

```console
sudo systemctl enable tango-starter
sudo systemctl enable tango-starter.timer

sudo systemctl start tango-starter
```

```{note}
Note that if you later make changes to these files you will need to reload with:
```{code}
sudo systemctl daemon-reload
```

## Combined single target

Finally combine everything into a single target by creating a file named **tango.target** under the `/etc/systemd/system/` directory. An example of the contents of this file is shown below:

:::{dropdown} tango.target
```ini
# /etc/systemd/system/tango.target
[Unit]
Description=Tango development environment target
Requires=tango-db.service
Requires=tango-starter.service
Requires=tango-accesscontrol.service
Requires=tango-accesscontrol.timer
Requires=tango-starter.timer

[Install]
WantedBy=multi-user.target
```
:::

Start this target with the `start` command:

```console
sudo systemctl start tango.target
```

## Defining Tango servers as systemd units

It may be useful to create systemd units for specific Tango servers in production. Similar to the above examples create a file named **device-server1.service** under the `/etc/systemd/system/` directory. An example of the contents of this file is shown below:

:::{dropdown} tango-server1.service
```ini
# /etc/systemd/system/tango-server1.service
[Unit]
Description=My Device Server
After=tango-accesscontrol.service
Requires=tango-db.service
Requires=tango-accesscontrol.service

[Service]
Restart=always
RestartSec=10
User=<user>
Environment=TANGO_HOST=<tango_host:port>
ExecStart=<path/to/device-class> <device>

[Install]
WantedBy=tango.target
```

Replace:
- `<user>`: your username (e.g. tango)
- `<tango_host:port>`: TANGO_HOST varible as IP:PORT (e.g. localhost:10000)
- `<path/to/device-class>`: e.g. for TangoTest this might be /usr/local/tango/bin/TangoTest
- `<device>`: name of the device to start
:::
