#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  include.py
#
#  Copyright 2015 Christopher MacMackin <cmacmackin@gmail.com>
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

#INC_SYNTAX = re.compile(r'\{!\s*(.+?)\s*!\}')
INC_SYNTAX = re.compile(r'\{!\s*(.+?)\s*!(tag=([A-Za-z0-9_-]+))?\}')


class MarkdownInclude(Extension):
    def __init__(self, configs={}):
        self.config = {
            'base_path': ['.', 'Default location from which to evaluate ' \
                'relative paths for the include statement.'],
            'encoding': ['utf-8', 'Encoding of the files used by the include ' \
                'statement.']
        }
        for key, value in configs.items():
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add(
            'include', IncludePreprocessor(md,self.getConfigs()),'_begin'
        )


class IncludePreprocessor(Preprocessor):
    '''
    This provides an "include" function for Markdown, similar to that found in
    LaTeX (also the C pre-processor and Fortran). The syntax is {!filename!},
    which will be replaced by the contents of filename. Any such statements in
    filename will also be replaced. This replacement is done prior to any other
    Markdown processing. All file-names are evaluated relative to the location
    from which Markdown is being called.
    '''
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
                            os.path.join(self.base_path,filename)
                        )
                    addition=[]
                    try:
                        with open(filename, 'r', encoding=self.encoding) as input_data:
                            tag_start_found=False
                            tag_end_found=False
                            source=[]
                            if m.group(2):
                                temp=[]
                                tag=m.group(3)
                                for l in input_data:
                                    source.append(l.strip())
                                    if 'tag::'+tag in l.strip():
                                        tag_start_found=True
                                        break

                                for l in input_data:
                                    source.append(l.strip())
                                    if tag and 'end::'+tag in l.strip():
                                        tag_end_found=True
                                        break
                                    temp.append(l.strip())

                                if not tag_start_found or not tag_end_found:
                                    prefix='WARNING - Include snippets - File: '+filename+', could not find '
                                    for t in source:
                                        addition.append(t)
                                    if not tag_start_found and not tag_end_found:
                                        print(prefix+'tag: '+tag)
                                    elif not tag_start_found:
                                        print(prefix+'start of tag: '+tag)
                                    elif not tag_end_found:
                                        print(prefix+'end of tag: '+tag)
                                else:
                                    for t in temp:
                                        addition.append(t)
                            else:
                                for l in input_data:
                                    addition.append(l.strip())


                    except Exception as e:
                        print('WARNING - Include snippets - Ignoring file: '+filename+'. Error: {}'.format(e))
                        lines[loc] = INC_SYNTAX.sub('',line)
                        break

                    lines = lines[:loc] + addition + lines[loc+1:]
                    break
            else:
                done = True
        return lines


def makeExtension(*args,**kwargs):
    return MarkdownInclude(kwargs)
