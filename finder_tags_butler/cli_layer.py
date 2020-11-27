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

"""Finder Tags Butler command line interface."""

import argparse

# Style constants
COLOR_BOLD = "\033[1m"
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_CIAN = "\033[96m"
COLOR_RST = "\033[0m"  # Restore

# Predefined messages
MSG_OK = COLOR_GREEN + "[OK]" + COLOR_RST
MSG_ERROR = COLOR_RED + "[ERROR]" + COLOR_RST
MSG_WARNING = COLOR_YELLOW + "[WARNING]" + COLOR_RST


def run_parser() -> str:
    parser = argparse.ArgumentParser(
        description="Finder Tags Butler",
        epilog="Synchronize Mac OS Finder tags between several machines.",
    )
    options = parser.add_mutually_exclusive_group()
    options.add_argument(
        "-s",
        "--save",
        dest="save_opt",
        action="store_true",
        help="Saves the tags of the current working directory to a manifest.",
    )
    options.add_argument(
        "-d",
        "--dump",
        dest="dump_opt",
        action="store_true",
        help="Dumps the tags of the manifest of the current working "
        "directory. If the manifest provides from other machine, "
        "also removes all the tags of the current working "
        "directory and children that are not in the manifest.",
    )
    options.add_argument(
        "-sd",
        "--soft-dump",
        dest="soft_dump_opt",
        action="store_true",
        help="Dumps the tags of the manifest of the current working "
        "directory, but does not remove any tag present in the current "
        "working directory and children.",
    )
    options.add_argument(
        "-hd",
        "--hard-dump",
        dest="hard_dump_opt",
        action="store_true",
        help="Dumps the tags of the manifest of the current working "
        "directory, removing all the tags of the current working "
        "directory and children that are not in the manifest.",
    )

    # Parse
    args = parser.parse_args()

    # Interpret the orders
    if args.save_opt:
        return "save_opt"
    elif args.dump_opt:
        return "dump_opt"
    elif args.soft_dump_opt:
        return "soft_dump_opt"
    elif args.hard_dump_opt:
        return "hard_dump_opt"
