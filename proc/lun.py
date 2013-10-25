import re
import os
import dbus
from string import Template
import template.tabletemplate
import ConfigParser
import string
import view.luntpl
import glob
import sys

class Lun:
    lunsbypath = {}
    lundesc = {}
    luninfo = []

    def __init__(self):
        self.getLunsByPath()
        self.getLunDesc()

        for disk, info in self.lunsbypath.iteritems():
            diskinfo = {
                            'device': disk,
                            'targetport': info['targetport'],
                            'id': str(self.lundesc[disk]['storage.serial']),
                            'lunid': str(info['lunid']),
                            'model': self.lundesc[disk]['storage.model'],
                            'vendor': self.lundesc[disk]['storage.vendor'],
                            'size': "%.f" % (self.lundesc[disk]['storage.size']),
                            'hwpath': self.lundesc[disk]['hwpath'],
                            'srcport': self.lundesc[disk]['srcport']
                    }

            self.luninfo.append(diskinfo)
            
    def show(self):
        config = ConfigParser.ConfigParser()
        config.optionxform = str
        abspath = os.path.dirname(sys.argv[0]) + '/settings/lang-en.conf'
        config.read([abspath])
        headers = dict(config.items('Lun'))

        self.luninfo.insert(0, headers)

        print template.tabletemplate.TableTemplate(self.luninfo, view.luntpl.tpl)

    def getLunsByPath(self):
        disk_by_path = os.listdir('/dev/disk/by-path')
        fcpat = re.compile('.*-fc-(0x[0-9a-z]+)[:-]((lun-)?(0x)?[0-9a-z]+)$')
        dskpat = re.compile('(sd[a-z]+)')

        for disk in disk_by_path:
            match = fcpat.search(disk)
            if match:
                target_port = match.group(1)
                lun_id = match.group(2)
                target = os.readlink('/dev/disk/by-path' + '/' + match.group(0))
                dskmatch = dskpat.search(target)
                
                if dskmatch:
                    diskdev = dskmatch.group(1)
                    self.lunsbypath[diskdev] = {}
                    self.lunsbypath[diskdev]['targetport'] = target_port
                    self.lunsbypath[diskdev]['lunid'] = lun_id

    def getLunDesc(self):
        system_bus = dbus.SystemBus()
        try:
            hal_mgr_obj = system_bus.get_object('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
            self.getHalDesc()
        except dbus.DBusException:
            self.getUdevDesc()
                
    def getHalDesc(self):
        system_bus = dbus.SystemBus()
        hal_mgr_obj = system_bus.get_object('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
        hal_mgr_iface = dbus.Interface(hal_mgr_obj, 'org.freedesktop.Hal.Manager')
        devs = hal_mgr_iface.GetAllDevices()

        for i in devs:
            dev = system_bus.get_object('org.freedesktop.Hal', i)
            interface = dbus.Interface(dev, dbus_interface='org.freedesktop.Hal.Device')

            if interface.PropertyExists('info.category'):
                category = interface.GetProperty('info.category')
                if category == 'storage':
                    props = interface.GetAllProperties()
                    props['storage.size'] = float(props['storage.size']) / 1000000.0
                    devpat = re.compile('/dev/(sd\w+)')
                    devname = devpat.search(props['block.device'])
                    
                    parentdev = system_bus.get_object('org.freedesktop.Hal', props['info.parent'])
                    parentiface =dbus.Interface(parentdev, dbus_interface='org.freedesktop.Hal.Device')
                    hwpath = parentiface.GetProperty('linux.sysfs_path')
                    hwregex = re.compile('.*?\/([a-zA-Z0-9:.]+)$')
                    hostregex = re.compile('\/([a-zA-Z0-9:.]+)\/host[0-9]+')
                    hwmatch = hwregex.search(hwpath)
                    hostmatch = hostregex.search(hwpath)
                     
                    if hwmatch:
                        props['hwpath'] = hwmatch.group(1)
                     
                    if hostmatch:
                        props['srcport'] = hostmatch.group(1)
                     
                    if devname:
                        self.lundesc[devname.group(1)] = props

                
    def getUdevDesc(self):
        import gudev
        client = gudev.Client(["block"])
        devs = client.query_by_subsystem("block")
        devpat = re.compile('/dev/(sd\w+)')

        for dev in devs:
            devicename = dev.get_property('DEVNAME')
            devtype = dev.get_property('DEVTYPE')
            devpath = dev.get_property('DEVPATH')

            if devtype == 'disk':
                devicematch = devpat.search(devicename)
                if devicematch:
                    devname = devicematch.group(1)

                    hwregex = re.compile('/([0-9:]+)/')
                    hostregex = re.compile('\/([a-zA-Z0-9:.]+)\/host[0-9]+')
                    hwmatch = hwregex.search(devpath)
                    hostmatch = hostregex.search(devpath)

                    self.lundesc[devname] = {}
                    self.lundesc[devname]['storage.vendor'] = dev.get_property('ID_VENDOR')
                    self.lundesc[devname]['storage.model'] = dev.get_property('ID_MODEL')
                    self.lundesc[devname]['storage.size'] = float(dev.get_sysfs_attr('size')) * 512 / 1000000.0
                    self.lundesc[devname]['storage.serial'] = dev.get_property('ID_SERIAL')

                    if hwmatch:
                        self.lundesc[devname]['hwpath'] = hwmatch.group(1)

                    if hostmatch:
                        self.lundesc[devname]['srcport'] = hostmatch.group(1)
