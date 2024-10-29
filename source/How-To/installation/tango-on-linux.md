(tango-on-linux)=

# Linux

{audience}`administrators, developers`

## Debian + Ubuntu

### Non-interactive installation

1. Install packages required to compile tango-controls:

```console
sudo apt-get install g++ openjdk-8-jdk mariadb-server libmariadb-dev zlib1g-dev libomniorb4-dev libcos4-dev omniidl libzmq3-dev make
```

2. Start mariadb :

```console
sudo service mariadb start
```

3. Set password for mariabdb root user to 'mypassword' (change as appropriate):

```console
sudo mariadb -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'mypassword';
# The following 2 lines do not apply on recent mariadb versions (MariaDB-10.4+)
# Please refer to MariaDB documentation to configure correctly your users (https://mariadb.com/kb/en/alter-user/ and https://mariadb.com/kb/en/set-password/)
UPDATE mysql.user SET authentication_string = '' WHERE user = 'root';
UPDATE mysql.user SET plugin = '' WHERE user = 'root';
```

4. Download source tarball from github:

```console
wget https://gitlab.com/api/v4/projects/24125890/packages/generic/TangoSourceDistribution/9.3.5/tango-9.3.5.tar.gz
```

5. Unpack in a sub-directory called tango:

```console
mkdir tango
cd tango
tar xzvf tango-9.3.5.tar.gz
```

6. Configure tango-controls to build and install in /usr/local/tango (set the DB password as appropriate):

```console
./configure --enable-java=yes --enable-mariadb=yes --enable-dbserver=yes --enable-dbcreate=yes --with-mysql-admin=root --with-mysql-admin-passwd='mypassword' --prefix=/usr/local/tango
```

7. Compile tango-controls:

```console
make
```

8. Install tango-controls:

```console
sudo make install
```

9. Add following lines to start script /usr/local/tango/bin/tango:

```console
sudo gedit /usr/local/tango/bin/tango

# add lines near the top:

export MYSQL_USER=root
export MYSQL_PASSWORD=mypassword
```

10. Start tango-controls database server:

```console
sudo /usr/local/tango/bin/tango start
```

11. Set the TANGO_HOST variable (note: you can do this in e.g. `~/.bashrc` or wherever it is appropriate for your system):

```console
export TANGO_HOST=localhost:10000
```

12. Start test device server:

```console
/usr/local/tango/bin/TangoTest test &
```

13. Test Jive:

```console
/usr/local/tango/bin/jive &
```

You can now define your device servers and devices, start and test them!

## CentOS

RPM packages for RedHat based systems are built from the [tango-spec](https://gitlab.com/tango-controls/tango-spec) repository
using [Copr](https://copr.fedorainfracloud.org/).
Copr can be used as a repository but only the latest build is kept forever.
To install the packages directly from Copr, please refer to the [tango-spec README](https://gitlab.com/tango-controls/tango-spec/-/blob/main/README.md#installing-the-rpms).

RPM packages from Copr are also available in the [MAX-IV's repository](http://pubrepo.maxiv.lu.se/rpm/el7/x86_64/).
Use yum to install them e.g. to install the TANGO database and test device server:

```console
$> sudo yum install -y mariadb mariadb-server
   sudo yum install -y libtango9 tango-db tango-test
```

The above packages install the Tango core C++ libraries, database and TangoTest server.

### Installation

If you want to install TANGO on CentOS, here are the steps you should follow:

- add the EPEL repository:

```console
$> sudo yum install -y epel-release
```

- add the MAX-IV's public repository by creating the following file:

```console
$> sudo nano /etc/yum.repos.d/maxiv.repo
[maxiv-public]
name=MAX IV public RPM Packages - $basearch
baseurl=http://pubrepo.maxiv.lu.se/rpm/el$releasever/$basearch
gpgcheck=0
enabled=1

$> sudo yum makecache
```

- install and start MariaDB:

```console
$> sudo yum install -y mariadb-server mariadb
   sudo systemctl start mariadb
   sudo systemctl enable mariadb
```

- run  mysql_secure_installation script:

```console
$> sudo mysql_secure_installation
```

- install  TANGO library:

```console
$> sudo yum install -y libtango9 libtango9-devel
```

- install  tango-db and tango-common packages:

```console
$> sudo yum install -y tango-db tango-common
```

- create TANGO database:

```console
$> cd /usr/share/tango-db/
   sudo ./create_db.sh
```

- set up TANGO environment:

  :::{note}
  You should not use `localhost` as your TANGO_HOST.
  You can set the machine hostname using {command}`sudo hostnamectl set-hostname tangobox`
  :::

```console
$> sudo nano /etc/tangorc
```

For example:

```console
TANGO_HOST=tangobox:10000
```

- set up environment variables:

```console
$> sudo nano /etc/profile.d/tango.sh
```

For example:

```console
. /etc/tangorc
export TANGO_HOST
```

- start and enable TANGO database:

```console
$> sudo systemctl start tango-db
   sudo systemctl enable tango-db
```

- install  Starter and TangoTest:

```console
$> sudo yum install -y tango-starter tango-test
```

- start and enable Starter:

```console
$> sudo systemctl start tango-starter
   sudo systemctl enable tango-starter
```

- install Java based tools:

```console
$> sudo yum install -y tango-java
```

- install PyTango:

```console
$> sudo yum install -y python-pytango
```

## Arch

An AUR package exists [here](https://aur.archlinux.org/packages/tango/)

Download and install it from there, or use your favourite AUR helper application to do the work for you.

## Video

The following video (by Mohamed Cherif Areour, in French with English subtitles) shows you how to install Tango on Ubuntu and LinuxMint.

```{raw} html
<iframe width="560" height="315" src="https://www.youtube.com/embed/f903EIbiv6w?rel=0" frameborder="0" allowfullscreen></iframe>
```

## Testing

**How to test that everything was correctly installed**

You have to have *"tango-test"* been installed and check where is it located (you can use *"locate TangoTest"* command) and start it with *"test"* instance.

For example:

```console
$> /usr/lib/tango/TangoTest test
```

Console should display "Ready to accept request".

After you may go to [Jive](#jive-manual) and choose the following window (see the image below):

```{image} tango-on-linux/jive.png
```

TangoTest (it is a {term}`server <device server>`)-> test (it is an {term}`instance <device server instance>`) -> TangoTest (it is a {term}`class <device class>`) -> sys/tg-test/1 (it is a {term}`device <device>`)

Right click on the device and choose *"Test device"*.

You should get a new window with *"Attributes"* where you should see the values. That means you have done everything correct.
