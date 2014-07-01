# Systeminfo - Simple utility for gathering hardware summary information
# Copyright (C) 2013, 2014  Pavol Ipoth  <pavol.ipoth@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# -*- coding: utf-8 -*-

"""
Module: tabletemplate.py

Class: TableTemplate

This class processes template string
It is used for generating body of table output

@author: Pavol Ipoth
@license: GPLv3+
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

import string

class TableTemplate:

        _template = ''

        _iteration = 0
        """
        @type: int
        @ivar: holds index for iterating over items
        """

        _maxInfo = {}
        """
        @type: dict
        @ivar: holds maximum length for each column
        """

        def __init__(self, tableRows, names, tplstring):
            """
            Method: __init__

            Initializies object, finds maximum width for each table columns

            @type tableRows: list
            @param tableRows: this is list of asset items
            @type names: list
            @param names: this is list of column names
            @type tplstring: str
            @param tplstring: this is template string
            @rtype: void
            """

            self.header = names
            tableRows.insert(0, names)
            self.tableData = tableRows
            self._template = tplstring
            for key, value in self.header.iteritems():
                    self._maxInfo[key] = [len(value)]
                    self._maxInfo[key+'Max'] = len(value)

            for cpunum, info in enumerate(self.tableData):
                    if len(info.keys()) > 0:
                            for key, value in self.header.iteritems():
                                if key not in self.tableData[cpunum]:
                                    self.tableData[cpunum][key] = 'N/A'

                                if self.tableData[cpunum][key] is None or self.tableData[cpunum][key] == '':
                                    self.tableData[cpunum][key] = 'N/A'

                                if max(self._maxInfo[key]) < len(self.tableData[cpunum][key]):
                                    self._maxInfo[key+'Max'] = len(self.tableData[cpunum][key])

                                self._maxInfo[key].append(len(str(self.tableData[cpunum][key])))

            # we are popping out header fields, we need just data for body
            self.tableData.pop(0)

        def __str__(self):
            """
            Method: __str__

            This method is key method in generating output string, just for header items,
            for each items is calling __getitem__ method

            @rtype: str
            @return: returns formatted string for whole template, all items
            """

            length = 0
            output = ""
            for i, v in enumerate(self.tableData):
                    if len(v.keys()) > 0:
                            output = output + self._template % self
                            self._iteration = self._iteration + 1

            self._iteration = 0
            return output

        def __getitem__(self, key):
            """
            Method: __getitem__

            Method formats and generates string for one item

            @type key: str
            @param key: is key of one value of one item
            @rtype: str
            @return: returns formatted string for one value of one item
            """

            el = key.split("|")
            if len(el) == 1:
                    return self.tableData[self._iteration][key]
            else:
                    return getattr(string, el[1])(self.tableData[self._iteration][el[0]], self._maxInfo[el[0]+'Max'])
