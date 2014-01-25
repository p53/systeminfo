"""
Module: memory.py

Class: Memory

This class is class for memory asset type

@author: Pavol Ipoth
@license: GPL
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

