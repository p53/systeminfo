import dmidecode
import ConfigParser
import template.propertytemplate
import template.voidtemplate
import re
import sys
import os
import platform
import io
import proc.base

class System(proc.base.Base):

    asset_info = [{}]
    
    template_header_type = 'VoidTemplate'
    template_body_type = 'PropertyTemplate'

    def getData(self):

        for hwinfo in dmidecode.system().iteritems():
            if hwinfo[1]['dmi_type'] == 1 and type(hwinfo[1]['data']) == dict:
                for iteminfo in hwinfo[1]['data'].iteritems():
                    tmpinfo = {}
                    p = re.compile('\s+')
                    key = p.sub('', iteminfo[0])
                    self.asset_info[0]['System' + key] = str(iteminfo[1])

        for hwinfo in dmidecode.chassis().iteritems():
            if hwinfo[1]['dmi_type'] == 3 and type(hwinfo[1]['data']) == dict:
                for iteminfo in hwinfo[1]['data'].iteritems():
                    tmpinfo = {}
                    p = re.compile('\s+')
                    key = p.sub('', iteminfo[0])
                    self.asset_info[0]['Chassis' + key] = str(iteminfo[1])

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
        
        self.asset_info[0]['OSCoreCount']  = str(core_count)
        self.asset_info[0]['OSCoreEnabled']  = str(core_enabled_count)
        self.asset_info[0]['OSThreadCount']  = str(thread_count)
        self.asset_info[0]['OSPhyscpuCount']  = str(phys_cpu_count)
        load = os.getloadavg()
        self.asset_info[0]['load']  = str(load[0]) + ' ' + str(load[1]) + ' ' + str(load[2])
        self.asset_info[0]['machinetype']  = platform.machine()
        self.asset_info[0]['nodename']  = platform.node()
        self.asset_info[0]['osrelease']  = platform.release()
        self.asset_info[0]['osname']  = platform.system()
        self.asset_info[0]['osversion']  = platform.version()
        
        try:
            distinfo = platform.dist()
        except AttributeError:
            distinfo = platform.linux_distribution()
            
        self.asset_info[0]['distname']  = distinfo[0]
        self.asset_info[0]['distver']  = distinfo[1]
        self.asset_info[0]['distid']  = distinfo[2]
        self.asset_info[0]['toolindex'] = self.asset_info[0]['SystemSerialNumber']
        
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
                                self.asset_info[0]['Memory' + key] = str(value)
