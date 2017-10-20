#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  include.py
#
#  Copyright 2017 François Onimus <francois.onimus@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from __future__ import print_function
import re
import os.path
from codecs import open
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

REGEX_KEY_TAG = "tag"
REGEX_KEY_LINES = "lines"

PREFIX = "WARNING - Include-snippets: ignore file: "
FORMAT = ". Examples: lines=3 (line 3 only) | lines=3,5,7 (lines 3, 5 and 7) | lines=3-5 (lines 3 to 5)"

INC_SYNTAX = re.compile(r"{!\s*(.+?)\s*!((\btag\b|\blines\b)=([A-Za-z0-9,_-]+))?\}")
START_TAG = "tag::"
END_TAG = "end::"


class MarkdownInclude(Extension):
    def __init__(self, configs=None, *args, **kwargs):
        super(MarkdownInclude, self).__init__(*args, **kwargs)
        if configs is None:
            configs = {}
        self.config = {
            'base_path': ['.', 'Default location from which to evaluate relative paths for the include statement.'],
            'encoding': ['utf-8', 'Encoding of the files used by the include statement.']
        }
        for key, value in configs.items():
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add(
            'include', IncludePreprocessor(md, self.getConfigs()), '_begin'
        )


class IncludePreprocessor(Preprocessor):
    """
    This provides an "include" function for Markdown, similar to that found in
    LaTeX (also the C pre-processor and Fortran). The syntax is {!filename!},
    which will be replaced by the contents of filename. Any such statements in
    filename will also be replaced. This replacement is done prior to any other
    Markdown processing. All file-names are evaluated relative to the location
    from which Markdown is being called.
    """

    def __init__(self, md, config):
        super(IncludePreprocessor, self).__init__(md)
        self.base_path = config['base_path']
        self.encoding = config['encoding']

    def run(self, lines):
        done = False
        while not done:
            for line in lines:
                loc = lines.index(line)
                m = INC_SYNTAX.search(line)

                if m:
                    filename = m.group(1)
                    filename = os.path.expanduser(filename)
                    if not os.path.isabs(filename):
                        filename = os.path.normpath(
                            os.path.join(self.base_path, filename)
                        )
                    addition = []

                    is_tag = False
                    is_lines = False
                    tag = None
                    wanted_lines = None
                    if m.group(2):
                        key = m.group(3)
                        value = m.group(4)
                        if key == REGEX_KEY_TAG:
                            is_tag = True
                            tag = value
                        elif key == REGEX_KEY_LINES:
                            is_lines = True
                            if ',' in value:
                                temporary = value.split(',')
                                wanted_lines = []
                                for t in temporary:
                                    if t.isdigit():
                                        wanted_lines.append(int(t) - 1)
                                    else:
                                        print(PREFIX + filename + '. Error: not a number : ' + t + FORMAT)
                            elif '-' in value:
                                start_end = value.split('-')
                                if len(start_end) != 2:
                                    print(PREFIX + filename + '. Error: ' + FORMAT)
                                    break
                                start = start_end[0]
                                end = start_end[1]
                                if not start.isdigit():
                                    print(PREFIX + filename + '. Error: not a number: ' + start + FORMAT)
                                elif not end.isdigit():
                                    print(PREFIX + filename + '. Error: not a number: ' + end + FORMAT)
                                else:
                                    wanted_lines = list(range(int(start) - 1, int(end)))
                            elif value.isdigit():
                                wanted_lines = [int(value) - 1]

                    try:
                        with open(filename, 'r', encoding=self.encoding) as input_data:
                            tag_start_found = False
                            tag_end_found = False
                            source = []
                            if is_tag:
                                temp = []
                                for l in input_data:
                                    source.append(strip(l))
                                    if START_TAG + tag in strip(l):
                                        tag_start_found = True
                                        break

                                for l in input_data:
                                    source.append(strip(l))
                                    if tag and END_TAG + tag in strip(l):
                                        tag_end_found = True
                                        break
                                    temp.append(strip(l))

                                if not tag_start_found or not tag_end_found:
                                    prefix = PREFIX + filename + ', could not find '
                                    for t in source:
                                        addition.append(t)
                                    if not tag_start_found:
                                        print(prefix + 'start of tag: ' + tag)
                                    elif not tag_end_found:
                                        print(prefix + 'end of tag: ' + tag)
                                else:
                                    for t in temp:
                                        addition.append(t)
                            elif is_lines:
                                last = wanted_lines[-1]
                                for index, l in enumerate(input_data):
                                    if index > last:
                                        break
                                    if index in wanted_lines:
                                        addition.append(strip(l))

                            else:
                                for l in input_data:
                                    addition.append(strip(l))

                    except Exception as e:
                        print(PREFIX + filename + '. Error: {}'.format(e))
                        lines[loc] = INC_SYNTAX.sub('', line)
                        break

                    lines = lines[:loc] + addition + lines[loc + 1:]
                    break
            else:
                done = True
        return lines


def strip(string):
    return string.replace("\n", "")


def makeExtension(*args, **kwargs):
    return MarkdownInclude(kwargs)
