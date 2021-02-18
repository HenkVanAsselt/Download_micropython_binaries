"""Download micropython ESP32 binaries from https://micropython.org/download/esp32/
Only the missing binaries will be downloaded.

This list of files and the downloads are done with 'requests'

20210211, HenkA, version 1.0
"""

# Global imports
import configparser
import pathlib
import requests
import re


# -----------------------------------------------------------------------------
def get_server_binfile_names(webpage) -> list:
    """From  the micropython esp32 download page, get the names of the available binary files

    :param webpage: URL of the webpage to inspect
    :returns: list of available bin filenames on the server
    """

    print(f"Determining binfiles available on {webpage}")

    filenames = []

    r = requests.get(webpage)
    
    regex = r"(esp32-.*\.bin)\""
    matches = re.finditer(regex, r.text, re.MULTILINE)
    
    for index,item in enumerate(matches,start=1):
        filenames.append(item.group(1))

    return filenames


# -----------------------------------------------------------------------------
def get_local_binfile_names(target_folder) -> list:
    """Create a list of already downloaded micropython bin files.

    :param target_folder: folder to inspect for binfiles
    :return: list of available files.
    """

    print(f"Determining binfiles available lcoally in {target_folder}")

    # We are only interested in the esp32 bin files
    local_bin_files = pathlib.Path(target_folder).glob("esp32-*.bin")

    local_filelist = []
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

    print(f"Downloading {filename} to {targetfolder}")

    url = f"{webpage}/{filename}"
    print(f"{url=}")

    r = requests.get(url, allow_redirects=True)

    targetfile = pathlib.Path(targetfolder, filename)
    print(f"{targetfile=}")

    with open(targetfile, 'wb') as f:
        f.write(r.content)




# -----------------------------------------------------------------------------
def main() -> None:

    # Read the configuration file
    config = configparser.ConfigParser()
    config.read('micropython.ini')

    # From the ESP32 webpage, get the names of the available bin files
    webpage = config['server'].get('webpage')
    server_bin_files = get_server_binfile_names(webpage)
    print(f"Webserver bin files = {server_bin_files}\n")

    # Determine which binfiles are already downloaded
    target_folder = config['local'].get('targetfolder')
    local_bin_files = get_local_binfile_names(target_folder)
    print(f"Local bin files: {local_bin_files}\n")

    # Determine which binfiles should still be downloaded
    missing_files = [filename for filename in server_bin_files if filename not in local_bin_files]
    include_unstable = config['options'].getboolean('include_unstable')

    if not include_unstable:
        print("Filtering out unstable bin files")
        missing_files = [filename for filename in missing_files if 'unstable' not in filename]
        print(f"New list: {missing_files}\n")

    if not missing_files:
        print(f"{target_folder} is up-to-date.\n")
        return
    else:
        print(f"Missing binfiles: {missing_files}\n")

    # Download the missing bin files from the micropython web server
    downloadpage = config['server'].get('downloadpage')
    for filename in missing_files:
        download_binfile(downloadpage, filename, target_folder)


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
