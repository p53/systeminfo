
__docformat__ = "javadoc"

"""
Module: cpu.py

Class: Cpu

Copyright 2013 Pavol Ipoth <pavol.ipoth@gmail.com>

Class for getting data for cpus

@author: Pavol Ipoth
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
    
        """
            Variable holds asset info
            
            @var asset_info list
        """
        asset_info = []
        
        """
            Method: getData
            
            Gathers info about cpu
            
            @param options dict
            @return void
        """
        def getData(self, options):
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
