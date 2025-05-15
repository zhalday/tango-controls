(conda-packages)=

# Conda Packages

```{tags} audience:administrators, audience:developers, audience:all
```

Most Tango packages are available on [conda-forge](https://conda-forge.org) for Linux, macOS and Windows.

Conda packages can be used in production or for development on your machine.

::::{note}
:class: dropdown

Running the Tango `Databaseds` requires a `mariadb` database.
The preferred method to install `mariadb` is to use your OS package manager. This will come with `systemd` integration on Linux. For local development, `docker` can be used.
It is not recommended to use conda for `mariadb` itself (there is currently no `mariadb-server` on `conda-forge` but there is a `mysql-server`).

You can then run `Databaseds` by installing the `tango-database` conda package.

:::{tip}
For local development, you can run `PyDatabaseds` instead by installing `pytango-db`, a pure Python implementation of the Tango Database
relying on sqlite. No `mariadb` needed. This isn't recommended for production at this point!
:::
::::

::::{grid} 3
:::{grid-item-card} C++ packages
* [tango-idl](https://anaconda.org/conda-forge/tango-idl)
* [cpptango](https://anaconda.org/conda-forge/cpptango)
* [tango-database](https://anaconda.org/conda-forge/tango-database)
* [tango-admin](https://anaconda.org/conda-forge/tango-admin)[^1]
* [tango-access-control](https://anaconda.org/conda-forge/tango-access-control)
* [tango-starter](https://anaconda.org/conda-forge/tango-starter)
* [tango-test](https://anaconda.org/conda-forge/tango-test)
* [universaltest](https://anaconda.org/conda-forge/universaltest)
* [libhdbpp](https://anaconda.org/conda-forge/libhdbpp)
* [libhdbpp-timescale](https://anaconda.org/conda-forge/libhdbpp-timescale)
* [hdbpp-cm](https://anaconda.org/conda-forge/hdbpp-cm)
* [hdbpp-es](https://anaconda.org/conda-forge/hdbpp-es)
:::
:::{grid-item-card} Java packages
* [jtango](https://anaconda.org/conda-forge/jtango)
* [tango-atk](https://anaconda.org/conda-forge/tango-atk)
* [tango-atk-panel](https://anaconda.org/conda-forge/tango-atk-panel)
* [tango-atk-tuning](https://anaconda.org/conda-forge/tango-atk-tuning)
* [jive](https://anaconda.org/conda-forge/jive)
* [tango-astor](https://anaconda.org/conda-forge/tango-astor)[^2]
* [pogo](https://anaconda.org/conda-forge/pogo)
:::
:::{grid-item-card} Python packages
* [pytango](https://anaconda.org/conda-forge/pytango)
* [pytango-db](https://anaconda.org/conda-forge/pytango-db)
* [itango](https://anaconda.org/conda-forge/itango)
* [dsconfig](https://anaconda.org/conda-forge/dsconfig)
* [taurus](https://anaconda.org/conda-forge/taurus)
* [sardana](https://anaconda.org/conda-forge/sardana)
* [svgsynoptic2](https://anaconda.org/conda-forge/svgsynoptic2)
* [tango-gateway](https://anaconda.org/conda-forge/tango-gateway)
:::
::::

:::{tip}
The above list is not exhaustive, especially for Python packages. You can always search on [anaconda](https://anaconda.org/conda-forge) or [prefix.dev](https://prefix.dev) to check if a package is available.
:::

[conda] is the original package manager to work with conda packages, but there are alternatives:

* [mamba]: a Python-based CLI conceived as a drop-in replacement for `conda`, offering higher speed.
* [micromamba]: a pure C++-based CLI, self-contained in a single-file executable.
* [pixi]: a Rust-based package manager and workflow tool built on the foundation of the conda ecosystem.
  It is also the easiest way to install global tools.

## conda/mamba/micromamba

In the following, we'll show commands using `conda`.
You should be able to replace `conda` with `mamba` or `micromamba` based on your preference.

`micromamba` supports a subset of all `mamba` or `conda` commands, but the most frequent ones are identical.

:::{warning}
[Anaconda distribution](https://docs.anaconda.com/anaconda/) and [Miniconda](https://docs.anaconda.com/miniconda/) are linked to [Anaconda Terms of Service](https://www.anaconda.com/terms-of-service).
They come with Anaconda's [defaults channels](https://docs.anaconda.com/working-with-conda/reference/default-repositories/), which have a pay-for-user policy.

Please review the [terms of service](https://www.anaconda.com/terms-of-service)
and only use [Anaconda Repository](https://repo.anaconda.com/) if you understand the consequences.
:::

To install [conda] and [mamba], you should use the [Miniforge3](https://github.com/conda-forge/miniforge) installer as it comes with both and `conda-forge` as the configured channel.

To install [micromamba], check the [official documentation](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html#automatic-install).

If you have `conda` already installed, you should run `conda info` to check the configured channels.

```console
$ conda info
...
channel URLs : https://conda.anaconda.org/conda-forge/...
               https://conda.anaconda.org/conda-forge/noarch
...
```

Ensure you have `conda-forge` channel configured. It is the **only channel** you need to install all above packages.
If `https://repo.anaconda.com/pkgs/...` is in your list of channels, you should remove it by editing your `.condarc` file.
Refer to the [official documentation](https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/use-condarc.html).

:::{warning}
When using `conda` or `mamba`, you should not install packages in the `base` environment.
It is reserved for their dependencies.
**Always create a separate environment**.

`micromamba` is a single executable and doesn't come with a `base` environment.
:::

To install `tango-test` and `pytango`, you can run:

```console
$ conda create -y -n tango tango-test python=3.12 pytango
$ conda activate tango
(tango) $ TangoTest --help
(tango) $ python -c 'import tango; print(tango.utils.info())'
```

You can also run an executable in a conda environment without activating it:

```console
$ conda run -n tango TangoTest --help
```

## pixi

`Pixi` is a package management tool for developers. It allows you to install libraries and applications in a reproducible way. It is also very convenient to install global tools.

Install `pixi` following the instructions on [pixi website](https://pixi.sh).

### Installing global tools with pixi

To install tools that aren't linked to any project, you can use the `pixi global` command.
Install `jive`, `pogo`, `tango-database` on your machine:

```console
$ pixi global install jive pogo tango-database
```

This will create a separate environment for each of the application and make them available in your `PATH`.
You can now invoke any of them (no activation needed):

```console
$ jive
```

See <https://pixi.sh/latest/reference/cli/#global-options> for more information.

### Working on projects

```{tags} audience:developers
```

When working on a project, `pixi` can manage environments for you.

If you clone a project with an existing `pixi.toml` file, like [pytango repository](https://gitlab.com/tango-controls/pytango), running `pixi run` will automatically create the defined environment.

If you work on a new project, create a `pixi.toml` file by running `pixi init`:

```console
$ cd myproject
$ pixi init
```

You can then add all the requirements you need:

```console
$ pixi add python=3.12 pytango
```

This will automatically update the `pixi.toml` file as well as a `pixi.lock` file
and create the environment under the `.pixi` directory.
You can use that environment by running `pixi run` or `pixi shell` to activate it.

```console
$ pixi run python -c 'import tango; print(tango.utils.info())'
```

```console
$ pixi shell
(myproject) $ python -c 'import tango; print(tango.utils.info())'
```

When using `pixi shell`, just enter `exit` to exit the shell.

[^1]: `tango-admin` is not available on Windows
[^2]: `astor` on conda-forge is taken by a Python package

[conda]: https://docs.conda.io/projects/conda/en/stable/
[mamba]: https://mamba.readthedocs.io/
[micromamba]: https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html
[pixi]: https://pixi.sh
