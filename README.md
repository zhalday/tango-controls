[![logo](http://www.tango-controls.org/static/tango/img/logo_tangocontrols.png)](http://www.tango-controls.org)

# Tango Controls Documentation

[![Documentation Status](https://readthedocs.org/projects/tango-controls/badge/?version=latest)](https://tango-controls.readthedocs.io/en/latest/?badge=latest)
[![Build Status)](https://img.shields.io/gitlab/pipeline-status/tango-controls/tango-doc?branch=main)](https://gitlab.com/tango-controls/tango-doc/-/pipelines?page=1&scope=branches&ref=main)

This repository contains the official documentation of the Tango Controls project.

It uses [Sphinx](https://www.sphinx-doc.org/en/stable/) and [myst-parser](https://myst-parser.readthedocs.io)
to generate HTML from markdown files.

It is publicised in HTML format [here](https://tango-controls.readthedocs.io/).

## Working locally

To build the html documentation, you need Python >= 3.10.

### pixi

This is an easy way to build the html documentation locally as `pixi` will install the proper python version and requirements automatically.
`Pixi` is just one executable that you can install from <https://pixi.sh>.

Build the documentation by running: `pixi run doc`.

### python venv

If you prefer to create a python virtualenv, use (the requirements were generated with Python 3.12):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Build the documentation:

```bash
make html
# or
python -m sphinx -b html -n -W source build/html
```

Open `build/html/index.html` in your browser.

## Updating requirements

The `requirements.txt` file is generated based on the pixi environment.

If the requirements required to build the documentation need to be updated, you should update the `pixi.toml` and `pixi.lock` files:

* Update the dependencies using `pixi add` / `pixi update` or removing the `pixi.lock` file and regenerating it by running `pixi list`.
* Update the `requirements.txt` by running `pixi run update-requirements`.
