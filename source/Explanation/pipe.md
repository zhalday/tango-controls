(tango-pipe-model)=
# Pipe

:::{note}
**Warning**: The Pipe Feature will get deprecated when the DevDict feature will be implemented.
:::

## Introduction
A Tango Pipe is like an Attribute with a flexible data structure, name and description.
Unlike Commands or Attributes, a Pipe does not have a pre-defined data type.
Tango Pipe data types may be a mixture of the basic Tango data types (or array of) and may change every time a pipe is written.

## Use Case
Pipe can be used to:

1. To define complex data structures to act as a single Attribute.
2. To pass data structures of arbitrary type and size.
