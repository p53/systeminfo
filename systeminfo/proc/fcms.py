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
Module: fcms.py

Class: Fcms

This class is class for fcms asset type

@author: Pavol Ipoth
@license: GPLv3+
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

import systeminfo.io.file
import os
import re
import ConfigParser
import dbus
import systeminfo.proc.pci
import sys
import systeminfo.proc.base

class Fcms(systeminfo.proc.base.Base):

    asset_info = []
    """
    @type: list
    @ivar: holds info about all fcms devices
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
        client = gudev.Client(["fc_host"])
        devs = client.query_by_subsystem("fc_host")
        # getting information all pci cards, and from those we will select our HBAs
        pciinfo = systeminfo.proc.pci.Pci(self.confDir, self.cacheDir)
        
        for dev in devs:
                props = {}
                parentdev = dev.get_parent()
                grandparent = parentdev.get_parent()
 
                props = pciinfo.getUdevPciDevInfo(grandparent)

                props['nodename'] = dev.get_sysfs_attr('node_name')
                props['portname'] = dev.get_sysfs_attr('port_name')
                props['portstate'] = dev.get_sysfs_attr('port_state')
                props['porttype'] = dev.get_sysfs_attr('port_type')
                props['speed'] = dev.get_sysfs_attr('speed')
                props['fabricname'] = dev.get_sysfs_attr('fabric_name')
                props['supportedclasses'] = dev.get_sysfs_attr('supported_classes')
                props['supportedspeeds'] = dev.get_sysfs_attr('supported_speeds')
                props['maxnpivvports'] = dev.get_sysfs_attr('max_npiv_vports')
                props['npivvportsinuse'] = dev.get_sysfs_attr('npiv_vports_inuse')
                props['portid'] = dev.get_sysfs_attr('port_id')
                props['symbolicname'] = dev.get_sysfs_attr('symbolic_name')

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
        pciinfo = systeminfo.proc.pci.Pci(self.confDir, self.cacheDir)
        
        for i in devs:
            dev = system_bus.get_object('org.freedesktop.Hal', i)
            interface = dbus.Interface(dev, dbus_interface='org.freedesktop.Hal.Device')

            # filtering out HBAs and Fiber channel, those have specific numbers in pci.ids file
            try:
                classNum = interface.GetProperty('pci.device_class')
                subclassNum = interface.GetProperty('pci.device_subclass')

                if classNum == 12 and subclassNum == 4:
                    props = interface.GetAllProperties()
                    pcipath = os.listdir(props['linux.sysfs_path'])

                    # for each fc_host get information on fc, scsi level
                    for path in pcipath:
                        pattern = re.compile('host[0-9]+')
                        mpath = pattern.search(path)

                        if mpath:
                            hostdir = props['linux.sysfs_path'] + '/' + mpath.group(0)
                            hostpath = os.listdir(hostdir)

                            for hostp in hostpath:
                                pattern = re.compile('fc_host.*')
                                scsipattern = re.compile('scsi_host.*')
                                hostpp = pattern.search(hostp)
                                scsihostpp = scsipattern.search(hostp)

                                if hostpp:
                                    props = pciinfo.getHalPciDevInfo(interface)

                                    nodename = systeminfo.io.file.readFile(hostdir + '/' + hostpp.group(0) + '/' + 'node_name')
                                    portname = systeminfo.io.file.readFile(hostdir + '/' + hostpp.group(0) + '/' + 'port_name')
                                    portstate = systeminfo.io.file.readFile(hostdir + '/' + hostpp.group(0) + '/' + 'port_state')
                                    porttype = systeminfo.io.file.readFile(hostdir + '/' + hostpp.group(0) + '/' + 'port_type')
                                    speed = systeminfo.io.file.readFile(hostdir + '/' + hostpp.group(0) + '/' + 'speed')
                                    fabricname = systeminfo.io.file.readFile(hostdir + '/' + hostpp.group(0) + '/' + 'fabric_name')
                                    supported_classes = systeminfo.io.file.readFile(hostdir + '/' + hostpp.group(0) + '/' + 'supported_classes')
                                    supported_speeds = systeminfo.io.file.readFile(hostdir + '/' + hostpp.group(0) + '/' + 'supported_speeds')
                                    port_id = systeminfo.io.file.readFile(hostdir + '/' + hostpp.group(0) + '/' + 'port_id')
                                    symbolic_name = systeminfo.io.file.readFile(hostdir + '/' + hostpp.group(0) + '/' + 'symbolic_name')

                                    props['nodename'] = nodename[0].strip()
                                    props['portname'] = portname[0].strip()
                                    props['portstate'] = portstate[0].strip()
                                    props['porttype'] = porttype[0].strip()
                                    props['speed'] = speed[0].strip()
                                    props['fabricname'] = fabricname[0].strip()
                                    props['supportedclasses'] = supported_classes[0].strip()
                                    props['supportedspeeds'] = supported_speeds[0].strip()
                                    props['portid'] = port_id[0].strip()
                                    props['symbolicname'] = symbolic_name[0].strip()

                                if scsihostpp:
                                    max_npiv_vports = systeminfo.io.file.readFile(hostdir + '/' + scsihostpp.group(0) + '/' + 'max_npiv_vports')
                                    npiv_vports_inuse = systeminfo.io.file.readFile(hostdir + '/' + scsihostpp.group(0) + '/' + 'npiv_vports_inuse')

                                    props['maxnpivvports'] = max_npiv_vports[0].strip()
                                    props['npivvportsinuse'] = npiv_vports_inuse[0].strip()

                    props_unicode = dict([(unicode(x), unicode(y)) for x, y in props.iteritems()])

                    self.asset_info.append(props_unicode)

            except dbus.DBusException:
                continue
