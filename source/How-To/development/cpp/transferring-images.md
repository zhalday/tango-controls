(transfering-images)=

# Transferring images

```{tags} audience:developers, lang:c++,python
```

%[glossary_term][EncodedAttribute]
%Special attribute data type for 2D image data.

Some optimized methods are available for image transfer
between clients and servers using the attribute data type `DevEncoded`
and all these methods have been merged in a class called EncodedAttribute.

Within this class, you will find methods to:

- Encode an image in a compressed way (JPEG) for images coded on 8
  (gray scale), 24 or 32 bits
- Encode a grey scale image coded on 8 or 16 bits
- Encode a color image coded on 24 bits
- Decode images coded on 8 or 16 bits (gray scale) and returned a 8 or
  bits grey scale image
- Decode color images transmitted using a compressed format (JPEG) and
  returns a 32 bits RGB image

The following code snippets are examples of how these methods have to be
used.

:::::{tab-set}

::::{tab-item} C++

On the server side, create an instance of the EncodedAttribute class within your object

```{code} cpp
:number-lines: 1

  class MyDevice : public TANGO_BASE_CLASS
  {
      ...
      Tango::EncodedAttribute jpeg;
      ...
  };
```

::::

::::{tab-item} Python

Just define an attribute with the expected `dtype`.

```{code} python
:number-lines: 1

  class TestDevice(Device):

      @attribute(dtype=DevEncoded, access=AttrWriteType.READ)
      def attr(self):
        ...
```

::::

:::::

In the code of your device, use an encoding method of the EncodedAttribute class:

:::::{tab-set}

::::{tab-item} C++

```{code} cpp
:number-lines: 1

  void MyDevice::read_Encoded_attr_image(Tango::Attribute &att)
  {
    ....
    jpeg.encode_jpeg_gray8(imageData, 256, 256, 50.0);
    att.set_value(&jpeg);
  }
```

:::{list-table}
:widths: 5 40
:header-rows: 1

*
  - Line
  - Explanation
*
  - 4
  - Image encoding. The size of the image is 256 by 256. Each pixel is coded using 8 bits. The encoding
    quality is defined to 50 in a scale of 0 - 100. `imageData` is the pointer to the image data (pointer to
    unsigned char).
*
  - 5
  - Set the value of the attribute using the `Attribute::set_value()` method.
:::

::::

::::{tab-item} Python

```{code} python
:number-lines: 1

  def read_Encoded_attr_image(self):
    enc = tango.EncodedAttribute()
    data = numpy.arange(100, dtype=numpy.byte)
    data = numpy.array((data, data, data))
    enc.encode_jpeg_gray8(data, quality = 50)
    return enc
```

:::{list-table}
:widths: 5 40
:header-rows: 1

*
  - Line
  - Explanation
*
  - 2
  - Create an Encoded Attribute object
*
  - 3 - 4
  - Create the raw image data
*
  - 5
  - Encode with 50% quality
:::

::::

:::::

On the client side, the code is the following (without exception management):

:::::{tab-set}

::::{tab-item} C++

```{code} cpp
:number-lines: 1

  ....
  DeviceAttribute da;
  EncodedAttribute att;
  int width,height;
  unsigned char *gray8;

  da = device.read_attribute("Encoded_attr_image");
  att.decode_gray8(&da, &width, &height, &gray8);
  ....
  delete[] gray8;
  ...
```

:::{list-table}
:widths: 5 40
:header-rows: 1

*
  - Line
  - Explanation
*
  - 7
  - Attribute named `Encoded_attr_image` is read.
*
  - 8
  - The image is decoded in a 8 bits gray scale format and stored in the buffer pointed to by `gray8`.
*
  - 10
  - The memory allocated by the image decoding at line 8 is returned.
:::

::::

::::{tab-item} Python

```{code} python
:number-lines: 1

  da = dev.read_attribute("Encoded_attr_image", extract_as=tango.ExtractAs.Nothing)
  enc = tango.EncodedAttribute()
  data = enc.decode_gray8(da)
```

:::{list-table}
:widths: 5 40
:header-rows: 1

*
  - Line
  - Explanation
*
  - 1
  - Attribute named `Encoded_attr_image` is read with the special `extract_as` argument of `Nothing`, see the
    [EncodedAttribute](inv:pytango:py:class#tango.EncodedAttribute) documentation for more details.
*
  - 2
  - The image is decoded in a 8 bits gray scale format.
:::

::::

:::::
