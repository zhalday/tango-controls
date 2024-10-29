(documentation-workflow-tutorial)=

# Tango Documentation

{audience}`developers`

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





