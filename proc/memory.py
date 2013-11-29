import dmidecode
import ConfigParser
import template.tabletemplate
import re
import sys
import os
import proc.base

class Memory(proc.base.Base):
    asset_info = []
    
    def getData(self, options):
        
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

