# Tango Core: Python

```{image} pytango/pytango_logo.png
```

## PyTango - a Python binding to Tango

[Python](https://www.python.org/) is a commonly used programming language in the scientific community, due to its many advantages
(the most important of those is probably simplicity of its syntax).
{term}`Tango Controls` also supports it in a form of a pybind11-based binding to the [cppTango](https://tango-controls.gitlab.io/cppTango/) implementation.

In "pythonic" terms, it is a package [available at PyPI](https://pypi.python.org/pypi/PyTango)
that exposes the complete Tango API (both the client and the server parts of it) as well as provides a framework
for unit-testing your {term}`device servers<device server>`.

:::{note}
You should use a PyTango version that has the same major and minor version numbers as cppTango that you have.
So if you have cppTango version X.Y.Z, you should have PyTango version X.Y.V (where V might equal Z,
but its not required).
:::



## PyTango usage

For instructions on how to use PyTango, the Python binding for Tango Controls,
please refer to the [PyTango documentation](inv:pytango:std#index)

(pytango-api-docs)=
## PyTango API reference

Please refer to [PyTango API documentation](inv:pytango:std:doc#api)
