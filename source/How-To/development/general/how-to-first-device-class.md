(how-to-write-first-device-class)=

# Create your first Device class

```{tags} audience:developers, lang:all
```

This How-to explains how to create your first Device class regardless of the language used.

Prerequisite: This how-to assumes that you have a Tango installed.

- Start [Pogo](#pogo-documentation) code generator: Now you can create a new class:
    - Click on ![pogo](how-to-first-device-class/PogoFileImage.png) and then {guilabel}`New`.

- Add the following required information for your class:
    - The Device Class identification information (shown in the left panel below)
    - The class name, language and description (shown in the right panel below)

    ```{image} how-to-first-device-class/PogoFirstConfiguration.png
    ```

- Once completed, you will see an empty Pogo interface:

    ```{image} how-to-first-device-class/PogoEmptyImage.png
    ```

    You can add {term}`Properties <Property>`, {term}`Commands <Command>` and {term}`Attributes <Attribute>` by double-clicking on each one.
    Below is an example after having defined some of these:

    ```{image} how-to-first-device-class/PogoFilled.png
    ```

- Generate your files from {guilabel}`File` -> {guilabel}`Generate` and press {guilabel}`OK` in the window.
    - Choose your output path and the files you want to create. For example, on linux OS in C++, the minimum set of files that need to be created are: an XMI file, Code files and a Makefile. See the example below:

        ```{image} how-to-first-device-class/PogoGenerate.png
        ```

    - You will now see the {program}`Pogo` generated files in your folder:
        ```{image} how-to-first-device-class/PogoFilesGenerated.png
        ```
        {program}`Pogo` has creates skeleton files with your Properties, Commands and Attributes.


- Next you will need to develop your device. Information on how to do this can be found in the language specific how-to sections: [C++](#cpp-client-programmers-guide), [Java](#getting-started-with-jtango-server) or [Python](#getting-started-pytango)

- Finally, to compile and run your class see the section on [how to start a device server](#howto-start-device-server).
