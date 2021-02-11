"""Download micropython ESP32 binaries from https://micropython.org/download/esp32/
Only the missing binaries will be downloaded.

This list of files will be determined with 'selenium' and the downloads are done with 'requests'

20210211, HenkA, version 1.0
"""

# Global imports
import configparser
import pathlib
import requests

# 3rd party imports
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


# -----------------------------------------------------------------------------
def get_bin_filenames(webpage) -> list:
    """From  the micropython esp32 download page, get the names of the available binary files

    :param webpage: URL of the webpage to inspect
    :returns: list of available bin filenames on the server
    """

    filenames = []

    opts = Options()
    opts.headless = True
    assert opts.headless # Operating in headless mode
    browser = Chrome(options=opts)
    browser.get(webpage)

    references = browser.find_elements_by_css_selector('a')
    for ref in references:
        if ref.text.startswith("esp32-") and ref.text.endswith(".bin"):
            filenames.append(ref.text)

    browser.close()
    return filenames


# -----------------------------------------------------------------------------
def get_local_binfiles(target_folder) -> list:
    """Create a list of already downloaded micropython bin files.

    :param target_folder: folder to inspect for binfiles
    :return: list of available files.
    """

    local_filelist = []

    local_bin_files = pathlib.Path(target_folder).glob("esp32-*.bin")
    for filename in local_bin_files:
        local_filelist.append(filename.name)

    return local_filelist

# -----------------------------------------------------------------------------
def download_binfile(webpage, filename, targetfolder):
    """Download the given filename from the webpage.

    :param webpage: The URL where the file can be found
    :param filename: Name of the file to download
    :param targetfolder: Local folder to save the file in
    """

    url = f"{webpage}/{filename}"
    print(f"{url=}")

    r = requests.get(url, allow_redirects=True)

    targetfile = pathlib.Path(targetfolder, filename)
    print(f"{targetfile=}")

    with open(targetfile, 'wb') as f:
        f.write(r.content)


# -----------------------------------------------------------------------------
def main():

    # Read the configuration file
    config = configparser.ConfigParser()
    config.read('micropython.ini')

    # From the ESP32 webpage, get the names of the available bin files
    webpage = config['server'].get('webpage')
    server_bin_files = get_bin_filenames(webpage)
    print(f"Webserver files = {server_bin_files}")

    # Determine which binfiles are already downloaded
    target_folder = config['local'].get('targetfolder')
    local_bin_files = get_local_binfiles(target_folder)
    print(f"Local file list: {local_bin_files}")

    # Download the missing bin files from the micropython web server
    downloadpage = config['server'].get('downloadpage')
    for filename in server_bin_files:
        if filename not in local_bin_files:
            print(f"Downloading {filename} to {target_folder}")
            download_binfile(downloadpage, filename, target_folder)


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
