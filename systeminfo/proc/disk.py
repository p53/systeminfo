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
Module: disk.py

Class: Disk

This class gets info for disks

@author: Pavol Ipoth
@license: GPLv3+
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

import re
import os
import dbus
import ConfigParser
import glob
import sys
import systeminfo.io
import systeminfo.proc.base

class Disk(systeminfo.proc.base.Base):

    lunsbypath = {}
    """
    @type: dict
    @ivar: holds target identificator and lun number from by-path listing
    """

    diskdesc = {}
    """
    @type: dict
    @ivar: holds all info we get except target and lun number
    """

    asset_info = []
    """
    @type: list
    @ivar: holds data about all disks
    """

    fields = [
                'targetport',
                'storage.serial',
                'lunid',
                'storage.model',
                'storage.vendor',
                'storage.size',
                'hwpath',
                'srcport',
                'rportstate',
                'major',
                'minor',
                'firmware',
                'iodone_count',
                'ioerror_count',
                'iorequest_count',
                'queue_depth',
                'scsi_level',
                'state',
                'timeout'
            ]
    """
    @type: list
    @ivar: holds keys which should be always present in diskdesc for each item
    """

    def getData(self, options):
        """
        Method: getData

        Method gathering all info about disks

        @type options: dict
        @param options: passed options
        @rtype: void
        """

        # getting information
        self.getDiskDesc()

        # checking if each item has keys present in fields list, to avoid exceptions
        # and assigning values to asset_info
        for disk, info in self.diskdesc.iteritems():

            for key in self.fields:
                if key not in self.diskdesc[disk].keys():
                    self.diskdesc[disk][key] = ''

            diskinfo = {
                            'toolindex': self.diskdesc[disk]['hwpath'],
                            'device': disk,
                            'targetport': self.diskdesc[disk]['targetport'],
                            'id': str(self.diskdesc[disk]['storage.serial']),
                            'model': unicode(self.diskdesc[disk]['storage.model']),
                            'vendor': unicode(self.diskdesc[disk]['storage.vendor']),
                            'size': "%.f" % (self.diskdesc[disk]['storage.size']),
                            'hwpath': self.diskdesc[disk]['hwpath'],
                            'srcport': self.diskdesc[disk]['srcport'],
                            'rportstate': self.diskdesc[disk]['rportstate'],
                            'major': str(self.diskdesc[disk]['block.major']),
                            'minor': str(self.diskdesc[disk]['block.minor']),
                            'firmware': str(self.diskdesc[disk]['storage.firmware_version']),
                            'iodone_count': str(self.diskdesc[disk]['iodone_count']),
                            'ioerror_count': str(self.diskdesc[disk]['ioerror_count']),
                            'iorequest_count': str(self.diskdesc[disk]['iorequest_count']),
                            'queue_depth': str(self.diskdesc[disk]['queue_depth']),
                            'scsi_level': str(self.diskdesc[disk]['scsi_level']),
                            'state': self.diskdesc[disk]['state'],
                            'timeout': str(self.diskdesc[disk]['timeout']),
                    }

            self.asset_info.append(diskinfo)

    def getDiskDesc(self):
        """
        Method: getLunsByPath

        This method gets target port and lun number for each disk block device

        @rtype: void
        """

        system_bus = dbus.SystemBus()
        try:
            import gudev
            self.getUdevDesc()
        except ImportError:
            hal_mgr_obj = system_bus.get_object('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
            self.getHalDesc()

    def getHalDesc(self):
        """
        Method: getHalDesc

        This method gets info about disks in case there is HAL on system

        @rtype: void
        """

        # getting DBUS object, instantiating HAL Manager
        # getting all devices, because HAL has some bugs in older versions and throws
        # exceptions when looking for specific device, this is slow, but reliable
        system_bus = dbus.SystemBus()
        hal_mgr_obj = system_bus.get_object('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
        hal_mgr_iface = dbus.Interface(hal_mgr_obj, 'org.freedesktop.Hal.Manager')
        devs = hal_mgr_iface.GetAllDevices()

        for i in devs:
            # iterating over devices, getting interface for Device
            dev = system_bus.get_object('org.freedesktop.Hal', i)
            interface = dbus.Interface(dev, dbus_interface='org.freedesktop.Hal.Device')

            # filtering storage devices and devices with info.category
            if interface.PropertyExists('info.category'):
                category = interface.GetProperty('info.category')
                if category == 'storage':
                    props = interface.GetAllProperties()

                    # IDE drives major number is 3 or 22
                    # SCSI drives 8
                    # floppy 2
                    if props['block.major'] in [3,22,8,2]:
                        devpat = re.compile('/dev/(\w{2,2}\w+)')
                        devname = devpat.search(props['block.device'])
                    
                        # some properties are block properties, some on lun level in HAL
                        # thus we are getting also parent device, for getting address of
                        # HBA we are matching regex, remote ports are gathered from sysfs
                        # path of lun
                        props['storage.size'] = float(props['storage.size']) / 1000000.0
                        block_dev_path = props['linux.sysfs_path'] + '/device'
                        parentdev = system_bus.get_object('org.freedesktop.Hal', props['info.parent'])
                        parentiface =dbus.Interface(parentdev, dbus_interface='org.freedesktop.Hal.Device')
                        hwpath = parentiface.GetProperty('linux.sysfs_path')
                        rportregex = re.compile('(.*\/rport-[0-9:-]+\/).*')
                        hwregex = re.compile('.*?\/([a-zA-Z0-9:.]+)$')
                        hostregex = re.compile('\/([a-zA-Z0-9:.]+)\/host[0-9]+')
                        hwmatch = hwregex.search(hwpath)
                        hostmatch = hostregex.search(hwpath)
                        rportmatch = rportregex.search(hwpath)

                        iodone_count = systeminfo.io.file.readFile(block_dev_path + '/iodone_cnt')
                        ioerror_count = systeminfo.io.file.readFile(block_dev_path + '/ioerr_cnt')
                        iorequest_count = systeminfo.io.file.readFile(block_dev_path + '/iorequest_cnt')
                        queue_depth = systeminfo.io.file.readFile(block_dev_path + '/queue_depth')
                        scsi_level = systeminfo.io.file.readFile(block_dev_path + '/scsi_level')
                        state = systeminfo.io.file.readFile(block_dev_path + '/state')
                        timeout = systeminfo.io.file.readFile(block_dev_path + '/timeout')

                        props['iodone_count'] = int(iodone_count[0].strip(), 16)
                        props['ioerror_count'] = int(ioerror_count[0].strip(), 16)
                        props['iorequest_count'] = int(iorequest_count[0].strip(), 16)
                        props['queue_depth'] = queue_depth[0].strip()
                        props['scsi_level'] = scsi_level[0].strip()
                        props['state'] = state[0].strip()
                        props['timeout'] = timeout[0].strip()

                        if rportmatch:
                            rportdir = glob.glob(rportmatch.group(1) + 'fc_remote_ports*')
                            rportstate = systeminfo.io.file.readFile(rportdir[0] + '/port_state')
                            rportname = systeminfo.io.file.readFile(rportdir[0] + '/port_name')
                            props['rportstate'] = rportstate[0].strip()
                            props['targetport'] = rportname[0].strip()

                        if hwmatch:
                            props['hwpath'] = hwmatch.group(1)

                        if hostmatch:
                            props['srcport'] = hostmatch.group(1)

                        self.diskdesc[devname.group(1)] = props

    def getUdevDesc(self):
        """
        Method: getUdevDesc

        Method gets info about disks if Udev is used on the system

        @rtype: void
        """

        # getting block devices, filtering out just disks
        import gudev
        client = gudev.Client(["block"])
        devs = client.query_by_subsystem("block")
        devpat = re.compile('/dev/(\w{2,2}\w+)')

        for dev in devs:
            devicename = dev.get_property('DEVNAME')
            devtype = dev.get_property('DEVTYPE')
            devpath = dev.get_property('DEVPATH')
            majornum = dev.get_property('MAJOR')

            if devtype == 'disk' and majornum in ['3','22','8','3']:
                devicematch = devpat.search(devicename)
                if devicematch:
                    devname = devicematch.group(1)
                    props = {}
                    self.diskdesc[devname] = {}

                    # getting info about src port from sysfs of device
                    hwregex = re.compile('/([0-9:]+)/')
                    hostregex = re.compile('\/([a-zA-Z0-9:.]+)\/host[0-9]+')
                    hwmatch = hwregex.search(devpath)
                    hostmatch = hostregex.search(devpath)

                    blockdev = dev.get_parent()
                    lundev = blockdev.get_parent()
                    rport = lundev.get_parent()
                    rportsysfs = rport.get_sysfs_path()
                    rportpath = glob.glob(rportsysfs + '/' + 'fc_remote_ports' + '/' + 'rport-*')

                    if len(rportpath) > 0:
                        rportstate = systeminfo.io.file.readFile(rportpath[0] + '/' + 'port_state')
                        rportname = systeminfo.io.file.readFile(rportpath[0] + '/' + 'port_name')
                        props['rportstate'] = rportstate[0].strip()
                        props['targetport'] = rportname[0].strip()

                    props['storage.vendor'] = dev.get_property('ID_VENDOR')
                    props['storage.model'] = dev.get_property('ID_MODEL')
                    props['storage.size'] = float(dev.get_sysfs_attr('size')) * 512 / 1000000.0
                    props['storage.serial'] = dev.get_property('ID_SERIAL')
                    props['block.major'] = dev.get_property('MAJOR')
                    props['block.minor'] = dev.get_property('MINOR')
                    props['storage.firmware_version'] = blockdev.get_sysfs_attr('rev')
                    props['state'] = blockdev.get_sysfs_attr('state')
                    props['timeout'] = blockdev.get_sysfs_attr('timeout')
                    props['scsi_level'] = blockdev.get_sysfs_attr('scsi_level')
                    props['queue_depth'] = blockdev.get_sysfs_attr('queue_depth')
                    props['iorequest_count'] = int(blockdev.get_sysfs_attr('iorequest_cnt'), 16)
                    props['iodone_count'] = int(blockdev.get_sysfs_attr('iodone_cnt'), 16)
                    props['ioerror_count'] = int(blockdev.get_sysfs_attr('ioerr_cnt'), 16)

                    if hwmatch:
                        props['hwpath'] = hwmatch.group(1)

                    if hostmatch:
                        props['srcport'] = hostmatch.group(1)

                    self.diskdesc[devname] = props
