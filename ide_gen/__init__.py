#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A set of subroutines used by the IDE-gen based scripts written in Python.

@package ide_gen

For higher level tools like makeprojects, cleanme and
buildme, common subroutines were collected and
placed in this module for reuse.

@mainpage

@htmlinclude README.html

Chapter list
============

Module list
===========

- \ref ide_gen

@var ide_gen.__numversion__
Current version of the library as a numeric tuple

@var ide_gen.__version__
Current version of the library

@var ide_gen.__author__
Author's name

@var ide_gen.__title__
Name of the module

@var ide_gen.__summary__
Summary of the module's use

@var ide_gen.__uri__
Home page

@var ide_gen.__email__
Email address for bug reports

@var ide_gen.__license__
Type of license used for distribution

@var ide_gen.__copyright__
Copyright owner

@var ide_gen.__all__
Items to import on "from ide_gen import *"
"""

from __future__ import absolute_import

import sys

from .hashes import xcode_calcuuid, vs_calcguid
from .string_utils import xcode_quote_string_if_needed

########################################

# Current version of the library as a numeric tuple
__numversion__ = (0, 1, 1)

# Current version of the library
__version__ = ".".join([str(num) for num in __numversion__])

# Author's name
__author__ = "Rebecca Ann Heineman"

# Name of the module
__title__ = "ide_gen"

# Summary of the module's use
__summary__ = "IDE project generator."

# Home page
__uri__ = "http://ide-gen.readthedocs.io"

# Email address for bug reports
__email__ = "becky@burgerbecky.com"

# Type of license used for distribution
__license__ = "MIT License"

# Copyright owner
__copyright__ = "Copyright 2025 Rebecca Ann Heineman"

# Items to import on "from ide_gen import *"
__all__ = [
    "xcode_calcuuid",
    "vs_calcguid",
    "xcode_quote_string_if_needed"
]
