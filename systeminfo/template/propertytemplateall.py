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
Module: propertytemplateall.py

Class: PropertyTemplateAll

This class generates output for several types
of output formats, which are based on key:value principle
uses jinja2 templates

@author: Pavol Ipoth
@license: GPLv3+
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

from template import Template

class PropertyTemplateAll(Template):
        
        _iteration = 0
        """
        @type: int
        @ivar: holds index for iterating over items
        """
        
        _maxInfo = {'propname': 0, 'propval': 0 }
        """
        @type: dict
        @ivar: holds maximum length for key column
        """

        _property_names = {}
        """
        @type: dict
        @ivar: holds names for each property
        """

        def __init__(self, tableRows, names):
            """
            Method: __init__

            Method initializies object

            @type tableRows: list
            @param tableRows: this is array of data
            @type names: list
            @param names: this is array of properties
            @rtype: void
            """

            self._property_names = names
            self.tableData = tableRows
            
            for index, itemData in enumerate(self.tableData):
                # if there is no value in data, fill with N/A
                for key, data in self._property_names.iteritems():
                        current_key = data

                        if key not in itemData.keys():
                            itemData[key] = 'N/A'

                        if itemData[key] is None or itemData[key] == '':
                                itemData[key] = 'N/A'

                        if self._maxInfo['propname'] < len(current_key):
                                self._maxInfo['propname'] = len(current_key)

                        if self._maxInfo['propval'] < len(itemData[key]):
                                self._maxInfo['propval'] = len(itemData[key])

