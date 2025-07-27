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

@var ide_gen.xcode_json.TABS
Default tab format for XCode

@var ide_gen.xcode_json.OBJECT_ORDER
Names of Xcode objects in the order they are output
"""

# pylint: disable=useless-object-inheritance
# pylint: disable=consider-using-f-string

from __future__ import absolute_import, print_function, unicode_literals

from operator import attrgetter

from .string_utils import xcode_quote_string_if_needed

########################################

# Default tab format for XCode
TABS = "\t"

# This is the order of XCode chunks that match the way
# that XCode outputs them.
OBJECT_ORDER = (
    "PBXAggregateTarget",
    "PBXBuildFile",
    "PBXBuildRule",
    "PBXContainerItemProxy",
    "PBXCopyFilesBuildPhase",
    "PBXFileReference",
    "PBXFrameworksBuildPhase",
    "PBXGroup",
    "PBXNativeTarget",
    "PBXProject",
    "PBXReferenceProxy",
    "PBXResourcesBuildPhase",
    "PBXShellScriptBuildPhase",
    "PBXSourcesBuildPhase",
    "PBXTargetDependency",
    "XCBuildConfiguration",
    "XCConfigurationList"
)

########################################


class JSONShared(object):
    """
    XCode JSON shared variables

    Every JSON entry for XCode derives from this object and has a minimum of a
    name, comment, uuid, default value, and an enabled flag.

    Attributes:
        name: Object's name (Can also be the uuid)
        comment: Optional object's comment field
        value: Value (Can be None, integer, string, array, or JSON object)
        uuid: Optional uuid string
        enabled: If False, disable output of this object.
        parent: Reference to the parent object

    """

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments

    def __init__(self, name, comment=None, value=None, uuid=None,
                 enabled=True):
        """
        Initialize the JSONShared entry.

        Args:
            name: Name of this object
            comment: Optional comment
            value: Optional value
            uuid: uuid hash of the object
            enabled: If False, don't output this object in the generated object.
        """

        self.name = name
        self.comment = comment
        self.value = value
        self.uuid = uuid
        self.enabled = enabled
        self.parent = None

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

        # Mark this object as the item's parent
        item.parent = self

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

    ########################################

    def get_parent(self):
        """
        Traverse the objects until the parent is found.

        Returns:
            Reference to the parent object
        """

        # Assume this object is the parent
        parent = self

        # Traverse the linked list
        head = parent.parent

        # Was the head found?
        while head is not None:

            # Move up the list
            parent = head
            head = parent.parent

        # Return the parent
        return parent


########################################


class JSONEntry(JSONShared):
    """
    XCode JSON single line entry.
    Each JSON entry for XCode consists of the name followed by an optional
    comment, and an optional value
    """

    # pylint: disable=too-many-arguments

    def __init__(self, name, comment=None, value=None,
                 enabled=True):
        """
        Initialize the JSONEntry.

        Args:
            name: Name of this object
            comment: Optional comment
            value: Optional value
            enabled: If False, don't output this object in the generated object.
        """

        # Init the shared variables
        JSONShared.__init__(
            self, name, comment, value,
            enabled=enabled)

    ########################################

    def generate(self, line_list, indent=0):
        """
        Generate the text lines for this JSON element.

        Args:
            line_list: list object to have text lines appended to
            indent: Integer number of tabs to insert (For recursion)
        """

        # Don't output if disabled
        if not self.enabled:
            return 0

        # Determine the indentation
        tabs = TABS * indent

        # Set the comment string, if any
        comment = self.get_comment_string()

        # Get the value string if any
        if self.value is None:

            # Generate just the value with a comma
            line_list.append(
                "{}{}{},".format(
                    tabs,
                    xcode_quote_string_if_needed(self.name),
                    comment))
        else:
            # Generate the JSON assignment line
            line_list.append(
                "{}{} = {}{};".format(
                    tabs,
                    xcode_quote_string_if_needed(self.name),
                    xcode_quote_string_if_needed(self.value),
                    comment))
        return 0

########################################


class JSONArray(JSONShared):
    """
    XCode JSON array.

    Each JSON entry for XCode consists of the name followed by an optional
    comment, and an optional value.

    This JSON object handles data that can be output in the form of an array.
    If fold_array is set to True, single entry arrays are output as a single
    entry without encapsulating parenthesis.

    Attributes:
        disable_if_empty: True if output is disabled if the list is empty
        fold_array: True if one entry array is output as JSONEntry
    """

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments

    def __init__(self, name, comment=None, value=None,
                 enabled=True, disable_if_empty=False, fold_array=False):
        """
        Initialize the entry.

        Args:
            name: Name of this object
            comment: Optional comment
            value: List of default values
            enabled: If False, don't output this object in the generated object.
            disable_if_empty: If True, don't output if no items in the list.
            fold_array: True if the array should be an entry if only one element
        """

        # Arrays require an iterable. Convert None to an
        # empty array to allow generation
        if value is None:
            value = []

        # Init shared variables
        JSONShared.__init__(
            self, name, comment, value,
            enabled=enabled)

        # If the array is empty, don't print
        self.disable_if_empty = disable_if_empty

        # Default array folding
        self.fold_array = fold_array

    ########################################

    def add_string_entry(self, name):
        """
        Create a new JSONEntry record and add to the array.
        Take the string passed in and append it to the end of the array.

        The JSONEntry will have it's name set to the input string. All other
        attributes are set to defaults.

        Args:
            name: String to append to the array
        Returns:
            JSONEntry created that was added
        """

        # Create a JSONEntry so it's stored as just a name
        new_entry = JSONEntry(name)

        # Append to the array
        self.add_item(new_entry)

        # Return the original item in case the caller wants to
        # perform additional actions on it.
        return new_entry

    ########################################

    def generate(self, line_list, indent=0):
        """
        Generate the text lines for this JSON element.

        Note:
            This can generate multiple lines of text when outputting
            a multi entry array.

        Args:
            line_list: list object to have text lines appended to
            indent: number of tabs to insert (For recursion)
        """

        # Is this object disabled?
        if not self.enabled:
            return 0

        # Disable if there are no values?
        if self.disable_if_empty and not self.value:
            return 0

        # Determine the indentation
        tabs = TABS * indent

        # Get the optional comment
        comment = self.get_comment_string()

        # If there is only one entry, and array folding is enabled,
        # only output a single item, not an array
        if self.fold_array and len(self.value) == 1:

            # Output the assignment value
            line_list.append("{}{}{} = {};".format(
                tabs, self.name, comment,
                xcode_quote_string_if_needed(
                    self.value[0].name)))

        else:
            # Generate the array opening
            line_list.append("{}{}{} = (".format(tabs, self.name, comment))

            # Sub entries are indented
            indent = indent + 1

            # Generate the array
            for item in self.value:
                item.generate(line_list, indent)

            # Generate the array closing
            line_list.append("{});".format(tabs))
        return 0

########################################


class JSONDict(JSONShared):
    """
    XCode JSON dictionary

    Each JSON entry for XCode consists of the name followed by an optional
    comment, and an optional value.

    The entries are encapsulated with curly brackets.

    Attributes:
        disable_if_empty: True if output is disabled if the list is empty
        isa: "Is a" name
        flattened: If True, flatten the child objects
    """

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments

    def __init__(self, name, comment=None, value=None, uuid=None,
                 enabled=True, disable_if_empty=False, isa=None,
                 flattened=False):
        """
        Initialize the entry.

        Args:
            name: Name of this object
            comment: Optional comment
            value: List of default values
            uuid: uuid hash of the object
            enabled: If False, don't output this object in the generated object.
            disable_if_empty: If True, don't output if no items in the list.
            isa: "Is a" type of dictionary object
            flattened: If True, flatten the child objects
        """

        # UUID has to be a string
        if uuid is None:
            uuid = ""

        # Value must be an iterable array
        if value is None:
            value = []

        # Init the shared values
        JSONShared.__init__(
            self, name, comment, value, uuid, enabled)

        # Disable if True and empty
        self.disable_if_empty = disable_if_empty

        # "Is a" class type name
        self.isa = isa

        # Default flattened state
        self.flattened = flattened

        # If there is an ISA entry, make it the first value
        if isa is not None:
            self.add_dict_entry("isa", isa)

    ########################################

    def add_dict_entry(self, name, value=None, enabled=True):
        """
        Create a new JSONEntry record and add to the dictionary
        Take the key value pair and append it to the dictionary.

        Create a JSONEntry with name as the key and value as the value.

        Args:
            name: String for the JSONEntry name
            value: String to use as the value for the entry
            enabled: Is this enabled by default?
        Returns:
            JSONEntry created that was added
        """

        # Create the key/value assignment
        new_entry = JSONEntry(name, value=value, enabled=enabled)

        # Add to the array
        self.add_item(new_entry)

        # Return the value
        return new_entry

    ########################################

    def generate(self, line_list, indent=0):
        """
        Generate the text lines for this JSON element.

        Note:
            This can generate multiple lines of text.

        Args:
            line_list: list object to have text lines appended to
            indent: number of tabs to insert (For recursion)
        """

        # If disabled, exit
        if not self.enabled:
            return 0

        # Disable if there are no values?
        if self.disable_if_empty and not self.value:
            return 0

        # Determine the indentation
        tabs = TABS * indent

        # Get the optional comment"
        comment = self.get_comment_string()

        # Generate the dictionary opening
        line_list.append("{}{}{} = {{".format(tabs, self.name, comment))

        # Generate the dictionary
        indent = indent + 1
        for item in self.value:
            item.generate(line_list, indent)

        # Generate the dictionary closing
        line_list.append("{}}};".format(tabs))
        return 0

########################################


class JSONObjects(JSONDict):
    """
    XCode JSON master object list object.

    Xcode has a master object record called ``objects`` which displays a
    special comment before emitting each sub record. This class implements
    this special case.

    Each record has a prefix and suffix comment, denoting what records are
    being output.

    Note:
        This is always named ``objects``
    """

    def __init__(self, name, uuid=None, enabled=True):
        """
        Initialize the entry.

        Args:
            name: Name of this object
            uuid: uuid hash of the object
            enabled: If False, don't output this object in the generated object.
        """

        JSONDict.__init__(self, name, uuid=uuid, enabled=enabled)

    ########################################

    def get_entries(self, isa):
        """
        Return a list of items that match the isa name.

        Args:
            isa: isa name string.
        Returns:
            List of entires found, can be an empty list.
        """

        # Return a list of items that match the attribute isa
        return [i for i in self.value if i.isa == isa]

    ########################################

    def generate(self, line_list, indent=0):
        """
        Generate the text lines for this JSON element.
        The objects are generated in OBJECT_ORDER order.

        Note:
            This can generate multiple lines of text.

        Args:
            line_list: list object to have text lines appended to
            indent: number of tabs to insert (For recursion)
        """

        # Is this object enabled?
        if not self.enabled:
            return 0

        # Determine the indentation
        tabs = TABS * indent

        # Generate the dictionary opening
        line_list.append("{}{}{} = {{".format(
            tabs, self.name, self.get_comment_string()))

        # Indent all future entries
        indent = indent + 1

        # Output the objects in "isa" order for XCode
        for object_group in OBJECT_ORDER:

            # Find all entries by this name
            item_list = [i for i in self.value if i.isa == object_group]

            # Any items in this group?
            if item_list:

                # Sort by uuid
                item_list = sorted(item_list, key=attrgetter("uuid"))

                # Using the name of the class, output the array of data items
                line_list.append("")
                line_list.append("/* Begin {} section */".format(object_group))

                for item in item_list:

                    # Because Apple hates me. Check if a record needs to be
                    # flattened instead of putting the data on individual lines,
                    # because, just because.
                    # This is used for filename records

                    if getattr(item, "flattened", None):
                        # Generate the lines in this fake entry
                        temp_list = []

                        # Create the text
                        item.generate(temp_list, 0)

                        # Flatten it and strip the tabs
                        temp = " ".join(temp_list).replace(TABS, "")

                        # Remove this space to match the output of XCode
                        temp = temp.replace(" isa", "isa")

                        # Insert the flattened line with extra indentation
                        line_list.append(tabs + TABS + temp)
                        continue

                    # Output the item as is with extra indentation
                    item.generate(line_list, indent)

                line_list.append("/* End {} section */".format(object_group))

        # Close the dictionary and exit
        line_list.append("{}}};".format(tabs))
        return 0
