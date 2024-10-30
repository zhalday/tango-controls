(macos-installation)=
# macOS

{audience}`administrators, developers`
{lang}`all`

There are no macOS app installer packages available for Tango Controls. Any installation of Tango Controls libraries or tools is done on the command line.

## Conda: Everything you'll usually need

The easiest way to get all the necessary Tango Controls libraries and tools for development or administration installed on macOS is to use Conda. In our {doc}`Conda <conda>` document we explain step by step how to to get the packages installed on macOS.

## But I need only PyTango

There are developers though that might only need PyTango and nothing else. In that case the simpler way to install just PyTango is to use [pip](https://pip.pypa.io/en/stable/).

### Installation

1. Begin by creating a virtual environment:

```console
python3 -m venv --upgrade-deps .venv
```

- Next activate the virtual environment:

```console

source .venv/bin/activate
```

- Then install PyTango from PyPi:

```console
python3 -m pip --require-virtualenv pytango
```

- Finally set up TANGO environment:

:::{note}
You should not use `localhost` as your TANGO_HOST. You should use either `127.0.0.1` or your computers host name.
:::

For example:

```console
export TANGO_HOST=mymaclaptop:10000
```

### Test your PyTango installation

To see if the PyTango installation was successful, you can run a simple command:

```console
# Do not forget to activate your virtual environment
source .venv/bin/activate

python3 -c 'import tango; print(tango.utils.info())'
```

The output should look similar to this:

```console
PyTango 10.0.1.dev0 (10, 0, 1, 'dev', 0)
PyTango compiled with:
    Python : 3.12.7
    Numpy  : 2.1.2
    Tango  : 10.1.0
    Boost  : 1.86.0

PyTango runtime is:
    Python : 3.12.7
    Numpy  : 2.1.1
    Tango  : 10.1.0

PyTango running on:
uname_result(system='Darwin', node='XX:XX:XX:XX:XX:XX', release='24.0.0', version='Darwin Kernel Version 24.0.0: Tue Sep 24 23:39:07 PDT 2024; root:xnu-11215.1.12~1/RELEASE_ARM64_T6000', machine='arm64')
```

If Python cannot find the `tango` import, then you likely forgot to activate your environment.

## For the really adventurous among you

If you fell lucky and would really like to build everything from the source codes, then you might be interested in [Thomas Juerges' Tango Controls build scripts](https://gitlab.com/tjuerges/build_tango). They are relatively easy to use, can be configured quite a lot and usually get you to a working Tango Controls system with cppTango, PyTango and a handful of tools within two or three minutes depending on the speed of your mac. Please head over to the Gitlab repository where the project's README will guide you through the installation steps. Please note that you will need [Homebrew](https://brew.sh) installed.
