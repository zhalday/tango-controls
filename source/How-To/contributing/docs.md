(documentation-workflow-tutorial)=

# Tango Documentation

{audience}`developers`

Please follow these guidelines when writing or improving the Tango Controls documentation in order to keep it as consistent as possible. It is also important to know how the contents is structured. You will find necessary information below.

```{contents} Table of Contents
:depth: 3
```

## About this documentation

The documentation is built using the documentation generator [Sphinx](https://www.sphinx-doc.org/en/master/) based on [Docutils](https://docutils.sourceforge.io/). The source content is written in [MyST Markdown](https://myst-parser.readthedocs.io/en/latest/).

The documentation source files are stored on GitLab: <https://gitlab.com/tango-controls/tango-doc> .

It is publicised in HTML on the readthedoc.io: <http://tango-controls.readthedocs.io/>


### Source structure

#### Versions

The *readthedocs.io* allows for various versions of published documentation. These are achieved by specifying branches in the GitLab repository. The branches for the official Tango Controls versions are named numerically with the format: #.#.#.

#### Chapters and headers

Chapters' order is defined by the master table of contents, contained in the file {file}`source/index.md`. This file
references further {file}`index.md` files contained in the subdirectories.


#### Glossary

Centralised definitions of the main concepts of Tango Controls are contained in the {file}`source/Reference/glossary.md` file. Entries defined there may be referenced from anywhere in the documentation using the format `` {term}`xxx` ``, e.g. `` {term}`device`  `` produces the following link to the `device` definition in the Glossary {term}`device`

#### Images

Images should be stored in a subdirectory of the directory where the source documentation is stored. As an example please refer to {file}`source/tools/pogo`. When a folder contains more than one Markdown file then the directory containing images referenced by that file should be named the same as the Markdown file, for example see {file}`source/How-To/installation/tango-on-windows`.

### Configuration

#### source/conf.py

This is a standard build configuration file used by Sphinx. The project name, version, and copyright info are defined here. Please refer to
[conf.py documentation](http://www.sphinx-doc.org/en/stable/config.html#module-conf) for further details.

#### requirements.txt

This is a standard {program}`pip` requirements file used to specify Python packages version.


#### readthedocs.yml

This is the configuration file for the `readthedocs` application. The output format for Tango Controls is standard HTML.


## Updating the documentation

If you find that some useful information is missing, misleading or improvements could be made please either:

- send a request through the GitLab project by creating a issue: <https://gitlab.com/tango-controls/tango-doc/issues>
- or make the correction yourself and contribute this back to the project.

If you decide to contribute, the preferred way is to:

- fork the repository,
- create your own local branch containing the fixes,
- create a merge request from your forked branch to the tango-doc `origin/main` branch.

:::{note}
```{rubric} GitLab online edit
```

For small fixes, you may use GitLab online editing feature.
It is a good practice to avoid direct commits to the 'main' branch.
Please select {guilabel}`Create a new branch and start pull request` before sending
the change.
:::


### Building/previewing documentation locally

#### Prerequisites

To work with documentation, first you need to have the following programs installed on your system:

- {program}`Python >=3.10` (as Sphinx is a Python tool),
- {program}`Git` (since the sources are kept in a git repository).


#### Building

To build the documentation you will need a Python virtual environment with Sphinx and other pip installable packages. To create this virtual environment and install the required packages:

```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Build the html with:
```
make html
```

This will build the HTML output in the {file}`build` directory.You can then use any web browser to view the documentation, e.g.:
```
firefox build/html/index.html
```

:::{note}
```{rubric} Don't see your changes?
```

Sometimes you will need to do a fresh build to see some changes. You can do this by first cleaning the build directory with:
```
make clean
```
Followed by:
```
make html
```
:::


### Contributing changes

1. Fork the tango-doc repository:

   From the <https://gitlab.com/tango-controls/tango-doc> click {guilabel}`Fork` in the top right corner.

2. Clone your forked repository to work on it locally:

   ```
   git clone git@gitlab.com:<user>/tango-doc.git
   ```
   The `origin` remote will point to your forked repository.

3. Create your local working branch:

   :::{note}
   The following command creates a branch based on `origin/main`.
   If you would like to contribute to another branch, e.g. directly to `9.2.5`, you need to use:

   ```
   git checkout -b update-docs-example origin/9.2.5
   ```

   To see what what branch is the current one use: {command}`git branch -a`. The current branch is marked
   with an asterisk (\*).
   :::

   ```
   git checkout -b update-docs-example origin/main
   ```

4. Edit the appropriate file (or create it if it doesn't exist).

5. Make sure that the file appears in the relevant toc-tree (in the {file}`index.md` file or in the master {file}`source/index.md`).

6. Check if your changes have built correctly:

   ```
   make clean html
   ```

5. Check results with a browser (open the `build/html/<filename>.html`)

If everything is OK, follow the next steps to commit your changes and create a merge request, which will be reviewed and eventually merged online.

#### Committing changes

1. Add modifications to a commit list. For example:

   ```
   git add source/How-To/contributing/docs.md
   git add source/How-To/contributing/contributing.md
   ```

2. Commit the changes providing some meaningful message. For example:

   ```
   git commit -m "Updating docs"
   ```

   :::{note}
   The changes are now committed to your local repository. You may continue editing, checking, and committing steps until you are happy with your work in order to track the history of changes. When finished you will need to share them by pushing your changes to the online repository.
   :::

3. If you continue to work locally on your branch for a long time it is good to perform a rebase to update your branch with any recent changes added by someone else. Firstly update your fork using the {guilabel}`Update fork` button on your forked repository. Then perform the rebase, for example:

   ```
   git fetch origin
   git rebase origin/main
   ```

   :::{note}
   If you are contributing to other branch than `main`, for example directly to the `9.5.2`, you need to call

   ```
   git rebase 9.5.2
   ```
   :::

#### Pushing (to the GitLab repository)

1. Push your changes to your forked repository. For example:

   ```
   git push -u origin update-docs-example
   ```

Now you are ready to ask for your changes to be merged by creating a merge request on GitLab.

#### Pull request (asking for merge)

1. Go to your branch on your forked repository.
2. Click {guilabel}`Create merge request`.
3. Check the `From` and `into` locations. `From` should be the branch on your forked repository and `into` should be into the upstream repository `tango-doc:main` branch.
4. Provide a relevant comment and check that the `Commits` and `Changes` are as expected.
5. Click {guilabel}`Create merge request`.

Now, someone will review your contribution, merge into selected branch and publish. If they finds any issues, they will get back to you and request further changes.


## Including Read the Docs Subprojects

Existing documentation from other projects can be included as a [Read the Docs subproject](<https://docs.readthedocs.io/en/stable/subprojects.html>) of the parent tango-controls project. The subproject will appear under the tango-controls domain, e.g. the Jive project documentation is available from <https://tango-controls.readthedocs.io/projects/jive>. Links to subproject content can easily be included in the parent tango-controls project and vice versa. This prevents content from being repeated in multiple locations.

### Setting up a subproject

The initial setup on Read the Docs needs to performed by someone who is a Read the Docs maintainer of both the parent tango-controls project and the subproject that you wish to include.

1. Add the project as a subproject of tango-controls on Read the Docs:

   From the Read the Docs project: {guilabel}`Project` > {guilabel}`Admin` > {guilabel}`Subproject` > {guilabel}`Add subproject`.

2. Configure the subproject mapping in the parent tango-controls project.

   In the {file}`src/conf.py` add to the `intersphinx_mapping` definition:
   ```
   intersphinx_mapping = {
    'subproj_name': ('https://<subproject_name>.readthedocs.io/en/latest/', None)
	}
   ```

3. Configure the mapping in the subproject to be able to link to the parent tango-controls project

   In the subproject {file}`src/conf.py` ensure the `intersphinx` extension is specified:
   ```
   extensions = [
		...
    'sphinx.ext.intersphinx',
	]
   ```

   In the subproject {file}`src/conf.py` add to the `intersphinx_mapping` definition:
   ```
   intersphinx_mapping = {
    'tango-controls': ('https://tango-controls.readthedocs.io/en/latest/', None)
	}
   ```

4. In the parent tango-controls you can then reference sections in the subproject using the following link format:

   ```
   [Explicit text](inv:subproj_name:std#index)
   ```

5. Similarly in the subproject you can reference sections in the parent tango-controls project using the following link format:

   ```
   [Explicit text](inv:tango-controls:std#index)
   ```

:::{tip}
You can list the references available in a project by using the `myst-inv` command (it comes with `myst-parser` and is available in the virtualenv you created).

```console
myst-inv https://<subproject_name>.readthedocs.io/en/latest/
```

You can filter by name with `-n` option. Check the help.
:::
