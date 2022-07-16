import gzip
import os
import urllib.request
import pathlib
from collections import defaultdict


class ContentFile:
    def __init__(self, mirror_url: str, arch: str, count: int = 10,
                 output_dir: str = None, reuse_if_exists: bool = False):
        self.mirror_url = mirror_url
        self.arch = arch
        self.count = count
        self.output_dir = output_dir
        self.reuse_if_exists = reuse_if_exists

    def __get_content_file_list(self) -> list:
        """
        Gets a list of content files

        Returns:
            content_types: A list of dictionaries with the following structure
                [{
                    "filename": "Contents-amd64.gz",
                    "url": http://ftp.uk.debian.org/debian/dists/stable/main/Contents-amd64.gz",
                    "arch": "amd64",
                }]
        """
        with urllib.request.urlopen(self.mirror_url) as response:
            raw_html = response.read()
        html = raw_html.decode()

        content_types = []
        extension = ".gz"
        for line in html.split("\r\n"):
            if line.startswith("<a href=\"Contents-"):
                start = line.find("Contents-")
                end = line.find(extension) + len(extension)
                filename = line[start:end]
                url = f"{self.mirror_url}{filename}" if self.mirror_url.endswith(
                    "/") else f"{self.mirror_url}/{filename}"
                start = filename.rfind("-") + 1
                end = filename.rfind(extension)
                arch = filename[start:end]
                content_types.append({
                    "filename": filename,
                    "url": url,
                    "arch": arch
                })
        return content_types

    def get_content_indices(self) -> list:
        """
        Gets the content file list and the URL(s) of the debian content indice file for the given architecture
        If the architecture is None it returns all the content indices.

        Returns:
            content_types: A list of dictionaries with the following structure
                [{
                    "filename": "Contents-amd64.gz",
                    "url": http://ftp.uk.debian.org/debian/dists/stable/main/Contents-amd64.gz",
                    "arch": "amd64",
                }]
            urls: A URL list of the debian content indice
        """
        content_file_list = self.__get_content_file_list()
        urls = [file["url"]
                for file in content_file_list if self.arch == file["arch"]]
        return content_file_list, urls

    def download_contents_file(self, content_file_url: str) -> str:
        """
        Takes a Debian contents indice and extracts the file to a given folder

        Arguments:
            content_file_url: URL of the content indice file

        Returns:
            output_file: path of the content indice file that was downloaded and extracted.
        """
        if self.output_dir is None:
            self.output_dir = os.getcwd()
        basename = os.path.basename(content_file_url)
        file_name = os.path.splitext(basename)[0]

        # gz file path
        output_gz_file = pathlib.Path(self.output_dir) / basename
        # extracted contents indice file path
        output_file = pathlib.Path(self.output_dir) / file_name
        if output_file.exists():
            if self.reuse_if_exists:
                return output_file

        # download the file from a given the url
        with urllib.request.urlopen(content_file_url) as response:
            data = response.read()
        with open(output_gz_file, "wb") as buffer:
            buffer.write(data)

        with gzip.open(output_gz_file, "rb") as buffer:
            data = buffer.read()
        with open(output_file, "wb") as buffer:
            buffer.write(data)

        return output_file

    def parse_contents_indice(self, contents_indice_file: str) -> dict:
        """
        Parses a given contents indice file and returns a dictionary with the
        package names and their associated files

        Arguments:
            contents_indice_file: path of the content indice file to be parsed.

        Returns:
            package_dict: a dictionary containing the packages as keys and
                a list of associated files as the values
        """
        with open(contents_indice_file, encoding="utf8") as lines:
            package_dict = defaultdict(list)
            for line in lines:
                line = line.strip()
                if line == "":
                    continue
                file_name, packages = line.rsplit(" ", maxsplit=1)
                packages = packages.split(",")
                for package in packages:
                    if file_name != "EMPTY_PACKAGE":
                        package_dict[package].append(file_name)
        return package_dict

    @staticmethod
    def get_arhitectures(content_indices):
        """Extracts all architectures from the given content indices."""
        architectures = sorted({item["arch"] for item in content_indices})
        architectures = ", ".join(architectures)
        return architectures
