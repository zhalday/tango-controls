(long-term-support)=

# Long Term Support

```{tags} audience:administrators, audience:developers
```

In 2016, the [Tango-Controls Steering Committee](https://www.tango-controls.org/about-us/executive-2016/) requested the
introduction of Long Term Support versions for some key components of Tango-Controls like cppTango, the C++ Tango Library and JTango.

Long Term Support (LTS) versions are special versions of Tango components which will be supported for 5 years (starting
from the day when the next direct major version is released).

LTS versions will benefit from critical bug fixes and potentially some patches for simple new features and less critical bugs.

For cppTango, the latest 9.3 version became an LTS version when cppTango 9.4.0 was released on September 30th 2022. This
means that cppTango 9.3.x will be supported until October 2nd 2027.

For the LTS versions only cppTango 9.3.x and starter will stay at C++98, all other projects can require newer C++ standards.

For PyTango there is no LTS policy. PyTango releases target the most recent minor release of cppTango.
Critical bug fixes to PyTango for unsupported cppTango releases are not planned.
