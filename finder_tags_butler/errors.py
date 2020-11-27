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


"""Finder Tags Butler errors module."""


class CorruptedManifestFileError(Exception):
    def __init__(self, *args):
        if args:
            self.path = args[0]
        else:
            self.path = None

    def __str__(self):
        if self.path:
            return (
                f"Tha manifest file '{self.path}' is corrupted and can "
                f"not be used by this program."
            )
        else:
            return "'CorruptedManifestFileError' has been raised."
