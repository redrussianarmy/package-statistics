"""Debian Package Statistics CLI Tool"""
import argparse
import os

from package_stats.content_file import ContentFile
from package_stats.exceptions import ContentIndiceForArchitectureNotFound


def main(mirror_url: str, arch: str, count: int, ascending: bool,
         output_dir: str, reuse_if_exists: bool) -> None:
    """This is the function that orchestrates the entirety of this application.

    1. Gets a list of all content indices from a repository
    2. Checks whether the provided architecture is valid or not
    3. Filters the content indices for the requested architecture
    4. Downloads the content indices file(s)
    5. Parses the content indices files(s)
    6. Prints out the package statistics

    Arguments:

        mirror_url: Debian mirror URL
        arch: System architecture
        count: Number of packages printed
        ascending: Sort output by number of package in ascending order.
        output_dir: Directory where the files are saved.
        reuse_if_exists: Use that content file if already downloaded

    """
    arch = arch.lower()
    content = ContentFile(mirror_url, arch, count, output_dir, reuse_if_exists)
    content_indices, content_indices_urls = content.get_content_indices()

    if len(content_indices_urls) == 0:
        # if given architecture is not in available architectures, error raises
        # with a list of available architectures
        available_architectures = content.get_arhitectures(content_indices)

        raise ContentIndiceForArchitectureNotFound(
            f"{arch} was not found in the given repository. "
            f"Available architectures are: {available_architectures}")

    complete_package_data = {}
    for url in content_indices_urls:
        content_indice_file = content.download_contents_file(url)
        package_data = content.parse_contents_indice(content_indice_file)
        complete_package_data.update(**package_data)

    package_list = complete_package_data.keys()

    # sort packages by number of packages in the ascending/descending order
    package_list = sorted(
        package_list, key=lambda x: len(complete_package_data[x]), reverse=not ascending)

    for idx, package in enumerate(package_list):
        if idx == 0:
            print(f"{'No.':<10}\t{'Package Name':<50}\tFile Count")
        print(
            f"{idx+1:<10}\t{package:<50}\t{len(complete_package_data[package])}")
        if idx+1 == count:
            break


def cli_main():
    """Command line interface"""
    parser = argparse.ArgumentParser(
        description=(
            "A tool that shows the package statistics by parsing a Contents Indice"
            " (source - https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices)"
            " from a debian mirror, taking into account the system architecture given."
        )
    )
    parser.add_argument(
        "arch", type=str,
        help="Architecture of the content indice to be parsed.")
    parser.add_argument(
        "-m", "--mirror_url", type=str,
        default="http://ftp.uk.debian.org/debian/dists/stable/main/",
        help=("Mirror URL where content file will be pulled "
              "DEFAULT http://ftp.uk.debian.org/debian/dists/stable/main/")
    )
    parser.add_argument(
        "-c", "--count", type=int, default=10,
        help="Number of packages to list. Use -1 to list all. DEFAULT 10")
    parser.add_argument(
        "-a", "--ascending", action="store_true",
        help="Sort package statistics list by number of files in ascending order. DEFAULT False")
    parser.add_argument(
        "-o", "--output-dir", type=str, default=os.getcwd(),
        help=("A directory to store downloaded content file."
              "DEFAULT <current-directory>")
    )
    parser.add_argument(
        "-r", "--reuse-if-exists",
        help=("Reuses a content file if it has been downloaded previously and "
              "exists in the output directory."),
        action="store_true",
    )
    args = parser.parse_args()
    main(
        mirror_url=args.mirror_url,
        arch=args.arch,
        ascending=args.ascending,
        count=args.count,
        output_dir=args.output_dir,
        reuse_if_exists=args.reuse_if_exists,
    )
