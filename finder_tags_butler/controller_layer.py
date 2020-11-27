# -*- coding: utf-8 -*-

###########################################################
# Finder Tags Butler
#
# Synchronize Mac OS Finder tags between several machines
#
# Copyright 2020 Borja González Seoane
#
# Contact: garaje@glezseoane.es
###########################################################

"""Finder Tags Butler core controller module."""

from finder_tags_butler.cli_layer import run_parser, raise_error_printing
from finder_tags_butler.logic_layer import *
from finder_tags_butler.properties import MANIFEST_FILE_NAME


def main():
    # First, run the parser
    opt, path = run_parser()

    # Calculate paths
    if not os.path.isdir(path):
        raise_error_printing(NotADirectoryError(path))
    manifest_path = os.path.join(path, MANIFEST_FILE_NAME)

    # Interpret the option selected by the user
    if opt == "save_opt":
        save_manifest(path, manifest_path)
    else:
        # Check manifest existence
        if not os.path.isfile(manifest_path):
            raise_error_printing(FileNotFoundError(manifest_path))

        if opt == "dump_opt":
            dump_manifest(
                manifest_path=manifest_path, path=path, force_overwriting=None
            )
        elif opt == "soft_dump_opt":
            dump_manifest(
                manifest_path=manifest_path, path=path, force_overwriting=False
            )
        elif opt == "hard_dump_opt":
            dump_manifest(
                manifest_path=manifest_path, path=path, force_overwriting=True
            )
        else:  # If the parser is updated with this if-block, this won't occur
            raise NotImplementedError


def order_error_printing_without_exit(error: Exception) -> None:
    pass
