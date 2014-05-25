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
Module: memory.py

Class: Memory

This class is class for memory asset type

@author: Pavol Ipoth
@license: GPLv3+
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

import dmidecode
import ConfigParser
import re
import sys
import os
import systeminfo.proc.base

class Memory(systeminfo.proc.base.Base):

    asset_info = []
    """
    @type: list
    @ivar: holds info about all memories
    """

    def getData(self, options):
        """
        Method: getData

        Gets all information about all memory items

        @type options: dict
        @param options: passed options
        @rtype void
        @see dmidecode
        """

        # we are getting info from dmidecode module (some info which i see in dmidecode
        # are not present in dict...), and filter out results for memory type (17)
        # assign in key - value pair
        for hwinfo in dmidecode.memory().iteritems():
            if hwinfo[1]['dmi_type'] == 17 and type(hwinfo[1]['data']) == dict:
                tmpinfo = {}
                for iteminfo in hwinfo[1]['data'].iteritems():
                    p = re.compile('\s+')
                    key = p.sub('', iteminfo[0])
                    tmpinfo[key] = str(iteminfo[1])

                tmpinfo['toolindex'] = hwinfo[0]
                tmpinfo['handle'] = hwinfo[0]

                self.asset_info.append(tmpinfo)
