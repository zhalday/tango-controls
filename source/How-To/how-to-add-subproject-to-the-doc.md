# How to add a subproject to the readthedocs tango-controls documentation

{audience}`developers`

## Introduction

In some specific cases, it can be useful to integrate the documentation of an existing Tango-related
project into <https://tango-controls.readthedocs.io> website as subproject while keeping
the source of this documentation in its own independent repository.

The main advantages of this solution will be:
- the subproject documentation will be searchable from <https://tango-controls.readthedocs.io> website
- the subproject documentation can stay in the subproject repository, so the subproject documentation
can be easily updated/synchronized when new features are implemented

## Official Readthedocs documentation

Please refer to <https://docs.readthedocs.io/en/stable/subprojects.html> for the official
readthedocs documentation describing how several documentation projects can be combined and presented
to the reader on the same website.

## Adding a subproject

To add a subproject to <https://tango-controls.readthedocs.io> website, you need to have admin
rights on the readthedocs project you want to integrate and on tango-controls readthedocs project.
If it's not the case, please get in touch with the all mighty admins of these readthedoc projects.
You can know who is admin by looking at
[TangoTickets Readme file](https://gitlab.com/tango-controls/TangoTickets#online-services-used).

You can then add one of the tango-controls readthedocs maintainers as maintainers of the project
you want to add as subproject.
To do that, you need to:
1- login on <https://readthedocs.org> with your readthedocs account
2- click on the project you want to integrate as subproject
3- click on the `admin` button/tab
4- click on the `maintainers` left menu entry
5- add one of the tango-controls readthedocs maintainers e-mail address or readthedocs username
in the appropriate text field in the `Add maintainer` section and click on the `Add` button.

Then the tango-controls readthedoc admin which is now co-maintainer of the subproject will
have to follow the procedure described on
[the official Readthedocs documentation](https://docs.readthedocs.io/en/stable/guides/subprojects.html#adding-a-subproject)
to know how to add a subproject.

Once this step is done, the subproject documentation of a subproject named tangosubproject will be available under
https://tango-controls.readthedocs.io/projects/tangosubproject/ URL.

:::{note}
When adding a subproject, you can specify an alias name for the subproject (e.g. tangosubprojectalias).
This name will be used in the URL used to access to the subproject documentation. e.g.: https://tango-controls.readthedocs.io/projects/tangosubprojectalias/
Please refer to <https://docs.readthedocs.io/en/stable/subprojects.html#using-aliases> for more details.
:::

## Use Intersphinx to reference your subproject from other projects

You should use Intersphinx to reference your subproject from tango-controls readthedocs
and other readthedocs projects.
Please refer to the
[ReadTheDocs official documentation](https://docs.readthedocs.io/en/stable/guides/intersphinx.html) to
learn how to configure your subproject to use Intersphinx.
