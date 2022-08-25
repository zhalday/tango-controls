.. _lts:

Long Term Support Versions
==========================

:audience:`administrators, developers`

In 2016, the `Tango-Controls Steering Committee <https://www.tango-controls.org/about-us/executive-2016/>`_ requested the introduction of Long Term Support versions for some key components of Tango-Controls like cppTango, the C++ Tango Library and JTango.

Long Term Support (LTS) versions are special versions of Tango components which will be supported for at least 5 years (starting from the day when the next direct major version is released).
LTS versions will benefit from critical bug fixes and potentially some patches for simple new features and less critical bugs.

For cppTango, the latest 9.3 version (currently 9.3.5) will become a LTS version as soon as cppTango 9.4.0 will be released (foreseen on October 2nd 2022).
This means that cppTango 9.3 will be supported until October 2nd 2027.

For PyTango there is no LTS policy. PyTango releases target the most recent minor release of cppTango.
This means that PyTango currently (July 2022) supports cppTango 9.3.x.
After cppTango 9.4.0 is released, future PyTango releases will support cppTango 9.4.x.
Critical bug fixes to PyTango for unsupported cppTango releases are not planned.

