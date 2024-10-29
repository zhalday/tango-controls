---
substitutions:
  image: |-
    ```{image} how-to-first-device-class/PogoFileImage.png
    ```
  image0: |-
    ```{image} how-to-first-device-class/PogoFirstConfiguration.png
    ```
  image1: |-
    ```{image} how-to-first-device-class/PogoEmptyImage.png
    ```
  image2: |-
    ```{image} how-to-first-device-class/PogoFilled.png
    ```
  image3: |-
    ```{image} how-to-first-device-class/PogoGenerateButton.png
    ```
  image4: |-
    ```{image} how-to-first-device-class/PogoGenerate.png
    ```
  image5: |-
    ```{image} how-to-first-device-class/PogoFilesGenerated.png
    ```
---

(how-to-write-first-device-class)=

# How to write your first Device Class

{audience}`developers`, {lang}`all`

This HowTo explains how to create your first Device Class regardless of the language used.

Prerequisite : Tango Environment.

## Start [Pogo ](#pogo-manual) Generator

Now you can create a new Class. Click on {{ image }} and New.

## Fill in your Class

Fill in required informations.
The Device Class identification on the left part and the description on the right.

{{ image0 }}

You will see an empty Pogo interface.

{{ image1 }}

You can add some Properties, Commands and Attributes, by double-clicking on each one.
There are different possible configuraton.

{{ image2 }}

## Generate

Generate your files {{ image3 }}
Choose your folder's path and files you want to create. For example, on linux OS with Cpp language, the minimum is XMI File, Code files and Makefile like you can see behind.

{{ image4 }}

You can now see {program}`Pogo`'s files in your folder. {program}`Pogo` had create skeleton files with your Properties, Commands and Attributes.

{{ image5 }}

Now you have a basic server who's make nothing. You can provide contents or fill it with different needs.

You can have some informations about how to start [here ](#getting-started-as-developer)

You can have more informations about device server usage [here ](#device-api).

How to fill your device in [Cpp ](#cpp-client-programmers-guide), [Java ](#getting-started-with-jtango-server) and [Python ](#getting-started-pytango)

## Compile And Run

Now you can compile and [Run ](#howto-start-device-server) your Class.

% definitions
% --------------
