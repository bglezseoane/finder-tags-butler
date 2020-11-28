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

"""Business logic layer."""

import os
import platform
from typing import Union, List

import yaml

from finder_tags_butler import properties
from finder_tags_butler.errors import CorruptedManifestFileError
from finder_tags_butler.logic_tags import (
    get_finder_tags_for_path,
    add_finder_tag_for_path,
    rm_all_finder_tags_for_path,
)


class TagAssociation:
    """Abstraction of a manifest content entry."""

    def __init__(self, path: str, tags: Union[List[str], None]):
        self.path = path
        self.tags = tags

    def __lt__(self, other):
        return self.path.__lt__(other.path)


class Manifest:
    """Abstraction of a manifest."""

    def __init__(self, content: List[TagAssociation] = None):
        """To load a manifest file, let 'content' set to 'None'."""
        if content is None:
            content = []
        self.content = content
        self.machine = platform.node()

    def save(self, path: str) -> None:
        """Save the current manifest object to a 'path''s YAML file.

        Warning: the path should be checked before call this function.

        :param path: The param of the output file.
        """
        with open(path, "w") as outfile:
            outfile.writelines(properties.MANIFEST_HEAD_COMMENT)
            yaml.dump(self, outfile)

    def load(self, path: str) -> None:
        """Read a 'path''s YAML file to the current 'Manifest' object.

        Warning: the path should be checked before call this function.

        :param path: The param of the output file.
        """
        with open(path, "r") as infile:
            file_manifest = yaml.load(infile, Loader=yaml.FullLoader)
            self.content = file_manifest.content
            self.machine = file_manifest.machine


def save_manifest(path: str, manifest_path: str,) -> None:
    """Save a manifest of the given 'path' into the given 'manifest_path'.

    Warning: the paths should be checked before call this function.

    :param path: The path to explore.
    :param manifest_path: The path of the output manifest (it would be
        overriding).
    """
    # Assert the paths are correct and absolutely
    path = os.path.abspath(os.path.expanduser(path))
    manifest_path = os.path.abspath(os.path.expanduser(manifest_path))

    # Get all the child files and folders recursively
    children = _get_children_of_path(path)

    # Prepare the content entries after explore the child elements
    content = []
    for child in children:
        tags = get_finder_tags_for_path(child)
        if not tags == []:
            content.append(TagAssociation(child, tags))

    # Finally, create the manifest and write it to a file
    manifest = Manifest(content)

    # Save the manifest
    manifest.save(manifest_path)


def dump_manifest(
    manifest_path: str, path: str, force_overwriting: Union[bool, None] = False
) -> [Exception]:
    """Dump a 'manifest_path''s manifest writing tags into the node's 'path'
    location.

    By default, if the manifest provides from another machine, the tags present
    in the target node but not in the manifest will be removed. If the manifest
    provides from the same machine, these tags will be preserved and a warning
    will be presented. Using the 'force_overwriting' param this behaviour can be
    forced.

    Warning: the paths should be checked before call this function.

    :param manifest_path: The path of the input manifest.
    :param path: The path to apply the manifest.
    :param force_overwriting: Passing this param as 'True', the tags of the
        target node will be always totally erased before dumping the
        manifest. Passing as 'False', they won't be removed never.
        Letting as 'None', they will be removed if the manifest
        provides from other machine.
    :return: A list of errors of the tags that have not been correctly
        processed.
    :raise: CorruptedManifestFileError, if the manifest file is corrupted.
    """
    # Assert the paths are correct and absolutely
    manifest_path = os.path.abspath(os.path.expanduser(manifest_path))
    path = os.path.abspath(os.path.expanduser(path))

    # Read the manifest
    if not _validate_mainifest_file(manifest_path):  # First check integrity
        raise CorruptedManifestFileError(manifest_path)
    manifest = Manifest()
    manifest.load(manifest_path)

    # Get all the child files and folders recursively
    children = _get_children_of_path(path)

    # First clean all the tags of the node, if it apply
    if force_overwriting is True or (
        platform.node() != manifest.machine and force_overwriting is not False
    ):
        for child in children:
            rm_all_finder_tags_for_path(child)

    # Set new tags
    tagging_errors = []
    try:
        for child in manifest.content:
            for tag in child.tags:
                if os.path.exists(child.path):
                    add_finder_tag_for_path(child.path, tag)
                else:
                    tagging_errors.append(FileNotFoundError(child.path))
                    continue  # Do not raise exception, the full process must go on
    except AttributeError:
        raise CorruptedManifestFileError(manifest_path)

    return tagging_errors


def _get_children_of_path(path: str) -> [str]:
    """Return all the children files and folders recursively.

    Discard hidden files and folders.

    :param path: The path of the node directory to explore.
    :return: A list with the children files and folders paths.
    """
    children = [path]
    for root, directories, files in os.walk(path):
        # Disable hidden contents
        directories[:] = [d for d in directories if not d.startswith(".")]
        files[:] = [d for d in files if not d.startswith(".")]

        for directory in directories:
            children.append(os.path.join(root, directory))
        for file in files:
            children.append(os.path.join(root, file))

    return children


# noinspection PyStatementEffect
def _validate_mainifest_file(manifest_path: str) -> bool:
    """Check the integrity of a manifest file.

    :param manifest_path: The path of the manifest to validate
    :return: True or false of the manifest is valid or not, respectively.
    """
    try:
        manifest = Manifest()
        manifest.load(manifest_path)

        # Check access to all the stuff
        manifest.machine
        manifest.content
        for child in manifest.content:
            child.path
            child.tags
    except AttributeError:
        return False

    return True
