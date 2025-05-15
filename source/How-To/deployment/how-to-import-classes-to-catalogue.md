# Import multiple device classes to the Catalogue

```{tags} audience:administrators
```

The Device Classes Catalogue is available on the Tango Controls web page at:
<https://www.tango-controls.org/developers/dsc/>.

A script can be used to import multiple device classes to the catalogue from a repository. This
is available to download [here](https://gitlab.com/tango-controls/dsc-import) and below or instructions
on how to use this script.

This can import information from a subversion (SVN), Git, Mercurial or FTP repositiory.

## Installation

This script requires:
- Python > 3.6
- Subversion (if importing from an SVN repository)

A list of the required Python modules is given in the [requirements.txt](https://gitlab.com/tango-controls/dsc-import/-/blob/master/requirements.txt?ref_type=heads) file.

The easiest way to install these is in a Python virtual environment:
```
# Create virtual environemnt
python -m venv venv

# Activate
source venv/bin/activate

# Install from requirements.txt
pip install -r requirements.txt
```


:::{warning}
Note if importing from SVN:

The library will not work if any of files in the SVN has no author defined, which is the case for tango-ds
repository on Sourceforge. To avoid this problem one can edit the Python svn module file {file}`svn/common.py`
around line 369 to have something like the following:

```python
author = ''
if commit_node.find('author') is not None:
   author = commit_node.find('author').text
```
:::


## How-to use the script to import multiple classes

1. Clone the import utility with git:
   ```
   git clone https://gitlab.com/tango-controls/dsc.git`
   cd dsc-import
   ```

2. Update so general variables in the settings.py file to reflect your environment and how you want
to import classes. Some of the important ones to consider might be:

   ```python
   FORCE_UPDATE = False  # when True no timestamps are checked and updates are performed
   USE_DOC_FOR_NON_XMI = True # when True, parse documentation to get xmi conntent for device servers without XMI
   ADD_LINK_TO_DOCUMENTATION = True # when True it provides a link to documentation

   # set the following variables to point to the repositories
   LOCAL_REPO_PATH = '/home/tango/tmp/tango-ds-repo/'  # local copy of the repository will be synced there
   LOG_PATH = '/home/tango/tmp/logs'  # where to log some information about import process

   # Tango Controls or test server address
   SERVER_BASE_URL = 'http://www.tango-controls.org/'
   ```

3. Configure to run:

   :::::{tab-set}
   ::::{tab-item} SVN
   In the settings.py file, configure the `REMOTE_REPO_HOST` and `REMOTE_REPO_PATH`:
   ```python
   REMOTE_REPO_HOST = 'svn.code.sf.net'  # host of the SVN repository (if using SVN repo)
   REMOTE_REPO_PATH = 'p/tango-ds/code'  # path within the server where the repository is located
   ```
   ::::
   ::::{tab-item} Other
   To import from another type of repository, for example Git, first define a *.csv* with the
   following content:
   ```
   name,repository_url,repository_type,tag,xmi_files_urls,pogo_docs_url_base,upload_xmi_file,readme_url,documentation_url,documentation_type,documentation_title,pogo_description_html,pogo_attributes_html,pogo_commands_html,pogo_properties_html
   ```
   The 'example-csv.csv' in the dsc-import repo provides an example on how to import from a Git repository:
   ```
   name,repository_url,repository_type,tag,xmi_files_urls,pogo_docs_url_base,upload_xmi_file,readme_url,documentation_url,documentation_type,documentation_title,pogo_description_html,pogo_attributes_html,pogo_commands_html,pogo_properties_html
   LiberaBrilliancePlus,https://github.com/MaxIV-KitsControls/Libera-BrilliancePlus,GIT,v1.2.1-alpha,https://raw.githubusercontent.com/MaxIV-KitsControls/Libera-BrilliancePlus/v1.2.1-alpha/src/LiberaBrilliancePlus.xmi,,,https://raw.githubusercontent.com/MaxIV-KitsControls/Libera-BrilliancePlus/v1.2.1-alpha/README.md,,,,,,,
   ```
   where:
   - name: LiberaBrilliancePlus
   - repository_url: https://github.com/MaxIV-KitsControls/Libera-BrilliancePlus
   - repository_type: GIT
   - tag: v1.2.1-alpha
   - xmi_files_urls: https://raw.githubusercontent.com/MaxIV-KitsControls/Libera-BrilliancePlus/v1.2.1-alpha/src/LiberaBrilliancePlus.xmi

      (**Note**: these need to be the 'raw' file from Git (View {guilabel}`Raw`))
   - readme_url: https://raw.githubusercontent.com/MaxIV-KitsControls/Libera-BrilliancePlus/v1.2.1-alpha/README.md

      (**Note**: Again needs to be the 'raw' file.)
   ::::
   :::::

3. Run the command:

   :::::{tab-set}
   ::::{tab-item} SVN
   ```
   python dsc_import_utility.py
   ```
   ::::
   ::::{tab-item} Other
   Add the `--csv-file` option to specify the file to use:
   ```
   python dsc_import_utility.py --csv-file <csv-file-name>.csv
   ```
   ::::
   :::::

   :::{note}
   You will be asked for your credentials for tango-controls.org. The import/update of
   device classes will be carried out under the account details provided.
   :::


## How the script works

During the import, the script will:

- Make a local copy of an SVN repository (in path defined by `LOCAL_REPO_PATH`). This speeds up the search process.

- Search this local copy for directories containing .XMI files. These are listed as candidates to be device servers.

- The list of candidates is processed and compared (by repository URL) with content in
  the Device Classes Catalogue:

  - If there are changes or `FORCE_UPDATE` is True the catalogue is updated

    - For device server without an .XMI file it looks for documentation servers and tries to parse html documentation
      generated by {program}`Pogo`.

  - If there are no changes the device server is skipped
