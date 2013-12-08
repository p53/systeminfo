
__docformat__ = "javadoc"

"""
Module: memory.py

Class: Memory

Copyright 2013 Pavol Ipoth <pavol.ipoth@gmail.com>

This class is class for memory asset type

@author: Pavol Ipoth
"""

import dmidecode
import ConfigParser
import template.tabletemplate
import re
import sys
import os
import proc.base

class Memory(proc.base.Base):
    
    """
        This variable holds info about all memories
        
        @var asset_info list
    """
    asset_info = []
    
    """
        Method: getData
        
        Gets all information about all memory items
        
        @param options dir
        @return void
        @see dmidecode
    """
    def getData(self, options):
        
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

