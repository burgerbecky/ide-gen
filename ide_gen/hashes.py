#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2022-2025 by Rebecca Ann Heineman becky@burgerbecky.com

# It is released under an MIT Open Source license. Please see LICENSE
# for license details. Yes, you can use it in a
# commercial title without paying anything, just give me a credit.
# Please? It's not like I'm asking you for money!

"""
Sub file for ide_gen.
Subroutines to generate text hashes for IDE objects

@package ide_gen.hashes
This module contains classes needed to generate hashes for IDE projects

"""

from __future__ import absolute_import, print_function, unicode_literals

from hashlib import md5
from uuid import NAMESPACE_DNS, UUID

from burger import convert_to_linux_slashes, convert_to_windows_slashes

########################################


def xcode_calcuuid(input_str):
    """
    Given a string, create a 96 bit unique hash for XCode

    Args:
        input_str: string to hash
    Returns:
        96 bit hash string in upper case.
    """

    temphash = md5(convert_to_linux_slashes(
        input_str).encode("utf-8")).hexdigest()

    # Take the hash string and only use the top 96 bits

    return temphash[0:24].upper()

########################################


def vs_calcguid(input_str):
    """
    Given a string, create a UUID hash for Visual Studio

    Given a project name string, create a 128 bit unique hash for
    Visual Studio.

    Args:
        input_str: Unicode string of the filename to convert into a hash
    Returns:
        A string in the format of CF994A05-58B3-3EF5-8539-E7753D89E84F
    """

    # Generate using md5 with NAMESPACE_DNS as salt
    temp_md5 = md5(
        NAMESPACE_DNS.bytes +
        convert_to_windows_slashes(input_str).encode("utf-8")).digest()
    return str(UUID(bytes=temp_md5[:16], version=3)).upper()
