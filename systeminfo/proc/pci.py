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
Module: pci.py

Class: Pci

This class is class for pci asset type

@author: Pavol Ipoth
@license: GPLv3+
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

import systeminfo.io.file
import os
import os.path
import re
import string
import ConfigParser
import sys
import systeminfo.proc.base
import platform
import csv
import dbus

class Pci(systeminfo.proc.base.Base):

        pciids = {'vendors' : {}, 'devices' : {}, 'classes' : {}, 'subclasses' : {}, 'subdevs' : {}}
        """
        @type: dict
        @ivar: holds mapping between hex values and vendors, classes, subclassess etc...
        """

        asset_info = []
        """
        @type: list
        @ivar: holds info about all pci devices
        """

        pciids_file = '/usr/share/hwdata/pci.ids'
        """
        @type: str
        @ivar: holds location of file with pci ids
        """
        
        pciids_cache_name = 'pciids'
        """
        @type: str
        @ivar: holds name of cache file for pci ids caching
        """
        
        def __init__(self, configDir, cachingDir):
            super(Pci, self).__init__(configDir, cachingDir)
            pciids_cache_file = self.cacheDir + Pci.pciids_cache_name + '.cache'
            cur_timestamp = 0
            
            if os.access(Pci.pciids_file, os.R_OK):
                cur_timestamp = os.path.getmtime(Pci.pciids_file)
                
            cached_pciids = self.getCustomCache(Pci.pciids_cache_name)
            
            if len(cached_pciids) > 0:
                saved_timestamp = cached_pciids.get('timestamp')
                
                if cur_timestamp != saved_timestamp:
                    self.getPciIds()
                    self.pciids['timestamp'] = cur_timestamp
                    self.createCustomCache(Pci.pciids_cache_name, self.pciids)
                else:
                    self.pciids = cached_pciids
                    
            else:       
                self.getPciIds()
                self.pciids['timestamp'] = cur_timestamp
                self.createCustomCache(Pci.pciids_cache_name, self.pciids)
            
        def getPciIds(self):
            """
            Method: getPciIds

            Method gets all info about pci items, parses /usr/share/hwdata/pci.ids file
            for information about pci devices, this file has fixed format

            we are creating this structure from parsing:

                pciids = {
                            'vendors': { '1002': 'AMD', '9092': 'HP'},
                            'classes': {'02': 'Network Controller', '03': 'Display Controller'},
                            'subclasses': {'03': { '00': 'VGA controller'}, '02': {'00': 'Ethernet Controller}},
                            'devices': {'1002': {'4147': 'R300 GL', '4136': 'RS100', '4150': 'RV350'}}
                            'subdevs': {'1002': {'10020002': 'R9600 Pro primary (Asus OEM for HP)'}}
                        }

                pciids = {
                            'vendors': {'vendorhex': 'Vendor', ...},
                            'classes': {'classhex': 'Class name', ...},
                            'subclasses: {'classhex': { 'subclasshex': 'Subclass name', ...}, ...},
                            'devices: {'vendorhex': {'devicehex': 'Device name', ...}, ...},
                            'subdevs: {'vendorhex': {'subdevhex': 'Subdev name', ...}, ...}
                        }

            @rtype: void
            """
            
            isclasssection = 0
            currentclass = ''
            currentvend = ''

            f = open(self.pciids_file, 'r')

            for line in f:
                vend = re.search('^(\w+)\s*(.*)', line)
                dev = re.search('^\t(\w+)\s*(.*)$', line)
                subdev = re.search('^\t\t(\w+)\s+(\w+)\s+(.*)$', line)
                isclasssec = re.search('^C\s+(\w{2,4})\s+(.*)$', line)
                issubclass = re.search('^\t(\w{2,4})\s+(.*)$', line)

                if isclasssec:
                    isclasssection = 1

                if isclasssection:
                    if isclasssec:
                        self.pciids['classes'][isclasssec.group(1)] = isclasssec.group(2)
                        currentclass = isclasssec.group(1)
                    elif issubclass:
                        if currentclass not in self.pciids['subclasses'].keys():
                            self.pciids['subclasses'][currentclass] = {}

                        self.pciids['subclasses'][currentclass][issubclass.group(1)] = issubclass.group(2)
                elif vend:
                    self.pciids['vendors'][vend.group(1)] = vend.group(2)
                    currentvend = vend.group(1)
                elif dev:
                    if currentvend not in self.pciids['devices'].keys():
                        self.pciids['devices'][currentvend] = {}
                
                    self.pciids['devices'][currentvend][dev.group(1)] = dev.group(2)
                elif subdev:
                    if currentvend not in self.pciids['subdevs'].keys():
                        self.pciids['subdevs'][currentvend] = {}
                
                    self.pciids['subdevs'][currentvend][subdev.group(1) + subdev.group(2)] = subdev.group(3)
                
            f.close()
                        
        def getData(self, options):
            """
            Method: getData

            Method gets info about PCI devices on the host
            
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

            Getting information for systems with Udev

            @type options: dict
            @param options: passed parameters
            @rtype: void
            """
            
            # getting info about pci devices, matching against pci ids parsed earlier
            import gudev
            client = gudev.Client(["pci"])
            devs = client.query_by_subsystem("pci")

            for dev in devs:
                props = self.getUdevPciDevInfo(dev)

                self.asset_info.append(props)

        def getHalDevs(self, options):
            """
            Method: getHalDevs

            Getting about pci devices on systems with HAL

            @type options: dict
            @param options: passed parameters
            @rtype: void
            """
            system_bus = dbus.SystemBus()
            hal_mgr_obj = system_bus.get_object('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
            hal_mgr_iface = dbus.Interface(hal_mgr_obj, 'org.freedesktop.Hal.Manager')
            devs = hal_mgr_iface.GetAllDevices()

            for i in devs:
                dev = system_bus.get_object('org.freedesktop.Hal', i)
                interface = dbus.Interface(dev, dbus_interface='org.freedesktop.Hal.Device')

                try:
                    subsystem = interface.GetProperty('linux.subsystem')

                    if subsystem == 'pci':
                        props = self.getHalPciDevInfo(interface)
                        self.asset_info.append(props)

                except dbus.DBusException:
                    continue
                
         
        def getUdevPciDevInfo(self, device):
             props = {}

             vendorhex = device.get_sysfs_attr('vendor')
             devhex = device.get_sysfs_attr('device')
             classhex = device.get_sysfs_attr('class')
             subvendhex = device.get_sysfs_attr('subsystem_vendor')
             subdevhex = device.get_sysfs_attr('subsystem_device')
 
             vendorhex = string.replace(vendorhex, '0x', '')
             devhex = string.replace(devhex, '0x', '')
             classhex = string.replace(classhex, '0x', '')
             subvendhex = string.replace(subvendhex, '0x', '')
             subdevhex = string.replace(subdevhex, '0x', '')
             subdevid = subvendhex + subdevhex
 
             subdevice = ''
 
             classreg = re.search('^(\w{2})(\w{2})(\w{2})', classhex)
 
             if vendorhex in self.pciids['subdevs'].keys():
                 if subdevid in self.pciids['subdevs'][vendorhex].keys():
                     subdevice = self.pciids['subdevs'][vendorhex][subdevid]
 
             props['addr'] = device.get_property('PCI_SLOT_NAME')
             props['vendor'] = self.pciids['vendors'][vendorhex]
             props['device'] = self.pciids['devices'][vendorhex][devhex]
             props['class'] = self.pciids['classes'][classreg.group(1)]
             props['subclass'] = self.pciids['subclasses'][classreg.group(1)][classreg.group(2)]
             props['subdevice'] = subdevice
             props['driver'] = device.get_property('DRIVER')
             props['sysfspath'] = device.get_sysfs_path()
             props['localcpus'] = device.get_sysfs_attr('local_cpus')
             props['irq'] = device.get_sysfs_attr('irq')
             props['numanode'] = device.get_sysfs_attr('numa_node')
             props['localcpulist'] = device.get_sysfs_attr('local_cpulist')
 
             props['toolindex'] = props['addr']
             
             return props

        def getHalPciDevInfo(self, devIntf):
             props = devIntf.GetAllProperties()
             addr_match = re.search('.*?\/([a-zA-Z:0-9\.]+)$', props['linux.sysfs_path'])
             addr = ''
             subdevice = ''
             
             irq = systeminfo.io.file.readFile(props['linux.sysfs_path'] + '/irq')
             local_cpus = systeminfo.io.file.readFile(props['linux.sysfs_path'] + '/local_cpus')
             
             if addr_match:
                 addr = addr_match.group(1)
             
             # HAL has these numbers in decimal we need to get it in hex
             # to be able to match against pci ids
             vendorhex = props['pci.vendor_id']
             classhex = hex(props['pci.device_class'])
             subclasshex = hex(props['pci.device_subclass'])
             subvendhex = hex(props['pci.subsys_vendor_id'])
             subdevhex = hex(props['pci.subsys_product_id'])
         
             vendorhex = string.replace(str(vendorhex), '0x', '')
             # in pci ids are hex numbers with 2 zeros fill, so we
             # need to convert our numbers from HAL to same format
             classhex = "%02x" % int(classhex[2:], 16)
             subclasshex = "%02x" % int(subclasshex[2:], 16)
             subvendhex = "%02x" % int(subvendhex[2:], 16)
             subdevhex = "%02x" % int(subdevhex[2:], 16)
             subdevid = subvendhex + subdevhex
         
             if vendorhex in self.pciids['subdevs'].keys():
                 if subdevid in self.pciids['subdevs'][vendorhex].keys():
                     subdevice = self.pciids['subdevs'][vendorhex][subdevid]
         
             props['addr'] = addr
             props['vendor'] = props['pci.vendor']
             props['device'] = props['pci.product']
             props['class'] = self.pciids['classes'][classhex]
             props['subclass'] = self.pciids['subclasses'][classhex][subclasshex]
             props['subdevice'] = subdevice
             props['sysfspath'] = props['linux.sysfs_path']
             props['localcpus'] = local_cpus[0].strip()
             props['irq'] = irq[0].strip()
             props['numanode'] = ''
             props['local_cpulist'] = ''
     
             if 'info.linux.driver' in props.keys():
                props['driver'] = props['info.linux.driver']
     
             props['toolindex'] = props['addr']
             
             props_unicode = dict([(unicode(x),unicode(y)) for x, y in props.iteritems()])
             
             return props_unicode
 