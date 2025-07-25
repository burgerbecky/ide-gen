#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for ide-gen hashes
Copyright 2013-2025 by Rebecca Ann Heineman becky@burgerbecky.com

It is released under an MIT Open Source license. Please see LICENSE
for license details. Yes, you can use it in a
commercial title without paying anything, just give me a credit.
Please? It's not like I'm asking you for money!

"""

import sys
import unittest
import os
from burger import is_string

# Insert the location of makeprojects at the begining so it's the first
# to be processed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pylint: disable=wrong-import-position
from ide_gen import xcode_calcuuid, vs_calcguid

# List of strings and expected hashes
_XCODE_UUID = (
    ("alsdkldkssd", "13583DA21BC9283A31920CFC"),
    ("", "D41D8CD98F00B204E9800998"),
    ("This is a test of Xcode", "970A101DFCE9A97F852E9D96"),
    ("file/test/slash", "3F0D700E9C3A65FA96D4F052"),
    ("file\\test\\slash", "3F0D700E9C3A65FA96D4F052")
)

# List of strings and expected hashes
_VS_GUID = (
    ("alsdkldkssd", "4162B8B2-B604-3CB2-9818-9DD6B42C9818"),
    ("", "C87EE674-4DDC-3EFE-A74E-DFE25DA5D7B3"),
    ("This is a test of Visual Studio", "3CF36F15-8B58-34EB-8A99-7EA61FA0C4D1"),
    ("file/test/slash", "C60F13FF-317D-39A3-B150-119B5B152049"),
    ("file\\test\\slash", "C60F13FF-317D-39A3-B150-119B5B152049")
)


########################################


class TestHashes(unittest.TestCase):
    """
    Test hashes
    """

########################################

    def test_xcode_hash(self):
        """
        Test to see if cleanme loads build_rules.py.
        """

        for item in _XCODE_UUID:
            before = item[0]
            after = xcode_calcuuid(before)
            self.assertEqual(after, item[1])
            self.assertTrue(is_string(after))

########################################

    def test_vs_hash(self):
        """
        Test to see if cleanme handles CLEANME_GENERIC.
        """

        for item in _VS_GUID:
            before = item[0]
            after = vs_calcguid(before)
            self.assertEqual(after, item[1])
            self.assertTrue(is_string(after))


########################################


if __name__ == "__main__":
    unittest.main()
