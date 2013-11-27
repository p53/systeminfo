import io.file
import os
import re
import string
import template.tabletemplate
import ConfigParser
import dbus
import proc.pci
import sys
import proc.base

class Fcms(proc.base.Base):
    asset_info = []

    def getData(self):
        system_bus = dbus.SystemBus()
        try:
            import gudev
            self.getUdevDevs()
        except ImportError:
            hal_mgr_obj = system_bus.get_object('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
            self.getHalDevs()

    def getUdevDevs(self):
        import gudev
        client = gudev.Client(["fc_host"])
        devs = client.query_by_subsystem("fc_host")
        pciinfo = proc.pci.Pci()
        pciinfo.getData()
        
        for dev in devs:
                props = {}
                parentdev = dev.get_parent()
                grandparent = parentdev.get_parent()
                vendorhex = grandparent.get_sysfs_attr('vendor')
                vendorhex = string.replace(vendorhex, '0x', '')
                hostregex = re.compile('\/([a-zA-Z0-9:.]+)\/host[0-9]+')
                hostmatch = hostregex.search(dev.get_sysfs_path())
                                    
                if hostmatch:
                    props['pcicard'] = hostmatch.group(1)
                                        
                props['pci.vendor'] = pciinfo.pciids['vendors'][vendorhex]
                props['linux.sysfs_path'] = dev.get_sysfs_path()
                props['nodename'] = dev.get_sysfs_attr('node_name')
                props['portname'] = dev.get_sysfs_attr('port_name')
                props['portstate'] = dev.get_sysfs_attr('port_state')
                props['porttype'] = dev.get_sysfs_attr('port_type')
                props['speed'] = dev.get_sysfs_attr('speed')
                
                props['toolindex'] = props['pcicard']
                
                self.asset_info.append(props)

    def getHalDevs(self):
        system_bus = dbus.SystemBus()
        hal_mgr_obj = system_bus.get_object('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
        hal_mgr_iface = dbus.Interface(hal_mgr_obj, 'org.freedesktop.Hal.Manager')
        devs = hal_mgr_iface.GetAllDevices()
        
        for i in devs:
            dev = system_bus.get_object('org.freedesktop.Hal', i)
            interface = dbus.Interface(dev, dbus_interface='org.freedesktop.Hal.Device')
            try:
                classNum = interface.GetProperty('pci.device_class')
                subclassNum = interface.GetProperty('pci.device_subclass')
                
                if classNum == 12 and subclassNum == 4:
                    props = interface.GetAllProperties()
                    pcipath = os.listdir(props['linux.sysfs_path'])
                    
                    for path in pcipath:
                        pattern = re.compile('host[0-9]+')
                        mpath = pattern.search(path)
                        
                        if mpath:
                            hostdir = props['linux.sysfs_path'] + '/' + mpath.group(0)
                            hostpath = os.listdir(hostdir)
                            
                            for hostp in hostpath:
                                pattern = re.compile('fc_host.*')    
                                hostpp = pattern.search(hostp)
                                
                                if hostpp:
                                    hostregex = re.compile('\/([a-zA-Z0-9:.]+)$')
                                    hostmatch = hostregex.search(props['linux.sysfs_path'])
                                    
                                    if hostmatch:
                                        props['pcicard'] = hostmatch.group(1)
                                        
                                    nodename = io.file.readFile(hostdir + '/' + hostpp.group(0) + '/' + 'node_name')
                                    portname = io.file.readFile(hostdir + '/' + hostpp.group(0) + '/' + 'port_name')
                                    portstate = io.file.readFile(hostdir + '/' + hostpp.group(0) + '/' + 'port_state')
                                    porttype = io.file.readFile(hostdir + '/' + hostpp.group(0) + '/' + 'port_type')
                                    speed = io.file.readFile(hostdir + '/' + hostpp.group(0) + '/' + 'speed')
                                    props['nodename'] = nodename[0].strip()
                                    props['portname'] = portname[0].strip()
                                    props['portstate'] = portstate[0].strip()
                                    props['porttype'] = porttype[0].strip()
                                    props['speed'] = speed[0].strip()
                    
                    props['toolindex'] = props['pcicard']
                    
                    self.asset_info.append(props)

            except dbus.DBusException:
                continue
