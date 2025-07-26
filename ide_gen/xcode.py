#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2022-2025 by Rebecca Ann Heineman becky@burgerbecky.com

# It is released under an MIT Open Source license. Please see LICENSE
# for license details. Yes, you can use it in a
# commercial title without paying anything, just give me a credit.
# Please? It's not like I'm asking you for money!

"""
Sub file for ide_gen.
XCode generator

@package ide_gen.xcode
This module contains classes needed to generate Xcode files

"""

from __future__ import absolute_import, print_function, unicode_literals

import os

from burger import is_string, is_number, convert_to_linux_slashes

from .hashes import xcode_calcuuid
from .string_utils import xcode_determine_source_type
from .xcode_json import JSONEntry, JSONDict, JSONObjects

########################################


class XCProject(JSONDict):
    """
    Root object for an XCode IDE project file

    Created with the name of the project and the version code

    Attributes:
        file_version: XCode file version
        objects: Dict of objects that comprise the Xcode project
        rootobject: JSONEntry that points to the root object
    """

    def __init__(self, name, file_version, uuid=None):
        """
        Init the project generator.

        Args:
            name: Project solution to generate from.
            file_version: XCode project file version
            uuid: uuid override for the project
        """

        # Sanity checks
        if not is_number(file_version):
            raise TypeError(
                "parameter \"file_version\" must be numeric type")

        # If a UUID was not supplied, calculate one
        if not is_string(uuid):
            uuid = xcode_calcuuid("PBXProjectRoot" + name + str(file_version))

        # Init the solution
        JSONDict.__init__(self, name, uuid=uuid)

        # Save the file version
        self.file_version = file_version

        # Archive version is always first and set to 1
        self.add_item(JSONEntry("archiveVersion", value="1"))

        # Always empty
        self.add_item(JSONDict("classes"))

        # Set to the version of XCode being generated for
        self.add_item(JSONEntry("objectVersion", value=str(file_version)))

        # Create the master object list
        objects = JSONObjects("objects")
        self.objects = objects
        self.add_item(objects)

        # UUID of the root object
        rootobject = JSONEntry("rootObject", "Project object", uuid)
        self.rootobject = rootobject
        self.add_item(rootobject)

    ########################################

    def generate(self, line_list, indent=0):
        """
        Generate an entire XCode project file

        Args:
            line_list: Line list to append new lines.
            indent: number of tabs to insert (For recursion)
        Returns:
            Non-zero on error.
        """

        # Write the XCode header for charset
        line_list.append("// !$*UTF8*$!")

        # Open brace for beginning
        line_list.append("{")

        # Increase indentatiopn
        indent = indent + 1

        # Dump everything in the project in the order they
        # were added
        for item in self.value:
            item.generate(line_list, indent)

        # Close up the project file
        line_list.append("}")
        return 0


########################################


class PBXFileReference(JSONDict):
    """
    A PBXFileReference entry.

    For each and every file managed by an XCode project, a PBXFileReference
    object will exist to reference it. Other sections of XCode will use the
    UUID of this object to act upon the file referenced by this object.

    The UUID is used for both PBXGroup for file hierachical display and
    PBXBuildFile if the file needs to be built with a compiler.

    Attributes:
        file_name: Filename
        file_type: Xcode filetype
    """

    def __init__(self, file_name, uuid=None, file_type=None):
        """
        Initialize the PBXFileReference object.

        Args:
            source_file: core.SourceFile record
            ide: IDETypes of the ide being built for.
        """

        # XCode is hosted by MacOSX, so use linux slashes
        file_name = convert_to_linux_slashes(file_name)

        # Generate the UUID if needed
        if uuid is None:
            uuid = xcode_calcuuid("PBXFileReference" + file_name)

        # Get the name without the leading path
        basename = os.path.basename(file_name)

        # Get the file type
        if file_type is None:
            file_type = xcode_determine_source_type(file_name)

        # Set up the values. The name of this object is the UUID
        # Also, this record is output "flattened"
        JSONDict.__init__(self, uuid, basename,
                          uuid=uuid,
                          isa="PBXFileReference",
                          flattened=True)

        # Store the full pathname
        self.file_name = file_name

        # Store the XCode filetype
        self.file_type = file_type

        # Process frameworks first (Special case)
        if file_type.startswith("wrapper.framework"):
            self.add_dict_entry("lastKnownFileType", file_type)
            self.add_dict_entry("name", basename)
            self.add_dict_entry("path", "System/Library/Frameworks/" + basename)
            self.add_dict_entry("sourceTree", "SDKROOT")
            return

        # If it's a text file, set encoding to UTF-8
        if file_type.startswith("sourcecode") or file_type.startswith("text"):
            self.add_dict_entry("fileEncoding", "4")

        # Binaries use explict file types
        if file_type.startswith("archive") or file_type.startswith(
                "compiled") or file_type.startswith("wrapper"):
            self.add_dict_entry("explicitFileType", file_type)

            # Never add to the index
            self.add_dict_entry("includeInIndex", "0")

        else:
            # Other files use this entry for the file type
            self.add_dict_entry("lastKnownFileType", file_type)

        # Records for source files
        if not file_type.startswith("archive") and not file_type.startswith(
                "compiled"):
            self.add_dict_entry("name", basename)
            self.add_dict_entry("path", file_name)
            self.add_dict_entry("sourceTree", "SOURCE_ROOT")
            return

        # Records for output binary files
        self.add_dict_entry("path", basename)
        self.add_dict_entry("sourceTree", "BUILT_PRODUCTS_DIR")
