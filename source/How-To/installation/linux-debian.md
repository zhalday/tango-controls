(linux-debian-installation)=

# Debian

```{tags} audience:administrators, audience:developers
```

:::{note}
Below are instructions on how to install Tango 10. For instructions on how to install older versions of Tango please
see previous versions of the [Tango documentation](https://readthedocs.org/projects/tango-controls/versions/).
:::

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

The following steps have been written for Debian bookworm and Ubuntu 24.04.

1. Install packages required to compile tango-controls:

   :::::{tab-set}
   ::::{tab-item} Debian
   ```console
   sudo apt-get install g++ openjdk-17-jdk mariadb-server libmariadb-dev \
   zlib1g-dev libzmq3-dev cmake git protobuf-compiler-grpc libprotobuf-dev \
   libcurl4-openssl-dev libjpeg-dev libgrpc++-dev libabsl-dev
   ```

   For omniORB you need to use the packages from bookworm/backports.

   - Add them to APT by opening the file:

      ```console
      sudo nano /etc/apt/sources.list.d/omniorb-bookworm-backports.list
      ```

      and adding the line:

      ```console
      deb http://deb.debian.org/debian bookworm-backports main
      ```

   - Update the package sources

      ```console
      sudo apt update
      ```

   - Install omniORB 4.3.x

      ```console
      sudo apt install libomniorb4-dev/bookworm-backports libcos4-dev/bookworm-backports \
      omniidl/bookworm-backports
      ```
   ::::
   ::::{tab-item} Ubuntu
   ```console
   sudo apt-get install g++ openjdk-17-jdk mariadb-server libmariadb-dev \
   zlib1g-dev libzmq3-dev cmake git libomniorb4-dev libcos4-dev omniidl \
   protobuf-compiler-grpc libprotobuf-dev libcurl4-openssl-dev libjpeg-dev \
   libgrpc++-dev
   ```
   ::::
   :::::


2. Start mariadb:

    ```console
    sudo service mariadb start
    ```

3. Set the password for the mariabdb root user. Replace `<mypassword>` with an appropriate password in the command below:

    ```console
    sudo mysql -u root -e "SET PASSWORD = PASSWORD('<mypassword>');"
    ```

4. Download OpenTelemetry dependency:

   :::{note}
   Tango is built with OpenTelemetry by default. If you wish to install Tango without OpenTelemetry then please
   go straight to step 6.
   :::

   Check for the latest released version at <https://github.com/open-telemetry/opentelemetry-cpp/releases>.
    ```console
    mkdir opentelemetry
    cd opentelemetry

    wget https://github.com/open-telemetry/opentelemetry-cpp/archive/refs/tags/vX.X.X.tar.gz
    tar xzvf v*.tar.gz
    cd opentelemetry-cpp-*
    ```

5. Build OpenTelemetry

    - Create build directory
        ```console
        mkdir build
        cd build
        ```

    - Configure build
        ```console
        cmake .. -DWITH_OTLP_GRPC=ON -DWITH_OTLP_HTTP=ON -DBUILD_SHARED_LIBS=ON \
        -DCMAKE_POSITION_INDEPENDENT_CODE=ON -DWITH_ABSEIL=ON -DWITH_BENCHMARK=OFF \
        -DWITH_EXAMPLES=OFF -DWITH_FUNC_TESTS=OFF -DWITH_DEPRECATED_SDK_FACTORY=OFF \
        -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=RelWithDebInfo
        ```

    - Compile
        ```console
        cmake --build . --target all
        ```

    - Install:
        ```console
        sudo cmake --install .
        ```


6. Download the Tango source code:

    - Create a new directory under ~/:
        ```console
        mkdir ~/tango
        cd ~/tango
        ```

    - The latest version can be downloaded from [here](https://gitlab.com/tango-controls/TangoSourceDistribution/-/releases),
    you want the `Tango Source Distribution` file. You can use `wget` to get the version you require:

        ```console
        wget https://gitlab.com/api/v4/projects/24125890/packages/generic/TangoSourceDistribution/X.X.X/tango-X.X.X.tar.gz
        ```

    - Unpack:
        ```console
        tar xzvf tango-*.tar.gz
        cd tango-X.X.X
        ```

7. Configure tango-controls to build and install in /usr/local (replacing `<mypassword>` with the password you set
   in step 3):

    ```console
    cmake -B build -S . -DMYSQL_ADMIN=root -DMYSQL_ADMIN_PASSWD=<mypassword> \
    -DTDB_DATABASE_SCHEMA=ON
    ```

   :::{note}
   To build without OpenTelemetry, add the argument `-DTANGO_USE_TELEMETRY=OFF` to the above command.
   :::

   Further CMake compilations flags are described in [](debian-compile-cmake-options).

8. Compile

    ```console
    cmake --build build --parallel $(nproc)
    ```
    where `$(nproc)` is the number of processes to use, for example `2`.

9. Install:

    ```console
    sudo cmake --build build --target install
    ```

10. Add the following lines to the start script /usr/local/bin/tango, replacing `<mypassword>` with the
password you set in step 3:

    ```console
    sudo nano /usr/local/bin/tango
    ```

    ```bash
    # add lines near the top:

    export MYSQL_USER=root
    export MYSQL_PASSWORD=<mypassword>
    ```

11. Start tango-controls database server:

    ```console
    sudo /usr/local/bin/tango start
    ```


12. Set the TANGO_HOST variable in `/etc/tangorc`:

    ```console
    sudo nano /etc/tangorc
    ```

    and add

    ```
    TANGO_HOST=127.0.0.1:10000
    ```

13. Start the TangoTest device server:

    ```console
    /usr/local/bin/TangoTest test &
    ```

    :::{note}
    If you receive an error at this stage similar to
    ```console
    error while loading shared libraries: libtango.so.10.0: cannot open
    shared object file: No such file or directory
    ```
    you will need to run the following command to get /usr/local/lib into the default runtime search path:
    ```
    sudo ldconfig
    ```

14. Test Jive:

    ```console
    /usr/local/bin/jive &
    ```

You can now define your device servers and devices, start and test them!

(debian-compile-cmake-options)=
### CMake options

Below are a list of CMake options that can be added accordingly to the command
in step 8 to configure the tango-controls build.

:::{list-table}
:widths: 10 20 10 10
:header-rows: 1

*   - Option
    - Description
    - Allowed values
    - Default
*   - TSD_LIB
    - Install and use bundled libtango, if OFF use libtango found on system
    - ON/OFF
    - ON
*   - TSD_CPP
    - Installation of cppTango and C++ applications
    - ON/OFF
    - ON
*   - TSD_JAVA
    - Installation of java applications
    - ON/OFF
    - ON
*   - TSD_DATABASE
    - Installation of tango database server
    - ON/OFF
    - ON
*   - TSD_TAC
    - Installation of access control server
    - ON/OFF
    - OFF
*   - TSD_HTML_DOCUMENTATION
    - Include the HTML documentation
    - ON/OFF
    - ON
*   - TANGO_USE_TELEMETRY
    - Build with OpenTelemetry
    - ON/OFF
    - ON
:::
