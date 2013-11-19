import dmidecode
import ConfigParser
import template.propertytemplate
import re
import sys
import os
import platform
import io

class System:
    asset_info = {
                    'load': {'propname': 'load'},
                    'machinetype': {'propname': 'machinetype'},
                    'nodename': {'propname': 'nodename'},
                    'osrelease': {'propname': 'osrelease'},
                    'osname': {'propname': 'osname'},
                    'osversion': {'propname': 'osversion'},
                    'distname': {'propname': 'distname'},
                    'distver': {'propname': 'distver'},
                    'distid': {'propname': 'distid'},
                    'OSCoreCount': {'propname': 'OSCoreCount'},
                    'OSCoreEnabled': {'propname': 'OSCoreEnabled'},
                    'OSThreadCount': {'propname': 'OSThreadCount'},
                    'OSPhyscpuCount': {'propname': 'OSPhyscpuCount'}
    }

    def __init__(self):

        for hwinfo in dmidecode.system().iteritems():
            if hwinfo[1]['dmi_type'] == 1 and type(hwinfo[1]['data']) == dict:
                for iteminfo in hwinfo[1]['data'].iteritems():
                    tmpinfo = {}
                    p = re.compile('\s+')
                    key = p.sub('', iteminfo[0])
                    tmpinfo['propname'] = 'System' + key
                    tmpinfo['propval'] = str(iteminfo[1])
                    self.asset_info['System' + key] = tmpinfo

        for hwinfo in dmidecode.chassis().iteritems():
            if hwinfo[1]['dmi_type'] == 3 and type(hwinfo[1]['data']) == dict:
                for iteminfo in hwinfo[1]['data'].iteritems():
                    tmpinfo = {}
                    p = re.compile('\s+')
                    key = p.sub('', iteminfo[0])
                    tmpinfo['propname'] = 'Chassis' + key
                    tmpinfo['propval'] = str(iteminfo[1])
                    self.asset_info['Chassis' + key] = tmpinfo

        core_count = 0
        core_enabled_count = 0
        thread_count = 0
        phys_cpu_count = 0
                
        for hwinfo in dmidecode.processor().iteritems():
            if hwinfo[1]['dmi_type'] == 4 and type(hwinfo[1]['data']) == dict:
                phys_cpu_count += 1
                for iteminfo in hwinfo[1]['data'].iteritems():
                    p = re.compile('\s+')
                    key = p.sub('', iteminfo[0])
                    if key == 'CoreCount':
                        core_count += iteminfo[1]
                    elif key == 'CoreEnabled':
                        core_enabled_count += iteminfo[1]
                    elif key == 'ThreadCount':
                        thread_count += iteminfo[1]
        
        self.getMemInfo()
        
        self.asset_info['OSCoreCount']['propval'] = str(core_count)
        self.asset_info['OSCoreEnabled']['propval'] = str(core_enabled_count)
        self.asset_info['OSThreadCount']['propval'] = str(thread_count)
        self.asset_info['OSPhyscpuCount']['propval'] = str(phys_cpu_count)
        load = os.getloadavg()
        self.asset_info['load']['propval'] = str(load[0]) + ' ' + str(load[1]) + ' ' + str(load[2])
        self.asset_info['machinetype']['propval'] = platform.machine()
        self.asset_info['nodename']['propval'] = platform.node()
        self.asset_info['osrelease']['propval'] = platform.release()
        self.asset_info['osname']['propval'] = platform.system()
        self.asset_info['osversion']['propval'] = platform.version()
        
        try:
            distinfo = platform.dist()
        except AttributeError:
            distinfo = platform.linux_distribution()
            
        self.asset_info['distname']['propval'] = distinfo[0]
        self.asset_info['distver']['propval'] = distinfo[1]
        self.asset_info['distid']['propval'] = distinfo[2]

    def getMemInfo(self):
                lines = io.file.readFile('/proc/meminfo')
                for line in lines:
                        m = re.search('(.*?)\s*:\s*(.*)', line)
                        if m:
                                tmpinfo = {}
                                key = m.group(1)
                                value = m.group(2)
                                p = re.compile('\s+')
                                optim = p.sub('', key)
                                tmpinfo['propname'] = 'Memory' + key
                                tmpinfo['propval'] = str(value)
                                self.asset_info['Memory' + key] = tmpinfo

    def show(self, options):
                config = ConfigParser.ConfigParser()
                config.optionxform = str
                abspath = os.path.dirname(sys.argv[0]) + '/settings/lang-en.conf'
                config.read([abspath])
                property_names = dict(config.items(self.__class__.__name__))

                for key, hash in self.asset_info.iteritems():
                        if 'propname' in hash.keys() > 0 and key in property_names.keys():
                                self.asset_info[key]['propname'] = property_names[key]

                templ_module = self.__class__.__name__.lower() + 'tpl' + options['outlength']
                templ_vars = __import__('view.' + templ_module, globals(), locals(),['tpl'])
                print template.propertytemplate.PropertyTemplate(self.asset_info, templ_vars.tpl)
