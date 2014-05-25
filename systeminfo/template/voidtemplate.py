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
Module: voidtemplate.py

Class: VoidTemplate

This class is just void template, returns empty string

@author: Pavol Ipoth
@license: GPLv3+
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

import string

class VoidTemplate:

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

            Method is just void method
            """
            pass

        def __str__(self):
            """
            Method: __str__

            This method is key method is not implemented as name of class suggests
            it is just void class

            @rtype: str
            @return: returns empty string
            """
            return ''
