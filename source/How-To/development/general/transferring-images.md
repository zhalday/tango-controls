(transfering-images)=

# Transfer images

```{tags} audience:developers, lang:all
```

There exists a set of methods that have been written to optimise image transfer
between clients and servers using the attribute `DevEncoded` data type.
These methods are contained in a class called `EncodedAttribute`.
Within this class, you will find methods to:

- Encode an image in a compressed format (JPEG) for images coded on 8
  (gray scale), 24 or 32 bits
- Encode a grey scale image coded on 8 or 16 bits
- Encode a color image coded on 24 bits
- Decode images coded on 8 or 16 bits (gray scale) and returned an 8 or
  bits grey scale image
- Decode color images transmitted using a compressed format (JPEG) and
  returns a 32 bits RGB image

The following code snippets are examples of how these methods should be
used in a server and in a client.

The **server** needs to creates an instance of the EncodedAttribute class
within your object and can then use an encoding method from the
EncodedAttribute class, e.g.

:::::{tab-set}

::::{tab-item} C++

```{code} cpp
:number-lines: 1

 class MyDevice::TANGO_BASE_CLASS
  {
      ...
      Tango::EncodedAttribute jpeg;
      ...
  }

  ...

 void MyDevice::read_Encoded_attr_image(Tango::Attribute &att)
  {
      ....
      jpeg.encode_jpeg_gray8(imageData,256,256,50.0);
      att.set_value(&jpeg);
  }
```
Line 13: Perform the image encoding. The size of the image is *256* by *256*. Each pixel
is coded using 8 bits. The encoding quality is defined to *50* in the scale
of 0 - 100. *imageData* is a pointer to the image data (unsigned chars).

Line 14: Set the value of the attribute using a `Attribute::set_value()`
method.
::::

::::{tab-item} Python

```{code} python
:number-lines: 1

  def read_Encoded_attr_image(self, att, image_data):
      jpeg = tango.EncodedAttribute()
      jpeg.encode_jpeg_gray8(image_data,256,256,50.0)
      att.set_value(jpeg)
```
Line 4: Perform the image encoding. The size of the image is *256* by *256*. Each pixel
is coded using 8 bits. The encoding quality is defined to *50* in the scale
of 0 - 100. *image_data* is the image data passed into the method.

Line 5: Set the value of the attribute using a `set_value()`
method.
::::

:::::



A snippet of the code then required on the **client** side is shown below (note:
shown without any exception management):

:::::{tab-set}

::::{tab-item} C++

```{code} cpp
:number-lines: 1

    ...
    DeviceAttribute da;
    EncodedAttribute att;
    int width,height;
    unsigned char *gray8;

    da = device.read_attribute("Encoded_attr_image");
    att.decode_gray8(&da,&width,&height,&gray8);
    ...
    delete [] gray8;
    ...
```

The attribute named *Encoded_attr_image* is read at line 7. The image is
decoded at line 8 in a 8 bits gray scale format. The image data are
stored in the buffer pointed to by *gray8*. The memory allocated by the
image decoding at line 8 is returned to the system at line 10.
::::

::::{tab-item} Python

```{code} python
:number-lines: 1

    ...
    dev = tango.DeviceProxy("a/b/c")
    da = dev.read_attribute("Encoded_attr_image", extract_as=tango.ExtractAs.Nothing)
    enc = tango.EncodedAttribute()
    gray8 = enc.decode_gray8(da)
    ...
```

The attribute named *Encoded_attr_image* is read at line 3. Note that the
argument `ExtractAs.Nothing` is required in this case as by default
the call that returns a `DeviceAttribute` in PyTango automatically
extracts the contents.

The image is decoded at line 5 in an 8 bits gray scale format. The image data are
stored in the variable *gray8*.
::::

:::::
