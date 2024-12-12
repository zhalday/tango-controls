"""
Script to append the javascript file to run during the sphinx build.
This should only be run during the readthedocs build (i.e. do not run it
locally) as the 'readthedocs.js' javascript code will disable the current
pydata theme's search dialog and replace it with the inbuilt readthedocs
search dialog that allows searching of subprojects.
"""
import glob

with open("source/conf.py", "a") as fp:
    fp.write("\nhtml_js_files = [\n\t'javascript/readthedocs.js',\n]\n")
