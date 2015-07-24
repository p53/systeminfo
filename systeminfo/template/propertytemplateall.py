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

This class processes template string
It is used for generating string as key value pairs of properties

@author: Pavol Ipoth
@license: GPLv3+
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

import string

class PropertyTemplateAll:

        _template = ''
        
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

        def __init__(self, tableRows, names, tplstring):
            """
            Method: __init__

            Method initializies object

            @type tableRows: list
            @param tableRows: this is array of data
            @type names: list
            @param names: this is array of properties
            @type tplstring: str
            @param tplstring: this is template string
            @rtype: void
            """

            self._property_names = names
            self.tableData = tableRows
            self._template = tplstring

        def __str__(self):
            """
            Method: __str__

            This method is key method in generating output string, in format of key value pairs,
            it calls __getitem__ for each item

            @rtype: str
            @return: returns formatted string for whole template
            """

            length = 0
            output = "[\n"
            
            for index, itemData in enumerate(self.tableData):
                # if there is no value in data, fill with N/A
                for key, data in self._property_names.iteritems():
                        current_key = self._property_names[key]

                        if key not in itemData.keys():
                            itemData[key] = 'N/A'

                        if itemData[key] is None or itemData[key] == '':
                                itemData[key] = 'N/A'

                        if self._maxInfo['propname'] < len(current_key):
                                self._maxInfo['propname'] = len(current_key)

                        if self._maxInfo['propval'] < len(itemData[key]):
                                self._maxInfo['propval'] = len(itemData[key])

                if len(itemData.keys()) > 0:
                     output = output + self._template % self
                    
                if self._iteration != (len(self.tableData) - 1) :
                     output += ",\n"
                     
                self._iteration = self._iteration + 1

            self._iteration = 0
            
            output += "]"
            
            return output

        def __getitem__(self, key):
            """
            Method: __getitem__

            Method formats and generates string for item

            @type key: str
            @param key: this is key from template
            @rtype: str
            @return: returns formatted string for one value of one item from template
            """

            el = key.split("|")
            current_key = ''

            if el[0] in self._property_names.keys():
                current_key = self._property_names[el[0]]
            else:
                current_key = el[0]

            # value column is not formated
            if len(el) == 1:
                    valformated = self.tableData[self._iteration][key]
                    keyformated = current_key
                    return '"' + keyformated + '"' + ':' + '"' + valformated + '"'
            else:
                    valformated = self.tableData[self._iteration][el[0]]
                    keyformated = getattr(string, el[1])(current_key, self._maxInfo['propname'])
                    return '"' + keyformated + '"' + ':' + '"' + valformated + '"'
