# Getting started

```{toctree}
:hidden:
intro.md
01-first-steps.md
02-state-status.md
```

This tutorial shows you how to get started with **Tango**, covering the major features, step by step.

The topics will build on the previous ones, but you can jump in at any point to learn about a specific aspect.

## Installation

There are many ways to install Tango, but for this tutorial we will use **Pixi**, which provides a similar experience
across multiple platforms, is fast, and very easy to use.

Follow the instructions on the [Pixi home page](https://pixi.sh/).  We'll wait for you here...

⏳

... welcome back.  Now open a new terminal, and run the following to check if the installation worked:

```console
$ pixi
```

Create a folder to keep the tutorial code.  You could start in your home directory, and make a directory
called `projects` for all your projects.

```console
$ cd
$ mkdir projects
$ cd projects
```

Create a Pixi project, and install all the dependencies we will need.

```console
$ pixi init tango-tut
$ cd tango-tut
$ pixi add python=3.12 pytango tango-test tango-admin jtango jive pogo
```

Enter the Pixi project shell, which is a bit like activating a Python virtual environment.
This will make our newly installed version of Python and its dependencies available
at the prompt.

```console
$ pixi shell
```

Test it:

```console
(tango-tut) $ python
```

```python-console
>>> import tango
>>> print(tango.utils.info())
PyTango 10.0.0 (10, 0, 0)
PyTango compiled with:
    Python : 3.12.7
    Numpy  : 2.0.2
    Tango  : 10.0.0
    Boost  : 1.86.0

PyTango runtime is:
    Python : 3.12.5
    Numpy  : 2.1.2
    Tango  : 10.0.0

PyTango running on:
uname_result(system='Darwin', node='my.machine', release='24.0.0', version='Darwin Kernel Version 24.0.0: Tue Sep 24 23:39:07 PDT 2024; root:xnu-11215.1.12~1/RELEASE_ARM64_T6000', machine='arm64')
```

We can exit the Pixi shell with the `exit` command:
```console
(tango-tut) $ exit
$
```
