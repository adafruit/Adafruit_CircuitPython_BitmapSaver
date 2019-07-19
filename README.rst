Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-bitmapsaver/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/bitmapsaver/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.com/adafruit/Adafruit_CircuitPython_BitmapSaver.svg?branch=master
    :target: https://travis-ci.com/adafruit/Adafruit_CircuitPython_BitmapSaver
    :alt: Build Status

Save a displayio.Bitmap (and associated displayio.Palette) into a BMP file.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

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
    python3 -m venv .env
    source .env/bin/activate
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
    from adafruit_bitmap_saver import save_bitmap

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
    save_bitmap(bitmap, palette, '/sd/test.bmp')

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_BitmapSaver/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Building locally
================

Zip release files
-----------------

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

    source .env/bin/activate

Then run the build:

.. code-block:: shell

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-bitmapsaver --library_location .

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.
