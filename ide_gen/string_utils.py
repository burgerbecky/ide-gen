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
import os
from burger import convert_to_array

# Valid characters for XCode strings without quoting
_XCODESAFESET = frozenset(string.ascii_letters + string.digits + "_$./")

# XCode file types
_XCODE_FILE_TYPES = [
    ("archive", None),
    ("archive.ar", "a"),
    ("archive.asdictionary", None),
    ("archive.binhex", None),
    ("archive.ear", None),
    ("archive.gzip", ("gz", "gzip")),
    ("archive.jar", "jar"),
    ("archive.macbinary", None),
    ("archive.ppob", None),
    ("archive.rsrc", "rsrc"),
    ("archive.stuffit", "sit"),
    ("archive.tar", "tar"),
    ("archive.war", None),
    ("archive.zip", "zip"),
    ("audio", None),
    ("audio.aiff", "aiff"),
    ("audio.au", "au"),
    ("audio.midi", "midi"),
    ("audio.mp3", "mp3"),
    ("audio.wav", "wav"),
    ("compiled", None),
    ("compiled.cfm", "cfm"),
    ("compiled.javaclass", None),
    ("compiled.mach-o", None),
    ("compiled.mach-o.bundle", None),
    ("compiled.mach-o.corefile", None),
    ("compiled.mach-o.dynlib", "dylib"),
    ("compiled.mach-o.dylinker", None),
    ("compiled.mach-o.executable", None),
    ("compiled.mach-o.fvmlib", None),
    ("compiled.mach-o.objfile", None),
    ("compiled.mach-o.preload", None),
    ("compiled.rcx", "rcx"),
    ("file", None),
    ("file.bplist", None),
    ("file.xib", None),
    ("folder", None),
    ("image", None),
    ("image.bmp", "bmp"),
    ("image.gif", "gif"),
    ("image.icns", "icns"),
    ("image.ico", "ico"),
    ("image.jpeg", ("jpg", "jpeg")),
    ("image.pdf", "pdf"),
    ("image.pict", ("pct", "pict")),
    ("image.png", None),
    ("image.tiff", None),
    ("sourcecode", None),
    ("sourcecode.ada", None),
    ("sourcecode.applescript", None),
    ("sourcecode.asm", None),
    ("sourcecode.asm.asm", ("x86", "x64", "arm", "a64", "ppc")),
    ("sourcecode.asm.llvm", None),
    ("sourcecode.c", None),
    ("sourcecode.c.c", "c"),
    ("sourcecode.c.c.preprocessed", None),
    ("sourcecode.c.h", None),
    ("sourcecode.c.objc", "m"),
    ("sourcecode.c.objc.preprocessed", None),
    ("sourcecode.cpp", None),
    ("sourcecode.cpp.cpp", ("cpp", "cc")),
    ("sourcecode.cpp.cpp.preprocessed", None),
    ("sourcecode.cpp.h", ("h", "hpp")),
    ("sourcecode.cpp.objcpp", "mm"),
    ("sourcecode.cpp.objcpp.preprocessed", None),
    ("sourcecode.dtrace", None),
    ("sourcecode.dylan", None),
    ("sourcecode.exports", None),
    ("sourcecode.fortran", None),
    ("sourcecode.fortran.f77", "f77"),
    ("sourcecode.fortran.f90", "f90"),
    ("sourcecode.glsl", "glsl"),
    ("sourcecode.jam", None),
    ("sourcecode.java", None),
    ("sourcecode.javascript", None),
    ("sourcecode.jobs", None),
    ("sourcecode.lex", None),
    ("sourcecode.make", None),
    ("sourcecode.mig", None),
    ("sourcecode.nasm", None),
    ("sourcecode.nqc", None),
    ("sourcecode.opencl", None),
    ("sourcecode.pascal", None),
    ("sourcecode.rez", None),
    ("sourcecode.scpt", None),
    ("sourcecode.webscript", None),
    ("sourcecode.yacc", None),
    ("text", ("txt", "text")),
    ("text.css", "css"),
    ("text.html", "html"),
    ("text.html.documentation", None),
    ("text.html.other", None),
    ("text.man", None),
    ("text.pbxproject", None),
    ("text.plist", None),
    ("text.plist.d2wmodel", None),
    ("text.plist.ibClassDescription", None),
    ("text.plist.info", None),
    ("text.plist.pbfilespec", None),
    ("text.plist.pblangspec", None),
    ("text.plist.scriptSuite", None),
    ("text.plist.scriptTerminology", None),
    ("text.plist.strings", "strings"),
    ("text.plist.woobjects", None),
    ("text.plist.xclangspec", None),
    ("text.plist.xcspec", None),
    ("text.plist.xcsynspec", None),
    ("text.plist.xctxtmacro", None),
    ("text.plist.xml", None),
    ("text.rtf", "rtf"),
    ("text.script", None),
    ("text.script.csh", "csh"),
    ("text.script.perl", "pl"),
    ("text.script.php", "php"),
    ("text.script.python", "py"),
    ("text.script.ruby", None),
    ("text.script.sh", "sh"),
    ("text.script.worksheet", None),
    ("text.xdef", None),
    ("text.woapi", None),
    ("text.xcconfig", "xcconfig"),
    ("text.xml", "xml"),
    ("video", None),
    ("video.avi", "avi"),
    ("video.mpeg", None),
    ("video.quartz-composer", None),
    ("video.quicktime", None),
    ("wrapper", None),
    ("wrapper.application", "app"),
    ("wrapper.application.webobjects", None),
    ("wrapper.cfbundle", None),
    ("wrapper.dsym", None),
    ("wrapper.framework", "framework"),
    ("wrapper.framework.static", None),
    ("wrapper.htmld", None),
    ("wrapper.installer-mpkg", "mpkg"),
    ("wrapper.installer-pkg", "pkg"),
    ("wrapper.java-classfolder", None),
    ("wrapper.kernel-extension", None),
    ("wrapper.nib", "nib"),
    ("wrapper.pb-project", None),
    ("wrapper.pb-target", None),
    ("wrapper.plug-in", None),
    ("wrapper.rtfd", None),
    ("wrapper.xcclassmodel", None),
    ("wrapper.xcdatamodel", None),
    ("wrapper.xcdatamodeld", None),
    ("wrapper.xcmappingmodel", None),
]


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


########################################

def xcode_determine_source_type(input_path):
    """
    Using a file extension, map to XCode file type.

    Args:
        input_path: Pathname to test
    Returns:
        Xcode filetype string or "sourcecode.c.h"
    """

    # Get the file extension and abort if one doesn't exist
    ext = os.path.splitext(input_path)[1][1:]
    if ext:

        # Case insensitive tests
        ext = ext.lower()

        # Test against all known xcode file types
        for item in _XCODE_FILE_TYPES:
            for entry in convert_to_array(item[1]):

                # Match?
                if entry == ext:
                    return item[0]

    # Default is C header file
    return "sourcecode.c.h"
