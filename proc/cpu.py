"""
Module: cpu.py

Class: Cpu

Class for getting data for cpus

@author: Pavol Ipoth
@license: GPL
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

import io.file
import re
from string import Template
import template.tabletemplate
import ConfigParser
import string
import os
import sys
import proc.base

class Cpu(proc.base.Base):
    
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
            
            lines = io.file.readFile('/proc/cpuinfo')
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
