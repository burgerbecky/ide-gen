#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2022-2025 by Rebecca Ann Heineman becky@burgerbecky.com

# It is released under an MIT Open Source license. Please see LICENSE
# for license details. Yes, you can use it in a
# commercial title without paying anything, just give me a credit.
# Please? It's not like I'm asking you for money!

"""
Sub file for ide_gen.
XCode JSON generators

@package ide_gen.xcode_json
This module contains classes needed to generate Xcode JSON objects

"""

# pylint: disable=useless-object-inheritance
# pylint: disable=consider-using-f-string

from __future__ import absolute_import, print_function, unicode_literals


########################################


class JSONShared(object):
    """
    XCode JSON shared variables

    Every JSON entry for XCode derives from this object and has a minimum of a
    name, comment, uuid, default value, and an enabled flag.

    Attributes:
        name: Object's name (Can also be the uuid)
        comment: Optional object's comment field
        uuid: Optional uuid string
        enabled: If False, disable output of this object.
        value: Value (Can be None, integer, string, array, or JSON object)
    """

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments

    def __init__(self, name, comment=None, uuid=None,
                 enabled=True, value=None):
        """
        Initialize the JSONShared entry.

        Args:
            name: Name of this object
            comment: Optional comment
            uuid: uuid hash of the object
            enabled: If False, don't output this object in the generated object.
            value: Optional value
        """

        self.name = name
        self.comment = comment
        self.uuid = uuid
        self.enabled = enabled
        self.value = value

    ########################################

    def add_item(self, item):
        """
        Append an item to the array.
        This is only for JSONDict or JSONDict objects

        Assume the value attribute is an iterable that can be appended
        and perform an append() operation on the attribute with the
        item parameter. If value cannot be appended, an exception is
        thrown.

        Args:
            item: JSONShared based object.
        """

        self.value.append(item)

    ########################################

    def find_item(self, name):
        """
        Find a named JSON item.
        Iterate over the JSON objects and locate one by name. This
        function assumes the value attribute is an iterable of JSON
        objects. An assert will be thrown if the iterable doesn't have
        objects with ``name`` attributes.

        Args:
            name: Name of the item to locate
        Returns:
            Reference to item or None if not found.
        """

        for item in self.value:
            if item.name == name:
                return item

        # The item was not found
        return None

    ########################################

    def get_comment_string(self):
        """
        Return the string to generate for a comment.
        If the JSON object has a comment, return the string surrounded
        by ANSI "C" style quotes with a space prefix.

        Otherwise, return an empty string.

        Example returned string is " /* comment */"

        Returns:
            Empty string, or string with C quotes.
        """

        # Is there a comment?
        if self.comment is None:
            return ""

        # Set the comment string
        return " /* {} */".format(self.comment)
