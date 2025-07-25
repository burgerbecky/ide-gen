#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for ide-gen string utilities
Copyright 2013-2025 by Rebecca Ann Heineman becky@burgerbecky.com

It is released under an MIT Open Source license. Please see LICENSE
for license details. Yes, you can use it in a
commercial title without paying anything, just give me a credit.
Please? It's not like I'm asking you for money!

"""

import sys
import unittest
import os

# Insert the location of makeprojects at the begining so it's the first
# to be processed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pylint: disable=wrong-import-position
from ide_gen import xcode_quote_string_if_needed

# List of strings and expected hashes
_XCODE_STRING_QUOTE = (
    ("alsdkldkssd", "alsdkldkssd"),
    ("", "\"\""),
    ("This is a test of Xcode", "\"This is a test of Xcode\""),
    ("file/test/slash", "file/test/slash"),
    ("file\\test\\slash", "\"file\\test\\slash\"")
)


########################################


class TestStringUtils(unittest.TestCase):
    """
    Test String Utilities
    """

########################################

    def test_xcode_quote_string_if_needed(self):
        """
        Test to see if cleanme loads build_rules.py.
        """

        for item in _XCODE_STRING_QUOTE:
            before = item[0]
            after = xcode_quote_string_if_needed(before)
            self.assertEqual(after, item[1])


########################################


if __name__ == "__main__":
    unittest.main()
