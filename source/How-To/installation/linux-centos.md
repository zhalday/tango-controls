(linux-centos-installation)=
# CentOS

{audience}`administrators, developers`

RPM packages for RedHat based systems are built from the [tango-spec](https://gitlab.com/tango-controls/tango-spec)
repository using [Copr](https://copr.fedorainfracloud.org/).
Copr can be used as a repository but only the latest build is kept forever.
To install the packages directly from Copr, please refer to the [tango-spec README](https://gitlab.com/tango-controls/tango-spec/-/blob/main/README.md#installing-the-rpms).

RPM packages from Copr are also available in the [MAX-IV's repository](http://pubrepo.maxiv.lu.se/rpm/el7/x86_64/).
Use yum to install them e.g. to install the TANGO database and test device server:

```console
sudo yum install -y mariadb mariadb-server
sudo yum install -y libtango9 tango-db tango-test
```

The above packages install the Tango core C++ libraries, database and TangoTest server.

## Installation

If you want to install TANGO on CentOS, here are the steps you should follow:

- add the EPEL repository:

```console
sudo yum install -y epel-release
```

- add the MAX-IV's public repository by creating the following file:

```console
sudo nano /etc/yum.repos.d/maxiv.repo
```

```console
[maxiv-public]
name=MAX IV public RPM Packages - $basearch
baseurl=http://pubrepo.maxiv.lu.se/rpm/el$releasever/$basearch
gpgcheck=0
enabled=1
```

```console
sudo yum makecache
```

- install and start MariaDB:

```console
sudo yum install -y mariadb-server mariadb
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

- run  mysql_secure_installation script:

```console
sudo mysql_secure_installation
```

- install  TANGO library:

```console
sudo yum install -y libtango9 libtango9-devel
```

- install  tango-db and tango-common packages:

```console
sudo yum install -y tango-db tango-common
```

- create TANGO database:

```console
cd /usr/share/tango-db/
sudo ./create_db.sh
```

- set up TANGO environment:

  :::{note}
  You should not use `localhost` as your TANGO_HOST.
  You can set the machine hostname using {command}`sudo hostnamectl set-hostname tangobox`
  :::

```console
sudo nano /etc/tangorc
```

For example:

```console
TANGO_HOST=tangobox:10000
```

- set up environment variables:

```console
sudo nano /etc/profile.d/tango.sh
```

For example:

```console
. /etc/tangorc
export TANGO_HOST
```

- start and enable TANGO database:

```console
sudo systemctl start tango-db
sudo systemctl enable tango-db
```

- install  Starter and TangoTest:

```console
sudo yum install -y tango-starter tango-test
```

- start and enable Starter:

```console
sudo systemctl start tango-starter
sudo systemctl enable tango-starter
```

- install Java based tools:

```console
sudo yum install -y tango-java
```

- install PyTango:

```console
sudo yum install -y python-pytango
```
