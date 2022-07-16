# Debian Package Statistics

## Instructions

Debian uses *deb packages to deploy and upgrade software. The packages
are stored in repositories and each repository contains the so called "Contents
index". The format of that file is well described here
https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices

A python command line tool that takes the architecture (amd64, arm64, mips etc.) 
as an argument and downloads the compressed Contents file associated with it 
from a Debian mirror. The program parses the file and output the statistics 
of the top X packages(DEFAULT 10) that have the most files associated with them.
An example output:

./package_statistics.py amd64

1. <package name 1>         <number of files>
2. <package name 2>         <number of files>
......
10. <package name 10>         <number of files>

---

## Application Installation (optional)

If desired, the application can be installed with the following command:

```bash
python3 setup.py install
```

*Note: The installation is not necessary to run the application*.

---
## Usage

### With Installation

Once `packagestats` is installed, it can be run in one of two ways.

```packagestats --help```

Or:

```python -m packagestats --help```

### Without Installation

`packagestats` can also be run without installation. The method below can be followed:

Either modify permissions to make it executable and use a version of python3 to run it:

```bash
chmod +x package_statistics.py
./package_statistics.py --help
```

Or, the python command directly can run the tool.

```bash
python package_statistics.py
```
---

## `packagestats` CLI

Command line tool has a help feature that shows all the operations that can be done.

```
$ python package_statistics.py --help
usage: package_statistics.py [-h] [-m MIRROR_URL] [-c COUNT] [-a] [-o OUTPUT_DIR] [-r] arch

A tool that shows the package statistics by parsing a Contents Index (source - https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices) from a        
debian mirror, taking into account the system architecture given.

positional arguments:

options:
  -h, --help            show this help message and exit
  -m MIRROR_URL, --mirror_url MIRROR_URL
                        Mirror URL where content file will be pulled DEFAULT http://ftp.uk.debian.org/debian/dists/stable/main/
  -c COUNT, --count COUNT
                        Number of packages to list. Use -1 to list all. DEFAULT 10
  -a, --ascending       Sort package statistics list by number of files in ascending order. DEFAULT False
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        A directory to store downloaded content file.DEFAULT <current-directory>
  -r, --reuse-if-exists
                        Reuses a content file if it has been downloaded previously and exists in the output directory.
```
---

## Examples

### Getting `amd64` Statistics

```
$ packagestats amd64

1               devel/piglit                                            51784
2               science/esys-particle                                   18015
3               libdevel/libboost1.74-dev                               14333
4               math/acl2-books                                         12668
5               golang/golang-1.15-src                                  9015
6               libdevel/liboce-modeling-dev                            7457
7               net/zoneminder                                          7002
8               libdevel/paraview-dev                                   6178
9               kernel/linux-headers-5.10.0-16-amd64                    6150
10              kernel/linux-headers-5.10.0-13-amd64                    6149
```

### Getting the top 15 packages

```bash
$ packagestats -c 15 amd64
No.             Package Name                                            File Count
1               devel/piglit                                            51784
2               science/esys-particle                                   18015
3               libdevel/libboost1.74-dev                               14333
4               math/acl2-books                                         12668
5               golang/golang-1.15-src                                  9015
6               libdevel/liboce-modeling-dev                            7457
7               net/zoneminder                                          7002
8               libdevel/paraview-dev                                   6178
9               kernel/linux-headers-5.10.0-16-amd64                    6150
10              kernel/linux-headers-5.10.0-13-amd64                    6149
11              kernel/linux-headers-5.10.0-16-rt-amd64                 6144
12              kernel/linux-headers-5.10.0-13-rt-amd64                 6143
13              localization/locales-all                                5956
14              math/coq-theories                                       5588
15              utils/pcp-testsuite                                     4704
```

### Saving Downloaded Files to `/usr`

```
$ packagestats -o /usr amd64
No.             Package Name                                            File Count
1               devel/piglit                                            51784
2               science/esys-particle                                   18015
3               libdevel/libboost1.74-dev                               14333
4               math/acl2-books                                         12668
5               golang/golang-1.15-src                                  9015
6               libdevel/liboce-modeling-dev                            7457
7               net/zoneminder                                          7002
8               libdevel/paraview-dev                                   6178
9               kernel/linux-headers-5.10.0-16-amd64                    6150
10              kernel/linux-headers-5.10.0-13-amd64                    6149
```
With this command, all files are downloaded to the `/usr` directory.

---

### Reusing Downloaded Files

If you want to use previously downloaded content files, the `-r` flag can be used.

```
$ packagestats -r amd64
```

---
### Attempting to Enter an Invalid Architecture
If the user enters an invalid architecture name, the following error will be raised.

```
$ packagestats hakan
Traceback (most recent call last):
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\Scripts\packagestats-script.py", line 33, in <module>
    sys.exit(load_entry_point('canonical-hakanbogan-packagestats==1.0', 'console_scripts', 'packagestats')())
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\lib\site-packages\canonical_hakanbogan_packagestats-1.0-py3.10.egg\package_stats\package_stats.py", line 102, in cli_main
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\lib\site-packages\canonical_hakanbogan_packagestats-1.0-py3.10.egg\package_stats\package_stats.py", line 40, in main
package_stats.exceptions.ContentIndiceForArchitectureNotFound: hakan was not found in the given repository. Available architectures are: all, amd64, arm64, armel, armhf, i386, mips64el, mipsel, ppc64el, s390x, source
```
---

## Tests

The core functions of `packagestats` have tests.

*Note: An internet connection is required for the tests to run*.

```
$ python setup.py test
running test
running egg_info
creating hb_packagestats.egg-info
writing hb_packagestats.egg-info\PKG-INFO
writing dependency_links to hb_packagestats.egg-info\dependency_links.txt
writing entry points to hb_packagestats.egg-info\entry_points.txt
writing top-level names to hb_packagestats.egg-info\top_level.txt
writing manifest file 'hb_packagestats.egg-info\SOURCES.txt'
reading manifest file 'hb_packagestats.egg-info\SOURCES.txt'
writing manifest file 'hb_packagestats.egg-info\SOURCES.txt'
running build_ext
test_downloads_content_file (tests.test_package_stats.TestPackStats)
the application can download the right contents file given an architecture ... ok
test_get_content_indice_file_url (tests.test_package_stats.TestPackStats)
the application can get the content index file url given the architecture ... ok
test_gets_package_data_from_contents (tests.test_package_stats.TestPackStats)
the application can get the package data from a contents file ... ok
test_lists_architectures (tests.test_package_stats.TestPackStats)
the application can list the architectures in the provided debian mirror ... ok

----------------------------------------------------------------------
Ran 4 tests in 11.113s

OK
```