import concurrent.futures
import itertools
import re
import urllib.request
from typing import List

base_url = 'http://data.astrometry.net'
regex_exp = '(index-\d+(?:-\d+)?\.fits)<.*'

index_folders = ['4100', '4200', '5000', '6000', '6100']

final_urls = []


def _check_folder(folder: str) -> List:
    """
    Return a list of FITS files names within a specified folder
    """
    with urllib.request.urlopen(f'{base_url}/{folder}', timeout=5) as conn:
        names = re.findall(regex_exp, conn.read().decode())
        full_names = [f'{folder}/{name}' for name in names]
        return full_names


def _get_fits_file(name: str) -> None:
    """
    Read the file content and write it to the disk
    """
    try:
        with urllib.request.urlopen(f'{base_url}/{name}', timeout=5) as conn:
            with open(f'/{name.split("/")[1]}', 'wb+') as f:
                content = conn.read()
                f.write(content)
    except Exception as e:
        print(e)


def main():
    fits_list = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(_check_folder, folder): folder for folder in index_folders}
        for future in concurrent.futures.as_completed(futures):
            try:
                fits_list.append(future.result())
            except Exception as exc:
                print('%r generated an exception: %s' % (exc))
        fits_list = list(itertools.chain(*fits_list))
        {executor.submit(_get_fits_file, fits_name): fits_name for fits_name in fits_list}


if __name__ == '__main__':
    main()
