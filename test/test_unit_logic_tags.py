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

"""Finder Tags Butler test suite: unit tests for tags logic"""

import tempfile
import unittest
from unittest import TestCase

from finder_tags_butler.logic_tags import (
    add_finder_tag_for_path,
    get_finder_tags_for_path,
    rm_all_finder_tags_for_path,
    rm_finder_tag_for_path,
)


class UnitTestSuiteLogicTags(TestCase):
    def test_set_and_get_tag_on_file(self):
        """Test get and set Finder tags.

        This version uses a file.
        """
        with tempfile.NamedTemporaryFile() as f:
            sample_file_path = f.name
            manual_tag = "5w&sfdbdb!$·!!Y&%"
            add_finder_tag_for_path(sample_file_path, manual_tag)
            res_tags = get_finder_tags_for_path(sample_file_path)[0]
            self.assertEqual(manual_tag, res_tags)

    def test_set_and_get_tag_on_dir(self):
        """Test get and set Finder tags.

        This version uses a directory.
        """
        with tempfile.TemporaryDirectory() as sample_folder:
            manual_tag = "Comprobación"
            add_finder_tag_for_path(sample_folder, manual_tag)
            res_tags = get_finder_tags_for_path(sample_folder)[0]
            self.assertEqual(manual_tag, res_tags)

    def test_set_and_get_tags_on_dir(self):
        """Test get and set Finder tags."""
        with tempfile.TemporaryDirectory() as sample_folder:
            manual_tag1 = "Sample tag 1"
            manual_tag2 = "Sample tag 2"
            manual_tag3 = "Sample tag 3"
            add_finder_tag_for_path(
                sample_folder, manual_tag1,
            )
            add_finder_tag_for_path(
                sample_folder, manual_tag2,
            )
            add_finder_tag_for_path(
                sample_folder, manual_tag3,
            )

            res_tags = get_finder_tags_for_path(sample_folder)

            self.assertTrue(manual_tag1 in res_tags)
            self.assertTrue(manual_tag2 in res_tags)
            self.assertTrue(manual_tag3 in res_tags)

    def test_remove_tag_on_dir(self):
        """Test remove a Finder tag."""
        with tempfile.TemporaryDirectory() as sample_folder:
            manual_tag1 = "Sample tag 1"
            manual_tag2 = "Sample tag 2"
            manual_tag3 = "Sample tag 3"
            add_finder_tag_for_path(
                sample_folder, manual_tag1,
            )
            add_finder_tag_for_path(
                sample_folder, manual_tag2,
            )
            add_finder_tag_for_path(
                sample_folder, manual_tag3,
            )

            # Remove
            rm_finder_tag_for_path(sample_folder, manual_tag1)

            res_tags = get_finder_tags_for_path(sample_folder)

            self.assertTrue(manual_tag2 in res_tags)
            self.assertTrue(manual_tag3 in res_tags)

    def test_remove_all_tags_on_dir(self):
        """Test remove all Finder tags."""
        with tempfile.TemporaryDirectory() as sample_folder:
            manual_tag1 = "Sample tag 1"
            manual_tag2 = "Sample tag 2"
            manual_tag3 = "Sample tag 3"
            add_finder_tag_for_path(
                sample_folder, manual_tag1,
            )
            add_finder_tag_for_path(
                sample_folder, manual_tag2,
            )
            add_finder_tag_for_path(
                sample_folder, manual_tag3,
            )

            # Remove
            rm_all_finder_tags_for_path(sample_folder)

            res_tags = get_finder_tags_for_path(sample_folder)

            self.assertEqual(res_tags, [])


if __name__ == "__main__":
    unittest.main()
