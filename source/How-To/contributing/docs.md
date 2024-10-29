(documentation-workflow-tutorial)=

# Tango Documentation

{audience}`developers`

When writing or improving the Tango Controls documentation it is worth to follow these guidelines.
This will help in keeping it as consistent as possible. It is also important to know how the contents
and the sources are structured to make your effort efficient. You will find necessary information below.

## About this documentation

The documentation is written with the [Sphinx] markup language. It is a documentation framework based on
[Docutils] and uses [reStructuredText] for providing content. For details please refer to [Sphinx webpage].

The documentation sources are stored on GitLab: <https://gitlab.com/tango-controls/tango-doc> .

It is publicised in HTML, PDF and EPUB formats on the readthedoc.io: <http://tango-controls.readthedocs.io/>

Some of the documents were not originally writen in Sphinx. These have been converted from other formats like
HTML, LaTeX or Word. These may contain some residual bugs and syntax errors left after conversion. They will
be consequently corrected when found.

## Updating the documentation

If you find that some useful information is missing, misleading or you can think about any potential improvements
please do either:

- send a request through the gitlab project: <https://gitlab.com/tango-controls/tango-doc/issues>
- or do correction by yourself.

If you decide to contribute by writing, the preferred way is to:

- clone or fork the repository,
- create your own local fix branch,
- when finished, send a pull request to the `origin/master` branch.

:::{note}
```{rubric} GitLab online edit
```

For small fixes, you may use GitLab online editing feature.
It is a good practice to avoid direct commits to 'dev' nor to 'master' branch.
Please select {guilabel}`Create a new branch and start pull request` before sending
the change.
:::

For details see [Documentation workflow tutorial ](#documentation-workflow-tutorial).

### Building/previewing documentation locally

To build the documentation you will need Sphinx environment which is a Python package.
Please consult [Sphinx webpage] for details on how to install it.

% There are references to doxygen C++ API documentation. You need to install
% `Breathe <https://breathe.readthedocs.io>`_, too. It is a tool for referencing doxygen documentation from the Sphinx.

:::{warning}
Some standard Python packages contain a buggy version of {program}`Breathe`. You may need to install it from
sources. You may use the following command:

{command}`pip install --upgrade git+git://github.com/michaeljones/breathe@cc8f830`
:::

After having Sphinx and Breathe installed you will be able to build the documentation:

- go to ({command}`cd`) folder where you have cloned the repository
- call {command}`sphinx-build source build`

This will build HTML output in the {file}`build` folder.Then you may use any web browser to view the documentation.

:::{note}
The build process generates a lot of warnings. Don't worry. We will work to remove as much of them as possible but some
are inevitable.
:::

For more details and step-by-step guidance pleas refer to
[Documentation workflow tutorial ](#documentation-workflow-tutorial).

## Sources structure

### Tango Controls versions

The *readthedocs.io* allows to publish various versions of the documentation. It is achieved by providing branches
in a git repository. The official version branches are these named numerically as Tango Controls versions: #.#.#.

### Chapters and headers

Chapters' order is defined by the main table of contents. It is contained in a file {file}`source/contents.rst` and
referenced index.rst files.

To keep chapters levels consistent please use the following underlining schema:

- First level underline: ==== (equal signs)
- Second level: ------ (dashes)
- Third level: ~~~ (waves)

### References

Basic list of [Reference Names](http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#reference-names)
is provided within {file}`source/conf.py` as a `rst_epilog` variable. The contents of this variable
is dynamically concatenated to the end of each *.rst* file during the building process. As of today, it provides some common
hyperlink targets. However, it is planned to include some common substitutions.
The list allows to use some entries like `` \`Tango webpage\`\_ `` which will be rendered as [Tango webpage]

### Glossary

Glossary entries (definitions) may be provided as content of any document. However, there is
a {file}`source/reference/glossary.rst` file. Its purpose is to centralise short definitions of main concepts of Tango Controls.
Entries defined there may be referenced as `` \:term\:\`...\` `` at any location in the documentation.

### Images

Fore each document, images should be stored in a sub-folder of the folder where the document is stored. As an example,
please refer to {file}`source/tools-and-extensions/astor`. When a folder contains more than one document the images folder should
be named as the document itself. See {file}`source/getting-started/installation/tango-on-windows` as an example.

## Configuration

### sources/conf.py

This is a standard `build configuration file` used by Sphinx. Among others the project name, version and copyright
info are defined there. Please refer to
[conf.py documentation](http://www.sphinx-doc.org/en/stable/config.html#module-conf).

### requirements.txt

This is a standard {program}`pip` requirements file used to fix packages version. Currently it contains Sphinx only.

### readthedocs.yml

This is a configuration file for the `readthedocs` application. It provides some fine-grain settings. For Tango Controls
it limits output formats to standard HTML, PDF and EPUB. Leaving this setting blank will lead to some problems
with the build process at readthedocs.


## Prerequisites

To work with documentation, first you need to have the following programs installed on your system:

- {program}`Python` >= 2.7 (as Sphinx is a Python tool),
- {program}`Git` (since the sources are kept in a git repository).

## Sphinx installation

Once installed the prerequisites, you can use Sphinx through two options:

- using Python3 venv way, or
- using virtualenv way.

### Using Python3 venv way

If you have prerequisites installed, you need to install Sphinx tools:

1. Install virtual environments support for Python:

   {command}`python3 -m venv doc-env`

2. Activate the environment:

   > - On GNU/Linux:

   {command}`source doc-env/bin/activate`

   > - On Windows:

   {command}`doc-env\Scripts\activate.bat`

3. Install Sphinx:

   {command}`pip install sphinx`

### Using virtualenv way

1. Install virtual environments support for Python:

   {command}`pip install virtualenv`

   :::{note}
   If you're using a Unix-based system, you might need to use {command}`sudo pip install virtualenv`.
   :::

2. Create an environment for sphinx tools:

   {command}`virtualenv doc-env`

3. Activate the environment:

   > - On GNU/Linux:
   >
   >   > {command}`source doc-env/bin/activate`
   >
   > - On Windows:
   >
   >   > {command}`doc-env\\Scripts\\activate.bat`

4. Install Sphinx:

   {command}`pip install sphinx`

## Get documentation sources

1. Go to a folder where you keep sources:

   {command}`cd src`

2. Clone documentation from the repository:

   {command}`git clone https://github.com/tango-controls/tango-doc.git`

3. Change current folder to the documentation folder:

   {command}`cd tango-doc`

4. Install extra requirements (like sphinx theme):

   {command}`pip install -r requirements.txt`

5. Try to build the documentation:

   {command}`sphinx-build source build`

6. Open build/index.html with your favorite browser to see if it has been built correctly.

(updating-doc)=

## Updating documentation

1. Create your local working branch:

   :::{note}
   The following command creates a branch based on `origin/master`.
   If you would like to contribute to another branch, e.g. directly to `9.2.5`, you need to use:
   {command}`git checkout -b "TD-66-step-by-step-demo" origin/9.2.5`

   To see what what branch is the current one use: {command}`git branch -a`. The current branch is marked
   with an asterisk (\*).
   :::

   {command}`git checkout -b "TD-66-step-by-step-demo" origin/master`

2. Edit a file (or create it if it doesn't exist) you would like to change. If you are following this tutorial for learning
   please use this file: {file}`source/tutorials-and-howtos/tutorials/example.rst`

3. Make sure that the file appears in a relevant toc-tree (in some {file}`index.rst` file or
   in {file}`source/contents.rst`). If you are now learning please check {file}`source/tutorials/index.rst`

4. Check if your changes have built correctly:

   {command}`sphinx-build source build`

5. Check results with a browser. If you've edited the example, open {file}`build/tutorials/index.html`

If everything is OK, you may commit changes and send a pull request (ask to review and merge into an on-line branch).

## Committing changes

1. Add modifications to a commit list. For example:

   {command}`git add source/tutorials-and-howtos/tutorials/example.rst`

   {command}`git add source/tutorials-and-howtos/tutorials/index.rst`

2. Commit the changes providing some meaningful message. For example:

   {command}`git commit -m "doing tutorial"`

   :::{note}
   The changes are now committed to your local repository. To share them, you need to push. You may repeat
   editing, checking and commit steps several times without pushing util you are happy with your work. This
   way you may track the history of changes.
   :::

3. If your work took a long time it is good to do rebasing with recent changes done by someone else. For example:

   {command}`git fetch origin`

   {command}`git rebase origin/master`

   :::{note}
   If you are contributing to other branch than `master`, for example directly to the `9.5.2`, you need to
   call {command}`git rebase 9.5.2`
   :::

## Pushing (to the GitHub repository)

1. Push your changes to the origin repository. For example:

   {command}`git push -u origin TD-66-step-by-step-demo`

Now you are ready to ask for merging by sending a pull request on GitHub.

## Pull request (asking for merge)

1. Go to <https://github.com/tango-controls/tango-doc>
2. Click the button {guilabel}`New pull request`.
3. On the {guilabel}`base` selector select the branch you want to update (usually `master` or some `#.#.#`).
4. On the {guilabel}`compare` selector select your branch.
5. Provide a relevant comment and click {guilabel}`Create pull request`.

Now, someone will review your contribution, merge into selected branch and publish. If he/she finds some issues,
he/she will get back to you.

## Continuing the contribution

If you would like to come up with some other contribution, you do not need to clone sources again. Follow the following
steps:

1. Fetch changes from the origin repository:

   {command}`git fetch origin`

2. Switch to the main branch you are going to update (for example 9.2.5):

   {command}`git checkout origin/9.2.5`

3. Pull the changes:

   {command}`git pull`

4. Follow steps from [Updating documentation ](#updating-doc)





