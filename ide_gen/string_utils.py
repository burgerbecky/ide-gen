#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2022-2025 by Rebecca Ann Heineman becky@burgerbecky.com

# It is released under an MIT Open Source license. Please see LICENSE
# for license details. Yes, you can use it in a
# commercial title without paying anything, just give me a credit.
# Please? It's not like I'm asking you for money!

"""
Sub file for ide_gen.
Subroutines to handle string fixups for IDE projects

@package ide_gen.string_utils
This module contains classes needed to fixup strings for IDE projects

@var ide_gen.string_utils._XCODESAFESET
Valid characters for XCode strings without quoting

"""

from __future__ import absolute_import, print_function, unicode_literals

import string

# Valid characters for XCode strings without quoting
_XCODESAFESET = frozenset(string.ascii_letters + string.digits + "_$./")

########################################


def xcode_quote_string_if_needed(input_path):
    """
    Quote a string for XCode.

    XCode requires quotes for certain characters. If any illegal character
    exist in the string, the string will be reencoded to a quoted string using
    XCode JSON rules.

    Args:
        input_path: string to encapsulate.
    Returns:
        Original input string if XCode can accept it or properly quoted
    """

    # If there are any illegal characters, break
    for item in input_path:
        if item not in _XCODESAFESET:
            break
    else:
        # No illegal characters were found in the string

        # Empty string?
        if not input_path:
            return "\"\""

        # Return the string without changes
        return input_path

    # Quote the escaped string and escape existing quotes
    return "\"{}\"".format(input_path.replace("\"", "\\\""))
