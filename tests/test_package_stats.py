import unittest
import tempfile
import pathlib
from package_stats.content_file import ContentFile


class TestPackStats(unittest.TestCase):
    """This test case tests the entirety of package_stats"""

    def setUp(self) -> None:
        self.architecture = "armel"
        self.mirror_url = "http://ftp.uk.debian.org/debian/dists/stable/main/"

    def test_lists_architectures(self):
        """the application can list the architectures in the provided debian mirror"""
        content_file = ContentFile(self.mirror_url, self.architecture)
        result, _ = content_file.get_content_indices()

        self.assertTrue(
            result is not None,
            "The function returned a None value where a non-empty list was expected.")

        self.assertTrue(isinstance(result, list),
                        "The function failed to return a list")

        self.assertTrue(
            len(result) > 0,
            "An empty list was returned. Either the code is broken, or the url has no Content Indices!")
        result_contains_dicts = all(isinstance(item, dict) for item in result)
        self.assertTrue(result_contains_dicts,
                        "each item in the result should be a dictionary")
        result_contains_keys = all("filename" in item.keys(
        ) and "url" in item.keys() for item in result)
        self.assertTrue(result_contains_keys,
                        "each item in the result should contain a filename and a url value")

    def test_get_content_indice_file_url(self):
        """the application can get the content indice file url given the architecture"""
        content_file = ContentFile(self.mirror_url, self.architecture)
        _, urls = content_file.get_content_indices()

        self.assertIsInstance(
            urls, list, "output of the function was expected to be a list of urls")
        self.assertTrue(urls[0].endswith(
            f"{self.architecture}.gz"), "output url should end with the [ARCHITECTURE].gz")

    def test_downloads_content_file(self):
        """the application can download the right contents file given an architecture
        string"""

        with tempfile.TemporaryDirectory() as temp_directory:
            content_file = ContentFile(
                self.mirror_url, self.architecture, output_dir=temp_directory)
            _, urls = content_file.get_content_indices()
            url = urls[0]
            content_file.download_contents_file(content_file_url=url)
            expected_file = pathlib.Path(
                temp_directory) / f"Contents-{self.architecture}"
            self.assertTrue(expected_file.exists(
            ), "The requested contents indice was not downloaded and unpacked")
            self.assertTrue(
                expected_file.is_file(),
                "The requested contents indice was not downloaded and unpacked to a file, it is a directory")

    def test_gets_package_data_from_contents(self):
        """ The application can get the package data from a contents file"""
        with tempfile.TemporaryDirectory() as temp_directory:
            content_file = ContentFile(
                self.mirror_url, self.architecture, output_dir=temp_directory)
            _, urls = content_file.get_content_indices()
            complete_package_data = {}
            total_keys = 0
            for url in urls:
                contents_file = content_file.download_contents_file(url)
                package_dict = content_file.parse_contents_indice(
                    contents_file)
                self.assertIsInstance(
                    package_dict, dict, "Package metadata should be a dictionary")
                self.assertTrue(len(package_dict.keys()) > 0,
                                "Package list is not empty")
                complete_package_data.update(**package_dict)
                total_keys += len(package_dict)
            self.assertEqual(total_keys, len(complete_package_data),
                             "the two package files were not added together")
