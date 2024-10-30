% Tango Controls documentation master file, created by
% sphinx-quickstart on Sat Aug  6 21:40:12 2016.
% You can adapt this file completely to your liking, but it should at least
% contain the root `toctree` directive.

# Welcome to the Tango Controls documentation!

{audience}`all`

```{toctree}
:name: maintoc
:maxdepth: 2
:hidden: True

Explanation/index
Tutorials/index
How-To/index
tools/tools
Reference/index
authors
Old-but-precious/index
```

Welcome!

This is a collection of documents for our Tango Controls community, users of Tango Controls, developers and interested parties. Among the many items that we cover here are explanations of what Tango Controls is, how to use Tango Controls for your controls system, how to write software using the Tango Controls framework and how to use Tango Controls and its tools.

Nothing is perfect and so is this documentation. In the likely case that you find that information is missing, please get in touch with us. Ideally you would simply [open an issue on Gitlab](https://gitlab.com/tango-controls/tango-doc/-/issues/new) so that we can address what you found.


## How this documentation is organized

The Tango Controls documentation follows largely the [Grand Unified Theory of Documentaiton](https://docs.divio.com/documentation-system/) and is organised in the following categories (with some overlap):

- {doc}`Explanation <Explanation/introduction>`: Overview of what Tango Controls is, its origins and who uses it. **If you are new to Tango Controls, then we recommend that you start reading there.**
- {doc}`Tutorials <Tutorials/index>`: We show you how to implement a Tango Devices, Tango clients and other Tango-related software.
- {doc}`How-Tos <How-To/index>`: Here we provide solutions to specific problems that might encounter on the road with Tango Controls.
- {doc}`Reference <Reference/reference>`: Tango Controls' main programming languages are C++, Java and Python. You will find their APIs here. We also support other languages and tools through bindings that we document here as well.
- {doc}`Tools <tools/tools>`: The Tango Controls ecosystem is rich with tools that make eveybody's life easier. Here we show you which tools exist and what one can do with them.

To support our readers in their quest to quickly find the information that they are looking for, we have tagged the pages here with one or more labels:

- **Programming language**: Pages that contain information that is relevant to software development are tagged with either one of the three main languages that Tango Controls supports (**c++**, **java**, **python**). If the information on a page is programming language independent, we have tagged it with **all**.
- **Target audience**:
- - **all**: The information on the page might be interesting for general audience, i.e. evrybody.
- - **developers**: Developers will likely find the information on the page interesting, i.e. it will help them with their implementation of Tango Devices, clients or Tango Controls software in general.
- - **administrators**: A page with this tag will be useful to the people who have to build, maintain or fix a Tango Controls system.

We understand that it is easy to get lost here due to the sheer amount of information. Therefore we provide below some suggestions to get you started:

- The {doc}`Overview <Explanation/overview>` will give you a quick overview of what Tango Controls is, its origins and who uses it. If you are new to Tango Controls, then this is where we recommend to start reading.
- {doc}`First steps <How-To/getting-started/first-steps>` will guide you through the process to get started with Tango Controls. This category includes an overview of Tango Controls concepts, procedures for installation and starting the system as well as *Getting started* tutorials.
- {doc}`Explanation/development/index` provides information for **Developers** that comes handy when developing {term}`Device Servers <device server>`, {term}`Devices <device>` and client applications.
- The {doc}`Admin and maintenance <How-To/deployment/index>` section is important mainly for **System Administrators**. However, it may provide some information for both **End Users** and **Developers**, too. It contains useful information on Tango Controls system deployment, startup and maintenance.
- You will find that Tango comes with a rich set of {doc}`tools <tools/tools>`. They are command line tools, graphical toolkits and programming tools for management, developing graphical applications, connecting with other systems and applications. All, **End Users**, **Developers** and **System Adminstrators**, should take a look at the toolkits' manuals.
- {doc}`Tutorials <Tutorials/index>` and {doc}`HOWTOs <How-To/index>` give step by step guidance and teach you how to work with Tango Controls or get your job efficiently done.
- If you would like to contribute to the documentation please read the document
  {doc}`How to work with Tango Controls documentation <How-To/contributing/contributing>` and the
  {doc}`Documentation workflow tutorial <How-To/contributing/docs>` .

## Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
- {ref}`Glossary <glossary>`
