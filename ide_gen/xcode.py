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

# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=consider-using-f-string

from __future__ import absolute_import, print_function, unicode_literals

import os
from operator import itemgetter

from burger import is_string, is_number, convert_to_linux_slashes, \
    convert_to_array

from .hashes import xcode_calcuuid
from .string_utils import xcode_determine_source_type
from .xcode_json import JSONEntry, JSONArray, JSONDict, JSONObjects

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
        self.archive_version = JSONEntry("archiveVersion", value="1")
        self.add_item(self.archive_version)

        # Always empty
        self.classes = JSONDict("classes")
        self.add_item(self.classes)

        # Set to the version of XCode being generated for
        self.object_version = JSONEntry(
            "objectVersion", value=str(file_version))
        self.add_item(self.object_version)

        # Create the master object list
        self.objects = JSONObjects("objects")
        self.add_item(self.objects)

        # UUID of the root object
        self.root_object = JSONEntry("rootObject", "Project object", uuid)
        self.add_item(self.root_object)

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
        file_encoding: fileEncoding record
        explicit_file_type: explicitFileType record
        last_known_file_type: lastKnownFileType record
        include_in_index: includeInIndex record
        name_entry: name record
        path: path record
        source_tree: sourceTree record
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

        # Get the file type
        if file_type is None:
            file_type = xcode_determine_source_type(file_name)

        # Get the name without the leading path
        basename = os.path.basename(file_name)

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

        # Create entries in output order

        # UTF-8 encoding
        self.file_encoding = self.add_dict_entry("fileEncoding", "4")

        # Default this off, since lastKnownFileType is the default
        self.explicit_file_type = self.add_dict_entry(
            "explicitFileType", file_type, False)

        self.last_known_file_type = self.add_dict_entry(
            "lastKnownFileType", file_type)

        # Index is only for binaries
        self.include_in_index = self.add_dict_entry(
            "includeInIndex", "0", False)

        self.name_entry = self.add_dict_entry("name", basename)

        self.path = self.add_dict_entry("path", file_name)

        self.source_tree = self.add_dict_entry("sourceTree", "SOURCE_ROOT")

        # Enable / disable entries based on file type

        # Process frameworks first (Special case)
        if file_type.startswith("wrapper.framework"):

            # No file encoding
            self.file_encoding.enabled = False

            # Use the system frameworks folders and the SDKROOT
            self.path.value = "System/Library/Frameworks/" + basename
            self.source_tree.value = "SDKROOT"
            return

        # If not a text file, disable file encoding
        if not file_type.startswith(
                "sourcecode") and not file_type.startswith("text"):
            self.file_encoding.enabled = False

        # Binaries use explict file types
        if file_type.startswith("archive") or file_type.startswith(
                "compiled") or file_type.startswith("wrapper"):
            # Turn on the index, and use explict types
            self.last_known_file_type.enabled = False
            self.explicit_file_type.enabled = True
            self.include_in_index.enabled = True

            # Records for output binary files
            if not file_type.startswith("wrapper"):
                self.name_entry.enabled = False
                self.path.value = basename
                self.source_tree.value = "BUILT_PRODUCTS_DIR"

########################################


class PBXBuildFile(JSONDict):
    """
    Create a PBXBuildFile entry

    Every file that is built needs a record to associate a source file to an
    output file. This record connects the two objects to alert XCode to build
    the input file for the output file.

    Effectively, these are makefile entries to invoke compilation recipes.

    Note:
        The outputfile is only needed for ensuring UUIDs are unique for
        XCode projects where multiple output files are created. There has
        to be unique PBXBuildFile uuid for every build target, even if the
        source file is the same

    Attributes:
        file_reference: PBXFileReference of the file being compiled
        settings: Additional compiler settings applied only to this file
    """

    def __init__(self, input_reference, output_reference, uuid=None):
        """
        Init the PBXBuildFile record.

        Args:
            input_reference: PBXFileReference of source file to compile
            output_reference: PBXFileReference of lib/exe being built.
            uuid: uuid override for this object
        """

        # Sanity checks
        if not isinstance(input_reference, PBXFileReference):
            raise TypeError(
                "parameter \"input_reference\""
                " must be of type PBXFileReference")

        if not isinstance(output_reference, PBXFileReference):
            raise TypeError(
                "parameter \"output_reference\""
                " must be of type PBXFileReference")

        # Make the uuid
        if uuid is None:
            # Use the input and output to generate the default
            # uuid hash
            uuid = xcode_calcuuid(
                "PBXBuildFile" +
                input_reference.file_name +
                output_reference.file_name)

        # File to compile
        basename = os.path.basename(input_reference.file_name)

        # Single file or Framework directory tree?
        ref_type = "Frameworks" \
            if input_reference.file_type.startswith("wrapper.framework") \
            else "Sources"

        # Initial record
        JSONDict.__init__(self, uuid, "{} in {}".format(basename, ref_type),
                          uuid=uuid,
                          isa="PBXBuildFile",
                          flattened=True)

        # PBXFileReference of the file being compiled
        self.file_reference = input_reference

        # Add the uuid of the file reference
        self.file_ref = self.add_dict_entry("fileRef", input_reference.uuid)

        # Add an entry for additional settings
        self.settings = JSONDict("settings", disable_if_empty=True)
        self.add_item(self.settings)

        # Set the source file name as a comment
        self.file_ref.comment = basename

########################################


class PBXGroup(JSONDict):
    """
    PBXGroup record.
    This entry creates all of the groups to display the source files
    in subdirectories for organizing the files' locations.

    Attributes:
        group_list: List of child groups
        file_list: List of child files
        children: Children list
        name_entry: name record
        path: path record
        source_tree: sourceTree record
    """

    def __init__(self, group_name, path, uuid=None):
        """
        Init the PBXGroup.

        Args:
            group_name: Name of this group
            path: Pathname for the group to represent
            uuid: uuid override for this object
        """

        # Create uuid, and handle an empty path
        if uuid is None:
            uuid_path = "<group>" if path is None else path
            uuid = xcode_calcuuid("PBXGroup" + group_name + uuid_path)

        # Init the defaults
        JSONDict.__init__(self, uuid, group_name,
                          uuid=uuid,
                          isa="PBXGroup")

        # No groups are files are part of this upon creation
        self.group_list = []
        self.file_list = []

        # Create the records in order of emission

        # Children groups (Empty for now)
        self.children = JSONArray("children")
        self.add_item(self.children)

        # Add the name
        self.name_entry = self.add_dict_entry(
            "name", group_name)

        # Add the path
        self.path = self.add_dict_entry("path", path)

        # Source tree root path
        value = "SOURCE_ROOT" if path is not None else "<group>"
        self.source_tree = self.add_dict_entry("sourceTree", value)

        # Enable these entries depending if the path exists
        self.name_entry.enabled = path is None or group_name != path
        self.path.enabled = path is not None

    ########################################

    def is_empty(self):
        """
        Return True if there are no entries in this group.

        Returns:
            True if this PBXGroup has no entries.
        """

        return not (self.group_list or self.file_list)

    ########################################

    def add_file(self, file_reference):
        """
        Append a file uuid and name to the end of the list.

        Args:
            file_reference: PBXFileReference item to attach to this group.
        """

        # Sanity check
        if not isinstance(file_reference, PBXFileReference):
            raise TypeError(
                "parameter \"file_reference\" must be of type PBXFileReference")

        # Add a tuple with the UUID and base name
        self.file_list.append(
            (file_reference.uuid, os.path.basename(
                file_reference.file_name)))

    ########################################

    def add_group(self, group):
        """
        Append a group to the end of the list.

        Args:
            group: PBXGroup item to attach to this group.
        """

        # Sanity check
        if not isinstance(group, PBXGroup):
            raise TypeError(
                "parameter \"group\" must be of type PBXGroup")

        # Add a tuple with the UUID and the name of the group
        self.group_list.append((group.uuid, group.name_entry.value))

    ########################################

    def generate(self, line_list, indent=0):
        """
        Write this record to output.

        Args:
            line_list: Line list to append new lines.
            indent: number of tabs to insert (For recursion)
        """

        # This is a fakeout. Create children entries, and add them
        # sorted by file names or group names because the lists are
        # tuples of uuid followed by name.

        self.children.value = []

        # Output groups first, sorted by group name
        for item in sorted(self.group_list, key=itemgetter(1)):
            self.children.add_string_entry(item[0]).comment = item[1]

        # Output files last, sorted by filename
        for item in sorted(self.file_list, key=itemgetter(1)):
            self.children.add_string_entry(item[0]).comment = item[1]

        # Print out the group entries
        return JSONDict.generate(self, line_list, indent)

########################################


class PBXBuildRule(JSONDict):
    """
    Create a PBXBuildRule entry.

    Create a generic build rule so that files with a certain extension
    will have a custom script run, so that it will build non-standard source
    code.

    Attributes:
        compiler_spec: compilerSpec record
        file_patterns: filePatterns record
        file_type: fileType record
        input_files: inputFiles record
        is_editable: isEditable record
        output_files: outputFiles record
        run_once_per_architecture: runOncePerArchitecture record
        script: script record
    """

    def __init__(self, file_pattern=None, file_type=None,
                 output_files=None, script=None, uuid=None):
        """
        Initialize the PBXBuildRule

        Args:
            file_pattern: File pattern to match
            file_type: Xcode internal tool name if known
            output_files: List of output files this will generate
            script: Bash script to execute
            uuid: uuid override
        """

        # If a file pattern is passed, use the XCode command
        # pattern.proxy to use the pattern if not already known
        if file_pattern and not file_type:
            file_type = "pattern.proxy"

        # Set blank if no pattern is used
        if not file_pattern:
            file_pattern = ""

        # Create the UUID if not already supplied
        if uuid is None:
            uuid = xcode_calcuuid(
                "PBXBuildRule" +
                str(file_pattern) +
                str(file_type))

        # Init the parent as a PBXBuildRule
        JSONDict.__init__(self, uuid, "PBXBuildRule",
                          uuid=uuid,
                          isa="PBXBuildRule")

        # Create entries in output order
        # The default rule is a bash/zsh script
        self.compiler_spec = self.add_dict_entry(
            "compilerSpec",
            "com.apple.compilers.proxy.script")

        # Apply to all files that match this pattern
        self.file_patterns = self.add_dict_entry("filePatterns", file_pattern)

        # filePatterns is a wildcard
        self.file_type = self.add_dict_entry("fileType", file_type)

        # Add the input files
        self.input_files = JSONArray("inputFiles")
        self.add_item(self.input_files)
        self.input_files.add_string_entry("${INPUT_FILE_PATH}")

        # This rule can be edited, since it's not a built-in
        self.is_editable = self.add_dict_entry("isEditable", "1")

        # Create the list of output files
        self.output_files = JSONArray("outputFiles")
        self.add_item(self.output_files)

        # Insert the output files
        for item in convert_to_array(output_files):
            # This is the file generated
            self.output_files.add_string_entry(item)

        # Only build once, don't build for each CPU type
        self.run_once_per_architecture = self.add_dict_entry(
            "runOncePerArchitecture", "0")

        # The script to execute (Must end with a CR)
        if script and not script.endswith("\\n"):
            script = script + "\\n"
        self.script = self.add_dict_entry("script", script)

    ########################################

    def generate(self, line_list, indent=0):
        """
        Write this record to output.

        Args:
            line_list: Line list to append new lines.
            indent: number of tabs to insert (For recursion)
        """

        # Some entries are not available in Xcode 3-10

        # pylint: disable=no-member
        file_version = self.get_parent().file_version

        # 52 is XCode 11
        if file_version <= 52:
            self.input_files.enabled = False
            self.run_once_per_architecture.enabled = False

        return JSONDict.generate(self, line_list, indent)

########################################


class PBXFrameworksBuildPhase(JSONDict):
    """
    Each PBXFrameworksBuildPhase entry

    Attributes:
        build_action_mask: Integer mask for enabling operations
        files: JSONArray of PBXBuildFile records
        run_only_for_deployment: runOnlyForDeploymentPostprocessing record
    """

    def __init__(self, file_reference):
        """
        Initialize PBXFrameworksBuildPhase.

        Args:
            file_reference: PBXFileReference record
        """

        # Sanity check
        if not isinstance(file_reference, PBXFileReference):
            raise TypeError(
                "parameter \"file_reference\" must be of type PBXFileReference")

        uuid = xcode_calcuuid(
            "PBXFrameworksBuildPhase" +
            file_reference.file_name)

        JSONDict.__init__(self, uuid, "Frameworks",
                          isa="PBXFrameworksBuildPhase",
                          uuid=uuid)

        self.build_action_mask = self.add_dict_entry(
            "buildActionMask", "2147483647")

        # JSONArray of PBXBuildFile records
        self.files = JSONArray(name="files")
        self.add_item(self.files)

        self.run_only_for_deployment = self.add_dict_entry(
            "runOnlyForDeploymentPostprocessing", "0")

    ########################################

    def add_build_file(self, build_file):
        """
        Add a framework to the files record

        Args:
            build_file: PBXBuildFile record
        """

        # Sanity check
        if not isinstance(build_file, PBXBuildFile):
            raise TypeError(
                "parameter \"build_file\" must be of type PBXBuildFile")

        self.files.add_item(
            JSONEntry(
                build_file.uuid,
                os.path.basename(
                    build_file.file_reference.file_name) +
                " in Frameworks"))
