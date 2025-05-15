(linux-redhat-installation)=
# Red Hat based

```{tags} audience:administrators, audience:developers
```

:::{warning}
Do NOT use **CentOS** anymore.
CentOS 7 has been end-of-life since 2024-06-30.
This was the last supported version of CentOS.

Migrate to another distribution: [RHEL](https://www.redhat.com/rhel/linux), [CentOS Stream](https://www.centos.org/centos-stream/), [AlmaLinux](https://almalinux.org), [Rocky Linux](https://rockylinux.org)...
:::

RPM packages for Red Hat based systems are built from the [tango-spec](https://gitlab.com/tango-controls/tango-spec)
repository using [Copr](https://copr.fedorainfracloud.org/).
Copr can be used as a repository but only the latest build is kept forever.
To install the packages directly from Copr, please refer to the [tango-spec README](https://gitlab.com/tango-controls/tango-spec/-/blob/main/README.md#installing-the-rpms).

RPM packages from Copr are also available in the [MAX-IV's repository](http://pubrepo.maxiv.lu.se/rpm/).

:::{dropdown} Available RPM packages

:tango-idl: Tango CORBA IDL file
:libtango9: Tango C++ library
:libtango9-devel: Tango C++ library development files
:tango-common: shared infrastructure for Tango packages
:tango-db: the Tango database device server, with systemd integration
:tango-admin: provides tango_admin, a cli to the Tango database
:tango-test: the TangoTest device server
:tango-starter: the Tango Starter device server, with systemd integration
:tango-java: java based Tango applications (jive, astor...)
:tango-accesscontrol: the TangoAccessControl device server
:::


## Installation

To install Tango on Red Hat, here are the steps you should follow:

1. Add the EPEL repository:

   ```console
   sudo dnf install -y epel-release
   ```

1. Add the MAX-IV's public repository by creating the following file:

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
   sudo dnf makecache
   ```

1. Install and start MariaDB:

   ```console
   sudo dnf install -y mariadb-server mariadb
   sudo systemctl start mariadb
   sudo systemctl enable mariadb
   ```

1. Run  mysql_secure_installation script:

   ```console
   sudo mysql_secure_installation
   ```

1. Install the tango Databaseds

   ```console
   sudo dnf install -y tango-db
   ```

1. Create TANGO database:

   ```console
   cd /usr/share/tango-db/
   sudo ./create_db.sh
   ```

1. Set up TANGO environment:

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

1. Set up environment variables:

   ```console
   sudo nano /etc/profile.d/tango.sh
   ```

   For example:

   ```console
   . /etc/tangorc
   export TANGO_HOST
   ```

1. Start and enable TANGO database:

   ```console
   sudo systemctl start tango-db
   sudo systemctl enable tango-db
   ```

1. Install Starter and TangoTest:

   ```console
   sudo dnf install -y tango-starter tango-test
   ```

1. Start and enable Starter:

   ```console
   sudo systemctl start tango-starter
   sudo systemctl enable tango-starter
   ```

1. Install Java based tools:

   ::::{tab-set}

   :::{tab-item} RHEL 8
   ```console
   # Enabling powertools and javapackages-tools is required to install log4j12
   sudo dnf config-manager --set-enabled powertools
   sudo dnf module -y enable javapackages-tools
   sudo dnf install -y tango-java
   ```
   :::

   :::{tab-item} RHEL 9
   ```console
   sudo dnf install -y tango-java
   ```
   :::

   ::::

:::{note}
`pytango` isn't packaged anymore as RPM. Last version packaged was 9.4.2.
Use pip in a virtualenv or conda to install a recent version.
:::
