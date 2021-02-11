Download MicroPython binaries
=============================

By means of Python, download ESP32 MicroPython binaries from https://micropython.org/download/esp32/ to a local folder on a PC.

Only the missing binaries will be downloaded.

This list of files will be determined with **selenium** and the downloads are done with **requests**.

The name of the local folder to use is stored in `micropython.ini` like the following example:

    [server]
    webpage = https://micropython.org/download/esp32/
    downloadpage = https://micropython.org/resources/firmware/
    
    [local]
    targetfolder = D:/hva/installed_dev/Arduino/MicroPython/firmware/
    
    [options]
    include_unstable = False

When the option `include_unstable` is set to `True`, then the unstable releases will be downloaded as well.

20210211, HenkA, version 1.1