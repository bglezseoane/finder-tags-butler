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

import sys

from finder_tags_butler.cli_layer import run_parser, print_error, print_ok
from finder_tags_butler.logic_layer import *
from finder_tags_butler.properties import MANIFEST_FILE_NAME


def main():
    # First, run the parser
    opt, path = run_parser()

    # Calculate paths
    if not os.path.isdir(path):
        order_error_printing_and_exit(NotADirectoryError(path))
    manifest_path = os.path.join(path, MANIFEST_FILE_NAME)

    # Interpret the option selected by the user
    if opt == "save_opt":
        save_manifest(path=path, manifest_path=manifest_path)
        # If the process finish well...
        order_ok_printing_without_exit(f"The manifest of {path} has been " f"saved. 💾")
    else:
        # Check manifest existence
        if not os.path.isfile(manifest_path):
            order_error_printing_and_exit(FileNotFoundError(manifest_path))

        # Define the text to print on success
        ok_msg_text = f"The manifest of {path} has been dumped. 🏷"

        if opt == "dump_opt":
            dump_manifest(
                manifest_path=manifest_path, path=path, force_overwriting=None
            )
            # If the process finish well...
            order_ok_printing_without_exit(ok_msg_text)

        elif opt == "soft_dump_opt":
            dump_manifest(
                manifest_path=manifest_path, path=path, force_overwriting=False
            )
            # If the process finish well...
            order_ok_printing_without_exit(ok_msg_text)
        elif opt == "hard_dump_opt":
            dump_manifest(
                manifest_path=manifest_path, path=path, force_overwriting=True
            )
            # If the process finish well...
            order_ok_printing_without_exit(ok_msg_text)
        else:  # If the parser is updated with this if-block, this won't occur
            raise NotImplementedError


def order_ok_printing_without_exit(msg_text: str) -> None:
    """:param msg_text: The message text to print."""
    print_ok(msg_text)
    sys.exit(0)


def order_error_printing_without_exit(error: Exception) -> None:
    """:param error: The error to print."""
    print_error(error)


def order_error_printing_and_exit(error: Exception) -> None:
    """:param error: The error to print."""
    print_error(error)
    sys.exit(1)
