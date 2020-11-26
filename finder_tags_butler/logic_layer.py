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
from json import JSONEncoder
from typing import Union, List

import yaml

from finder_tags_butler.logic_tags import (
    get_finder_tags_for_path,
    add_finder_tag_for_path,
    rm_all_finder_tags_for_path,
)


class _ContentEntry:
    """Abstraction of a manifest content entry."""

    def __init__(self, path: str, tags: Union[List[str], None]):
        self.path = path
        self.tags = tags

    def __lt__(self, other):
        return self.path.__lt__(other.path)


class _DefaultEncoder(JSONEncoder):
    """To achieve objects JSON serializable."""

    def default(self, o):
        return o.__dict__


class Manifest:
    """Abstraction of a manifest."""

    def __init__(self, content: List[_ContentEntry] = None):
        """To load a manifest file, let 'content' set to 'None'."""
        if content is None:
            content = []
        self.content = content

    def save(self, path: str) -> None:
        """Save the current manifest object to a 'path''s JSON file.

        Warning: the path should be checked before call this function.

        :param path: The param of the output file.
        """
        with open(path, "w") as outfile:
            yaml.dump(self.content, outfile)

    def load(self, path: str) -> None:
        """Read a 'path''s JSON file to the current 'Manifest' object.

        Warning: the path should be checked before call this function.

        :param path: The param of the output file.
        """
        with open(path, "r") as infile:
            self.content = yaml.load(infile, Loader=yaml.FullLoader)


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
        content.append(_ContentEntry(child, tags))

    # Finally, create the manifest and write it to a file
    manifest = Manifest(content)

    # Save the manifest
    manifest.save(manifest_path)


def dump_manifest(manifest_path: str, path: str) -> None:
    """Dump a 'manifest_path''s manifest overwriting tags into the node's
    'path' location.

    Warning: the paths should be checked before call this function.

    :param manifest_path: The path of the input manifest.
    :param path: The path to apply the manifest.
    """
    # Assert the paths are correct and absolutely
    manifest_path = os.path.abspath(os.path.expanduser(manifest_path))
    path = os.path.abspath(os.path.expanduser(path))

    # Read the manifest
    manifest = Manifest()
    manifest.load(manifest_path)

    # Get all the child files and folders recursively
    children = _get_children_of_path(path)

    # First clean all the tags of the node
    for child in children:
        rm_all_finder_tags_for_path(child)

    # Set new tags
    for child in manifest.content:
        for tag in child.tags:
            if os.path.exists(child.path):
                add_finder_tag_for_path(child.path, tag)
            else:
                # print("Error with this tag")  TODO
                continue  # Do not raise exception, the full process must go on


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
