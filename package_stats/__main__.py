"""This module enables usage such as
python -m packagestats

This is needed for standard behaviour compliance
with packages such as pip and other builtins.
"""

from .package_stats import cli_main


if __name__ == "__main__":
    cli_main()
