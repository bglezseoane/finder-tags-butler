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

from finder_tags_butler.cli_layer import run_parser
from finder_tags_butler.logic_layer import *
from finder_tags_butler.properties import MANIFEST_FILE_NAME


def main():
    # First, run the parser
    opt = run_parser()

    # Calculate paths
    cwd = os.getcwd()
    cwd_manifest = os.path.join(cwd, MANIFEST_FILE_NAME)

    # Interpret the option selected by the user
    if opt == "save_opt":
        save_manifest(cwd, cwd_manifest)
    elif opt == "dump_opt":
        dump_manifest(manifest_path=cwd_manifest, path=cwd, force_overwriting=None)
    elif opt == "soft_dump_opt":
        dump_manifest(manifest_path=cwd_manifest, path=cwd, force_overwriting=False)
    elif opt == "hard_dump_opt":
        dump_manifest(manifest_path=cwd_manifest, path=cwd, force_overwriting=True)
    else:  # If the parser is updated with this if-block, this won't occur
        raise NotImplementedError
