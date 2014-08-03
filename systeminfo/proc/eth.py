# Systeminfo - Simple utility for gathering hardware summary information
# Copyright (C) 2013, 2014  Pavol Ipoth  <pavol.ipoth@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# -*- coding: utf-8 -*-

"""
Module: eth.py

Class: Eth

This class is class for net asset type

@author: Pavol Ipoth
@license: GPLv3+
@copyright: Copyright 2014 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

import systeminfo.io.file
import os
import re
import string
import ConfigParser
import dbus
import systeminfo.proc.pci
import sys
import systeminfo.proc.base

class Eth(systeminfo.proc.base.Base):

    asset_info = []
    """
    @type: list
    @ivar: holds info about all net devices
    """
    
    def getData(self, options):
        """
        Method: getData

        Method gets info about fcms devices, routes to appropriate method, depending if
        HAL or Udev is used

        @type options: dict
        @param options: passed options
        @rtype: void
        """
        system_bus = dbus.SystemBus()
        
        try:
            import gudev
            self.getUdevDevs(options)
        except ImportError:
            hal_mgr_obj = system_bus.get_object('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
            self.getHalDevs(options)
            
    
    def getUdevDevs(self, options):
        """
        Method: getUdevDevs
    
        Method gets info about FC HBA's for systems with Udev
    
        @type options: dict
        @param options: passed options
        @rtype: void
        """
        
        # getting fc_host devices, these are HBA ports
        import gudev
        client = gudev.Client(["net"])
        devs = client.query_by_subsystem("net")
        
        # getting information all pci cards, and from those we will select our HBAs
        pciinfo = systeminfo.proc.pci.Pci()
        pciinfo.getData(options)
        
        for dev in devs:
            props = {}
            parentdev = dev.get_parent()

            if parentdev:
                classhex = parentdev.get_sysfs_attr('class')
                
                if classhex:
                    classhex = string.replace(classhex, '0x', '')
        
                    classreg = re.search('^(\w{2})(\w{2})(\w{2})', classhex)
                    
                    parentClassId = classreg.group(1)
                    parentSubClassId = classreg.group(2)
                    
                    if parentClassId == '02' and parentSubClassId == '00':
                        
                        vendorhex = parentdev.get_sysfs_attr('vendor')
                        devhex = parentdev.get_sysfs_attr('device')
                        subvendhex = parentdev.get_sysfs_attr('subsystem_vendor')
                        subdevhex = parentdev.get_sysfs_attr('subsystem_device')
            
                        vendorhex = string.replace(vendorhex, '0x', '')
                        devhex = string.replace(devhex, '0x', '')
                        subvendhex = string.replace(subvendhex, '0x', '')
                        subdevhex = string.replace(subdevhex, '0x', '')
            
                        devsysfspath = dev.get_sysfs_path()
                        
                        duplex = systeminfo.io.file.readFile(devsysfspath + '/' + 'duplex')
                        speed = systeminfo.io.file.readFile(devsysfspath + '/' + 'speed')
                                        
                        props['addr'] = parentdev.get_property('PCI_SLOT_NAME')
                        props['vendor'] = pciinfo.pciids['vendors'][vendorhex]
                        props['device'] = pciinfo.pciids['devices'][vendorhex][devhex]
                        props['class'] = pciinfo.pciids['classes'][parentClassId]
                        props['subclass'] = pciinfo.pciids['subclasses'][parentClassId][parentSubClassId]
                        props['driver'] = parentdev.get_property('DRIVER')
                        props['sysfspath'] = parentdev.get_sysfs_path()
                        props['localcpus'] = parentdev.get_sysfs_attr('local_cpus')
                        props['irq'] = parentdev.get_sysfs_attr('irq')
                        props['numanode'] = parentdev.get_sysfs_attr('numa_node')
                        props['localcpulist'] = parentdev.get_sysfs_attr('local_cpulist')
                        
                        props['mac'] = dev.get_sysfs_attr('address')
                        props['operstate'] = dev.get_sysfs_attr('operstate')
                        props['mtu'] = dev.get_sysfs_attr('mtu')
                        props['intf'] = dev.get_property('INTERFACE')
                        props['duplex'] = duplex[0].strip()
                        props['speed'] = speed[0].strip()
                                                
                        props['toolindex'] = props['addr']
            
                        self.asset_info.append(props)
                
    def getHalDevs(self, options):
        """
        Method: getHalDevs
    
        Method gets info about FC HBA's for systems with HAL
    
        @type options: dict
        @param options: passed options
        @rtype: void
        """
        
        # again we get all devices, to have compatibility with older HAL
        system_bus = dbus.SystemBus()
        hal_mgr_obj = system_bus.get_object('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
        hal_mgr_iface = dbus.Interface(hal_mgr_obj, 'org.freedesktop.Hal.Manager')
        devs = hal_mgr_iface.GetAllDevices()
        
        for i in devs:
            dev = system_bus.get_object('org.freedesktop.Hal', i)
            interface = dbus.Interface(dev, dbus_interface='org.freedesktop.Hal.Device')
        
            # filtering out net devices
            try:
                
                subsystem = interface.GetProperty('linux.subsystem')

                if subsystem == 'net':

                    parentudi = interface.GetProperty('info.parent')
                    parentdev = system_bus.get_object('org.freedesktop.Hal', parentudi)
                    parentintf = dbus.Interface(parentdev, dbus_interface='org.freedesktop.Hal.Device')
                    parentclass = parentintf.GetProperty('pci.device_class')
                    parentsubclass = parentintf.GetProperty('pci.device_subclass')            
                    
                    if parentclass == 2 and parentsubclass == 0:

                        props = interface.GetAllProperties()
                        
                        parentsysfspath = parentintf.GetProperty('linux.sysfs_path')
                        addr_match = re.search('.*?\/([a-zA-Z:0-9\.]+)$', parentsysfspath)
                        addr = ''
                        
                        if addr_match:
                            addr = addr_match.group(1)
                                                
                        devsysfspath = interface.GetProperty('linux.sysfs_path')
                        mac_addr = interface.GetProperty('net.address')
                        intf_name = interface.GetProperty('net.interface')
                        vendor = parentintf.GetProperty('info.vendor')
                        product = parentintf.GetProperty('info.product')
                        driver = parentintf.GetProperty('info.linux.driver')
                        parentsysfspath = parentintf.GetProperty('pci.linux.sysfs_path')
                        
                        duplex = systeminfo.io.file.readFile(devsysfspath + '/' + 'duplex')
                        mtu = systeminfo.io.file.readFile(devsysfspath + '/' + 'mtu')
                        operstate = systeminfo.io.file.readFile(devsysfspath + '/' + 'operstate')
                        speed = systeminfo.io.file.readFile(devsysfspath + '/' + 'speed')

                        irq = systeminfo.io.file.readFile(parentsysfspath + '/irq')
                        local_cpus = systeminfo.io.file.readFile(parentsysfspath + '/local_cpus')
                                                
                        props['addr'] = addr
                        props['numanode'] = ''
                        props['local_cpulist'] = ''
                        props['localcpus'] = local_cpus[0].strip()
                        props['irq'] = irq[0].strip()        
                                    
                        props['duplex'] = duplex[0].strip()
                        props['mtu'] = mtu[0].strip()
                        props['operstate'] = operstate[0].strip()
                        props['speed'] = speed[0].strip()
                        props['mac'] = mac_addr
                        props['intf'] = intf_name
                        props['vendor'] = vendor
                        props['product'] = product
                        props['sysfspath'] = parentsysfspath
                        props['driver'] = driver
                        
                        props['toolindex'] = props['addr']

                        props_unicode = dict([(unicode(x), unicode(y)) for x, y in props.iteritems()])
    
                        self.asset_info.append(props_unicode)
                        
            except dbus.DBusException:
                continue