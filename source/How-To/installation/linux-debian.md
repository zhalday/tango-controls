(linux-debian-installation)=

# Debian

```{tags} audience:administrators, audience:developers
```

## Binary packages

If you don't have special requirements for a specific tango version, the easiest way is to use the standard debian
packages.

1. Installing the packages

```console
sudo apt install libtango-dev tango-db tango-test
```

You can use the default answers when asked questions during installation.

2. Starting the TangoTest device server

```console
/usr/lib/tango/TangoTest test
```

This should print `Ready to accept request`.

Now you can ping the TangoTest device server in another console

```console
tango_admin --ping-device sys/tg_test/1; echo $?
```

which should return `0`.

The drawback of the stock debian packages is that they don't include any java applications like jive or astor.

If you need these, or a newer tango version, you can consider compiling the tango-controls package (called
TangoSourceDistribution) in the next section.

(debian-compile-tango-source-distribution)=
## Compilation of the TangoSourceDistribution

The following steps have been written for Debian bookworm. Ubuntu should be similiar.

1. Install packages required to compile tango-controls:

```console
sudo apt-get install g++ openjdk-17-jre-headless mariadb-server libmariadb-dev zlib1g-dev libzmq3-dev cmake
```

For omniORB you need to use the packages from bookworm/backports.

Add them to APT using

```console
sudo nano /etc/apt/sources.list.d/omniorb-bookworm-backports.list
```

and adding

```console
deb http://deb.debian.org/debian bookworm-backports main
```

and update the package sources

```console
sudo apt update
```

and install omniORB 4.3.x

```console
sudo apt install libomniorb4-dev/bookworm-backports libcos4-dev/bookworm-backports omniidl/bookworm-backports
```

2. Start mariadb :

```console
sudo service mariadb start
```

3. Set password for mariabdb root user to 'mypassword' (change as appropriate):

```console
sudo mysql -u root -e "SET PASSWORD = PASSWORD('mypassword');"
```

4. Download the sources

The latest version can be downloaded from [here](https://gitlab.com/tango-controls/TangoSourceDistribution/-/releases),
you want the `Tango Source Distribution` file.

5. Unpack in a sub-directory called tango:

```console
mkdir tango
cd tango
tar xzvf tango-*.tar.gz
```

6. Configure tango-controls to build and install in /usr/local (replacing `mypassword` with the password you set
   earlier):

```console
cmake -B build -S . -DMYSQL_ADMIN=root -DMYSQL_ADMIN_PASSWD=mypassword -DTDB_DATABASE_SCHEMA=ON
```

7. Compile

```console
cmake --build build --parallel $(nproc)
```

8. Install

```console
sudo cmake --build build --target install
```

9. Add the following lines to the start script /usr/local/bin/tango:

```console
sudo nano /usr/local/bin/tango
```

```bash
# add lines near the top:

export MYSQL_USER=root
export MYSQL_PASSWORD=mypassword
```

10. Start tango-controls database server:

```console
sudo /usr/local/tango/bin/tango start
```

11. Set the TANGO_HOST variable in `/etc/tangorc` via

```console
sudo nano /etc/tangorc
```

and adding

```
TANGO_HOST=127.0.0.1:10000
```

12. Start the TangoTest device server:

```console
/usr/local/tango/bin/TangoTest test &
```

13. Test Jive:

```console
/usr/local/tango/bin/jive &
```

You can now define your device servers and devices, start and test them!
