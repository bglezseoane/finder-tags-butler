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

"""Finder Tags Butler test suite: integration tests for logic layer."""

import os
import random
import shutil
import socket
import string
import tempfile
import unittest
from unittest import TestCase

import yaml

from finder_tags_butler.logic_layer import (
    _get_children_of_path,
    save_manifest,
    dump_manifest,
    _validate_mainifest_file,
)
from finder_tags_butler.logic_tags import (
    add_finder_tag_for_path,
    get_finder_tags_for_path,
    rm_all_finder_tags_for_path,
)
from finder_tags_butler.properties import MANIFEST_FILE_NAME


class IntegrationTestSuiteLogicLayer(TestCase):
    def test_save_and_dump_manifest(self):
        """Test the full process to save and dump a manifest."""
        with tempfile.TemporaryDirectory() as sample_node:
            # Generate random stuff
            _generate_random_folders_tree(sample_node)

            # Select some random files and folders
            children = _get_children_of_path(sample_node)
            tagged_children = children[: (len(children) // 3)]  # Children subset

            # Create a list with a random tag name to each tagged child
            tags = []
            for _ in tagged_children:
                tags.append(
                    "".join(random.choice(string.ascii_letters) for i in range(15))
                )  # Random tag name

            # Tag children
            additional_tag_1 = "Multiple of eleven"
            additional_tag_2 = "Multiple of 11"
            for i in range(0, len(tagged_children)):
                add_finder_tag_for_path(tagged_children[i], tags[i])
                if not i % 11:
                    add_finder_tag_for_path(tagged_children[i], additional_tag_1)
                    add_finder_tag_for_path(tagged_children[i], additional_tag_2)

            # Save the manifest
            manifest_path = os.path.join(sample_node, MANIFEST_FILE_NAME)
            save_manifest(sample_node, manifest_path)

            # Remove all the tags
            for child in tagged_children:
                rm_all_finder_tags_for_path(child)

            # Now dump the saved manifest to restore the previous state
            dump_manifest(manifest_path, sample_node)

            # Check that the machine name is correctly stored
            with open(manifest_path, "r") as infile:
                file_manifest = yaml.load(infile, Loader=yaml.FullLoader)
            self.assertEqual(file_manifest.machine, socket.gethostname())

            # Get current state and check against the previous one
            for i in range(0, len(tagged_children)):
                res_tags = get_finder_tags_for_path(tagged_children[i])
                self.assertTrue(tags[i] in res_tags)
                if not i % 11:
                    self.assertTrue(additional_tag_1 in res_tags)
                    self.assertTrue(additional_tag_2 in res_tags)
                    # Achieve an empty list
                    res_tags.remove(tags[i])
                    res_tags.remove(additional_tag_1)
                    res_tags.remove(additional_tag_2)
                    self.assertFalse(res_tags)
                else:
                    # Achieve an empty list
                    res_tags.remove(tags[i])
                    self.assertFalse(res_tags)

    def test_manifest_files_validation(self):
        with tempfile.TemporaryDirectory() as sample_node:
            # Generate random stuff
            _generate_random_folders_tree(sample_node)

            # Select some random files and folders
            children = _get_children_of_path(sample_node)
            tagged_children = children[: (len(children) // 3)]  # Children subset

            # Create a list with a random tag name to each tagged child
            tags = []
            for _ in tagged_children:
                tags.append(
                    "".join(random.choice(string.ascii_letters) for i in range(15))
                )  # Random tag name

            # Tag children
            additional_tag_1 = "Multiple of eleven"
            additional_tag_2 = "Multiple of 11"
            for i in range(0, len(tagged_children)):
                add_finder_tag_for_path(tagged_children[i], tags[i])
                if not i % 11:
                    add_finder_tag_for_path(tagged_children[i], additional_tag_1)
                    add_finder_tag_for_path(tagged_children[i], additional_tag_2)

            # Save the manifest
            manifest_path = os.path.join(sample_node, MANIFEST_FILE_NAME)
            save_manifest(sample_node, manifest_path)

            # Save several copies of the manifest
            manifest_path_copy1 = f"{manifest_path}.copy1"
            manifest_path_copy2 = f"{manifest_path}.copy2"
            manifest_path_copy3 = f"{manifest_path}.copy3"
            shutil.copy(manifest_path, manifest_path_copy1)
            shutil.copy(manifest_path, manifest_path_copy2)
            shutil.copy(manifest_path, manifest_path_copy3)

            # Check validity of initial manifest
            self.assertTrue(_validate_mainifest_file(manifest_path))

            # Insert random dirty text at the head of the file
            with open(manifest_path_copy1, "w") as f:
                f.seek(0)
                f.write("fñv´´zñvsfvlausvbsvs<dfsdagfasb<cygidsvysGCV<UDS")

            self.assertFalse(_validate_mainifest_file(manifest_path_copy1))

            # Insert incomplete manifest representation
            with open(manifest_path_copy2, "w") as f:
                yaml.dump({"machine": "computer"}, f)

            self.assertFalse(_validate_mainifest_file(manifest_path_copy2))

            # Change name of component
            with open(manifest_path_copy3, "r") as f:
                filedata = f.read()
            filedata = filedata.replace("content", "wine")
            with open(manifest_path_copy3, "w") as f:
                f.write(filedata)

            self.assertFalse(_validate_mainifest_file(manifest_path_copy3))


if __name__ == "__main__":
    unittest.main()


def _generate_random_folders_tree(root_path: str, depth: int = 101) -> None:
    """Help method that generates a big folder tree with random files and
    folders.

    Contents won't be erased, so its recommended to use temporary paths to run
    this method.

    :param root_path: The path where create a Git repository structure and mock
        content.
    :param depth: The depth of the generated sources trees. I.e. more
        volume of random stuff created.
    """
    # Random seed
    r = random.randint(4, depth)

    subdirs = []
    for i in range(0, r // 4):
        subdir = os.path.join(
            root_path, "".join(random.choice(string.ascii_letters) for i in range(35))
        )
        os.mkdir(subdir)
        subdirs.append(subdir)

    for i in range(0, r // 2):
        subdir = random.choice(subdirs)
        if i % 2:
            open(os.path.join(subdir, f"file{i}.txt"), "a").close()
        else:
            subsubdir = os.path.join(subdir, f"subdirectory{i}")
            os.mkdir(subsubdir)
            with open(os.path.join(subsubdir, f"BIG_FILE{i}"), "wb") as f:
                f.write(os.urandom((i + 10) * 1024))
