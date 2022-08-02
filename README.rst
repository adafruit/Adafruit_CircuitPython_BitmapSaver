Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-bitmapsaver/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/bitmapsaver/en/latest/
    :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_BitmapSaver/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_BitmapSaver/actions/
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

Save a displayio.Bitmap (and associated displayio.Palette) into a BMP file.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

CircuitPython 5.0 or later is required.

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
=====================
.. note:: This library is not available on PyPI yet. Install documentation is included
   as a standard element. Stay tuned for PyPI availability!

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-bitmapsaver/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-bitmapsaver

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-bitmapsaver

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install adafruit-circuitpython-bitmapsaver

Usage Example
=============

.. code-block:: python

    import board
    import busio
    import digitalio
    from displayio import Bitmap, Palette
    import adafruit_sdcard
    import storage
    from adafruit_bitmapsaver import save_pixels

    print('Setting up SD card')
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = digitalio.DigitalInOut(board.SD_CS)
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")

    WHITE = 0xFFFFFF
    BLACK = 0x000000
    RED = 0xFF0000
    ORANGE = 0xFFA500
    YELLOW = 0xFFFF00
    GREEN = 0x00FF00
    BLUE = 0x0000FF
    PURPLE = 0x800080
    PINK = 0xFFC0CB

    colors = (BLACK, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE)

    print('Building sample bitmap and palette')
    bitmap = Bitmap(16, 16, 9)
    palette = Palette(len(colors))
    for i, c in enumerate(colors):
        palette[i] = c

    for x in range(16):
        for y in range(16):
            if x == 0 or y == 0 or x == 15 or y == 15:
                bitmap[x, y] = 1
            elif x == y:
                bitmap[x, y] = 4
            elif x == 15 - y:
                bitmap[x, y] = 5
            else:
                bitmap[x, y] = 0

    print('Saving bitmap')
    save_pixels('/sd/test.bmp', bitmap, palette)

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/bitmapsaver/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_BitmapSaver/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
