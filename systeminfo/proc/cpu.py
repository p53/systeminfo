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
Module: cpu.py

Class: Cpu

Class for getting data for cpus

@author: Pavol Ipoth
@license: GPLv3+
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

import systeminfo.io.file
import re
import ConfigParser
import string
import os
import sys
import systeminfo.proc.base

class Cpu(systeminfo.proc.base.Base):

        asset_info = []
        """
        @type: list
        @ivar: holds asset info
        """

        def getData(self, options):
            """
            Method: getData

            Gathers info about cpu

            @type options: dict
            @param options: passed options
            @rtype: void
            """

            lines = systeminfo.io.file.readFile('/proc/cpuinfo')
            index = 0
            self.asset_info.append({})

            # processors are separated by blank lines, properties
            # are printed as property some white spaces colon white spaces
            # value, so we are dividing info by regexes, each processor
            # is new item in array
            for line in lines:

                    m = re.search('(.*?)\s*:\s*(.*)', line)
                    if m:
                            key = m.group(1)
                            value = m.group(2)
                            p = re.compile('\s+')
                            optim = p.sub('', key)
                            self.asset_info[index][optim] = value

                            if optim == 'processor':
                                self.asset_info[index]['toolindex'] = value

                    if re.match('^\n$', line):
                            self.asset_info.append({})
                            index = index + 1

            self.asset_info.pop()
