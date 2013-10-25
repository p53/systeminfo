import dmidecode
import view.memtpl
import ConfigParser
import template.tabletemplate
import re
import sys
import os

class Memory:
    meminfo = []
    
    def __init__(self):
        
        for hwinfo in dmidecode.memory().iteritems():
            if hwinfo[1]['dmi_type'] == 17 and type(hwinfo[1]['data']) == dict:
                tmpinfo = {}
                for iteminfo in hwinfo[1]['data'].iteritems():
                    p = re.compile('\s+')
                    key = p.sub('', iteminfo[0])
                    tmpinfo[key] = iteminfo[1]
                    
            self.meminfo.append(tmpinfo)
        
    def show(self):
        config = ConfigParser.ConfigParser()
        config.optionxform = str
        abspath = os.path.dirname(sys.argv[0]) + '/settings/lang-en.conf'
        config.read([abspath])
        headers = dict(config.items('Memory'))

        self.meminfo.insert(0, headers)

        print template.tabletemplate.TableTemplate(self.meminfo, view.memtpl.tpl)
        

