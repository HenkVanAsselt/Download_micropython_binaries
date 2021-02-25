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

Alternative
-----------

The main reason for this project was to get some experience with **selenium**.

As `nursanamar` pointed out, this can also be done with `requests` and `re`, thus not
using selenium at all:

    def get_server_binfile_names(webpage) -> list:
        """From  the micropython esp32 download page, get the names of the available binary files

        :param webpage: URL of the webpage to inspect
        :returns: list of available bin filenames on the server
        """

    print(f"Determining binfiles available on {webpage}")

    import re
    
    filenames = []
    r = requests.get(webpage)
    
    regex = r"(esp32-.*\.bin)\""
    matches = re.finditer(regex, r.text, re.MULTILINE)
    
    for index,item in enumerate(matches,start=1):
        filenames.append(item.group(1))
    
    return filenames