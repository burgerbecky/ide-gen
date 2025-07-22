#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A set of subroutines used by the IDE-gen based scripts written in Python.
"""

# pylint: disable=C0302

#
## \package ide_gen
#
# For higher level tools like makeprojects, cleanme and
# buildme, common subroutines were collected and
# placed in this module for reuse.
#

#
## \mainpage
#
# \htmlinclude README.html
#
# Chapter list
# ============
#
#
# Module list
# ===========
#
# - \ref ide_gen
#

from __future__ import absolute_import

import sys

########################################


## Numeric version
__numversion__ = (0, 1, 0)

## Current version of the library
__version__ = '.'.join([str(num) for num in __numversion__])

## Author's name
__author__ = 'Rebecca Ann Heineman'

## Name of the module
__title__ = 'ide_gen'

## Summary of the module's use
__summary__ = 'IDE project generator.'

## Home page
__uri__ = 'http://ide-gen.readthedocs.io'

## Email address for bug reports
__email__ = 'becky@burgerbecky.com'

## Type of license used for distribution
__license__ = 'MIT License'

## Copyright owner
__copyright__ = 'Copyright 2021 Rebecca Ann Heineman'

## Items to import on "from ide_gen import *"
__all__ = [
]
