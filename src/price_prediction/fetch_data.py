"""
Script that fetches DVF data from the French government website
"""
import argparse
import gzip
import logging
import os
import shutil

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BASE_URL = "https://files.data.gouv.fr/geo-dvf/latest/csv/"


def unzip_gz_file(input_path: str, output_path: str):
    """
    Unzip a .gz file.

    Arguments:
        input_path (str): The path to the input file.
        output_path (str): The path to the output file.

    Returns:
        None
    """
    with gzip.open(input_path, "rb") as f_in:
        with open(output_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def download_file(url: str, output_path: str):
    """
    Download a file from a URL.

    Arguments:
        url (str): The URL to download the file from.
        output_path (str): The path to the output file.

    Returns:
        None
    """
    response = requests.get(url, stream=True)

    response.raise_for_status()

    with open(output_path, "wb") as f:
        shutil.copyfileobj(response.raw, f)


def main():
    parser = argparse.ArgumentParser(description="Fetch DVF data.")
    parser.add_argument(
        "--years", nargs="+", help="The years to fetch.", type=str, required=True
    )
    parser.add_argument(
        "--output-dir",
        help="The directory to save the data to.",
        type=str,
        default="data",
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    for year in args.years:
        url = BASE_URL + f"/{year}/full.csv.gz"

        year_dir = os.path.join(args.output_dir, year)
        os.makedirs(year_dir, exist_ok=True)

        logger.info(f"Fetching data for year {year} from {url}...")
        try:
            download_file(url=url, output_path=os.path.join(year_dir, f"full.csv.gz"))
        except Exception as e:
            logger.exception(f"Failed to fetch data for year {year} from {url}")
            continue

        logger.info(f"Unzipping {year_dir}/full.csv.gz...")
        unzip_gz_file(
            input_path=os.path.join(year_dir, f"full.csv.gz"),
            output_path=os.path.join(year_dir, f"full.csv"),
        )

        logger.info(f"Done for year {year}.")


if __name__ == "__main__":
    main()
