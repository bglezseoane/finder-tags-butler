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


def run_parser() -> dict:
    """Parse the user input.

    Supported options are:
        - 'save_opt'.
        - 'dump_opt'.
        - 'hard_dump_opt'.
        - 'soft_dump_opt'.

    :return: A dict '{"path": args.path, "option": opt}'.
    """
    parser = argparse.ArgumentParser(
        description="Finder Tags Butler",
        epilog="Synchronize Mac OS Finder tags between several machines.",
    )
    parser.add_argument(
        "path", metavar="PATH", type=str, nargs=1, help="The directory where work...",
    )
    options = parser.add_mutually_exclusive_group(required=True)
    options.add_argument(
        "-s",
        "--save",
        dest="save_opt",
        action="store_true",
        help="Saves the tags of the 'path' directory to a manifest.",
    )
    options.add_argument(
        "-d",
        "--dump",
        dest="dump_opt",
        action="store_true",
        help="Dumps the tags of the manifest of the 'path' "
        "directory. If the manifest provides from other machine, "
        "also removes all the tags of the 'path' "
        "directory and children that are not in the manifest.",
    )
    options.add_argument(
        "-sd",
        "--soft-dump",
        dest="soft_dump_opt",
        action="store_true",
        help="Dumps the tags of the manifest of the 'path' "
        "directory, but does not remove any tag present in the current "
        "working directory and children.",
    )
    options.add_argument(
        "-hd",
        "--hard-dump",
        dest="hard_dump_opt",
        action="store_true",
        help="Dumps the tags of the manifest of the 'path' "
        "directory, removing all the tags of the 'path' "
        "directory and children that are not in the manifest.",
    )

    # Parse
    args = parser.parse_args()

    # Catch the selected option
    if args.save_opt:
        opt = "save_opt"
    elif args.dump_opt:
        opt = "dump_opt"
    elif args.soft_dump_opt:
        opt = "soft_dump_opt"
    elif args.hard_dump_opt:
        opt = "hard_dump_opt"

    # Return the full user input order
    # noinspection PyUnboundLocalVariable
    return {"path": args.path[0], "option": opt}


def print_ok(msg_text: str) -> None:
    """Print the input error with the proper error formatting.

    :param msg_text: The message content text.
    """
    print(f"{MSG_OK}: {msg_text}")


def print_error(error: Exception) -> None:
    """Print the input error with the proper error formatting.

    :param error: The error to print.
    """
    print(f"{MSG_ERROR}: {error.__str__()}")
