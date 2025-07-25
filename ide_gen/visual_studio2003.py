#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project file generator for Microsoft Visual Studio 2003-2008.

This module contains classes needed to generate project files intended for use
by Microsoft's Visual Studio 2003, 2005 and 2008.
"""

# \package ide_gen.visual_studio2003

from __future__ import absolute_import, print_function, unicode_literals

from burger import is_string

########################################


def convert_file_name(item):
    """ Convert macros from to Visual Studio 2003-2008
    Args:
        item: Filename string
    Returns:
        String with converted macros
    """
    if is_string(item):
        item = item.replace("%(RootDir)%(Directory)", "$(InputDir)")
        item = item.replace("%(FileName)", "$(InputName)")
        item = item.replace("%(Extension)", "$(InputExt)")
        item = item.replace("%(FullPath)", "$(InputPath)")
        item = item.replace("%(Identity)", "$(InputPath)")
    return item

class VS2003Global(Object):
    def __init__(self):
        self.global_sections = []

    def generate(self, line_list, indent):
        return line_list

class VS2003sln(Object):
    def __init__(self, name):
        if not name:
            name = "unnamed"
        self.name = name
        self.project = []
        self.globals = VS2003Global()

    def generate(self):
        """
        Generate the solution file and return a list of strings.

        Returns:
            list of text lines for the Visual Studio 2003 solution file.
        """
        line_list = []

        line_list.append(
            "Microsoft Visual Studio Solution File, Format Version 8.00")
        for project in self.projects:
            project.generate(self, line_list=line_list, indent=0)
        self.globals.generate(self, line_list=line_list, indent=0)
        return line_list
