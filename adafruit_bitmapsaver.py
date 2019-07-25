# The MIT License (MIT)
#
# Copyright (c) 2019 Dave Astels for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_bitmapsaver`
================================================================================

Save a displayio.Bitmap (and associated displayio.Palette) into a BMP file.


* Author(s): Dave Astels

Implementation Notes
--------------------

**Hardware:**


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports

import struct
from displayio import Bitmap, Palette

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BitmapSaver.git"

#pylint:disable=line-too-long,broad-except,redefined-outer-name

def _write_bmp_header(output_file, filesize):
    output_file.write(bytes('BM', 'ascii'))
    output_file.write(struct.pack('<I', filesize))
    output_file.write(b'\00\x00')
    output_file.write(b'\00\x00')
    output_file.write(struct.pack('<I', 54))

def _write_dib_header(output_file, bitmap):
    output_file.write(struct.pack('<I', 40))
    output_file.write(struct.pack('<I', bitmap.width))
    output_file.write(struct.pack('<I', bitmap.height))
    output_file.write(struct.pack('<H', 1))
    output_file.write(struct.pack('<H', 24))
    output_file.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

def _bytes_per_row(bitmap):
    pixel_bytes = 3 * bitmap.width
    padding_bytes = (4 - (pixel_bytes % 4)) % 4
    return pixel_bytes + padding_bytes

def _write_pixels(output_file, bitmap, palette):
    row_buffer = bytearray(_bytes_per_row(bitmap))

    for y in range(bitmap.height, 0, -1):
        buffer_index = 0
        for x in range(bitmap.width):
            pixel = bitmap[x, y-1]
            color = palette[pixel]
            for _ in range(3):
                row_buffer[buffer_index] = color & 0xFF
                color >>= 8
                buffer_index += 1
        output_file.write(row_buffer)

def save_bitmap(bitmap, palette, file_or_filename):
    """Save a bitmap (using an associated palette) to a 24 bit per pixel BMP file.

    :param bitmap: the displayio.Bitmap to save
    :param palette: the displayio.Palette to use for looking up colors in the bitmap
    """
    if not isinstance(bitmap, Bitmap):
        raise ValueError('First argument must be a Bitmap')
    if not isinstance(palette, Palette):
        raise ValueError('Second argument must be a Palette')
    try:
        if isinstance(file_or_filename, str):
            output_file = open(file_or_filename, 'wb')
        else:
            output_file = file_or_filename

        filesize = 54 + bitmap.height * _bytes_per_row(bitmap)
        _write_bmp_header(output_file, filesize)
        _write_dib_header(output_file, bitmap)
        _write_pixels(output_file, bitmap, palette)
    except Exception:
        raise
    else:
        output_file.close()
