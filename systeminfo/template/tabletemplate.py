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

from template import Template

class TableTemplate(Template):

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
        _property_names = {}
        """
        @type: dict
        @ivar: holds names for each property
        """
        
        def __init__(self, tableRows, names):
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

            self._property_names = names
            tableRows.insert(0, names)
            self.tableData = tableRows

            for key, value in self._property_names.iteritems():
                    self._maxInfo[key] = [len(value)]
                    self._maxInfo[key+'Max'] = len(value)

            for cpunum, info in enumerate(self.tableData):
                    if len(info.keys()) > 0:
                            for key, value in self._property_names.iteritems():
                                if key not in self.tableData[cpunum]:
                                    self.tableData[cpunum][key] = 'N/A'

                                if self.tableData[cpunum][key] is None or self.tableData[cpunum][key] == '':
                                    self.tableData[cpunum][key] = 'N/A'

                                if max(self._maxInfo[key]) < len(self.tableData[cpunum][key]):
                                    self._maxInfo[key+'Max'] = len(self.tableData[cpunum][key])

                                self._maxInfo[key].append(len(str(self.tableData[cpunum][key])))