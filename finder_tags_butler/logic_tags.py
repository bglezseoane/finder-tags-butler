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

"""Tags functions.

This file simply closures some functions to manage Finder tags.
"""

import mac_tag


def get_finder_tags_for_path(path: str) -> [dict]:
    """Returns the Finder tags for a given file or folder.

    :param path: The path of the file of folder to examine.
    :raise FileNotFoundError: If the path does not points to anything reachable.
    :return: A list of tags as a dict with their titles and colors names.
    """
    try:
        tags_dict = mac_tag.get(path)
        tags = []
        """Access in a unnatural way due to some conflicts with complicated 
        paths... It is known that the dict will only contain one value"""
        for e in tags_dict:
            tags.extend(tags_dict[e])
        return tags
    except FileNotFoundError:
        raise FileNotFoundError(path)


def add_finder_tag_for_path(path: str, tag: str) -> None:
    """Set a Finder tag for a given file or folder.

    :param path: The path of the file of folder to edit.
    :param tag: The tag name to set.
    """
    if tag:
        mac_tag.add(tag, path)
    else:
        raise ValueError("Null tags are not valid")


def rm_finder_tag_for_path(path: str, tag: str) -> None:
    """Remove a Finder tag for a given file or folder.

    :param path: The path of the file of folder to edit.
    :param tag: The tag name to remove.
    """
    mac_tag.remove(tag, path)


def rm_all_finder_tags_for_path(path: str) -> None:
    """Remove all existent Finder tags for a given file or folder.

    :param path: The path of the file of folder to edit.
    """
    tags = get_finder_tags_for_path(path)
    for tag in tags:
        mac_tag.remove(tag, path)
