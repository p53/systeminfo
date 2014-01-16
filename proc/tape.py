"""
Module: tape.py

Class: Tape

This class gets info for tapes

@author: Pavol Ipoth
@license: GPL
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

import re
import os
import dbus
from string import Template
import template.tabletemplate
import ConfigParser
import string
import glob
import sys
import io
import proc.base

class Tape(proc.base.Base):
    
    lunsbypath = {}
    """
    @type: dict
    @ivar: holds target identificator and lun number from by-path listing
    """
    
    tapedesc = {}
    """
    @type: dict
    @ivar: holds all info we get except target and lun number
    """

    asset_info = []
    """
    @type: list
    @ivar: holds data about all tapes
    """
        
    fields = [
                'targetport', 
                'storage.serial', 
                'storage.model', 
                'storage.vendor', 
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
    @ivar: holds keys which should be always present in tapedesc for each item
    """
    
    def getData(self, options):
        """
        Method: getData
        
        Method gathering all info about tapes
        
        @type options: dict
        @param options: passed options
        @rtype: void
        """
    
        # getting information
        self.getTapeDesc()
        
        # checking if each item has keys present in fields list, to avoid exceptions
        # and assigning values to asset_info
        for tape, info in self.tapedesc.iteritems():
        
            for key in self.fields:
                if key not in self.tapedesc[tape].keys():
                    self.tapedesc[tape][key] = ''

            tapeinfo = {    
                            'toolindex': self.tapedesc[tape]['hwpath'],
                            'device': tape,
                            'targetport': self.tapedesc[tape]['targetport'],
                            'id': str(self.tapedesc[tape]['storage.serial']),
                            'model': unicode(self.tapedesc[tape]['storage.model']),
                            'vendor': unicode(self.tapedesc[tape]['storage.vendor']),
                            'hwpath': self.tapedesc[tape]['hwpath'],
                            'srcport': self.tapedesc[tape]['srcport'],
                            'rportstate': self.tapedesc[tape]['rportstate'],
                            'major': str(self.tapedesc[tape]['block.major']),
                            'minor': str(self.tapedesc[tape]['block.minor']),
                            'firmware': str(self.tapedesc[tape]['storage.firmware_version']),
                            'iodone_count': str(self.tapedesc[tape]['iodone_count']),
                            'ioerror_count': str(self.tapedesc[tape]['ioerror_count']),
                            'iorequest_count': str(self.tapedesc[tape]['iorequest_count']),
                            'queue_depth': str(self.tapedesc[tape]['queue_depth']),
                            'scsi_level': str(self.tapedesc[tape]['scsi_level']),
                            'state': self.tapedesc[tape]['state'],
                            'timeout': str(self.tapedesc[tape]['timeout']),
                    }

            self.asset_info.append(tapeinfo)

    def getTapeDesc(self):
        """
        Method: getLunsByPath
        
        This method gets target port and lun number for each tape block device
        
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
        
        This method gets info about tapes in case there is HAL on system
        
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
            if interface.PropertyExists('scsi.type'):
                category = interface.GetProperty('scsi.type')
                if category == 'tape':
                    props = interface.GetAllProperties()
                    devpat = re.compile('(st\w+)$')
                    tapedevnamelink = props['linux.sysfs_path'] + '/tape'
                    tapedevlink = os.readlink(tapedevnamelink);
                    devname = devpat.search(tapedevlink)   
                    
                    if devname:
                        # some properties are block properties, some on lun level in HAL
                        # thus we are getting also parent device, for getting address of
                        # HBA we are matching regex, remote ports are gathered from sysfs
                        # path of lun
                        block_dev_path = props['linux.sysfs_path']
                        parentdev = system_bus.get_object('org.freedesktop.Hal', props['info.parent'])
                        parentiface =dbus.Interface(parentdev, dbus_interface='org.freedesktop.Hal.Device')
                        hwpath = parentiface.GetProperty('linux.sysfs_path')
                        rportregex = re.compile('(.*\/rport-[0-9:-]+\/).*')
                        hwregex = re.compile('.*?\/([a-zA-Z0-9:.]+)$')
                        hostregex = re.compile('\/([a-zA-Z0-9:.]+)\/host[0-9]+')
                        hwmatch = hwregex.search(block_dev_path)
                        hostmatch = hostregex.search(block_dev_path)
                        rportmatch = rportregex.search(block_dev_path)
                        
                        iodone_count = io.file.readFile(block_dev_path + '/iodone_cnt')
                        ioerror_count = io.file.readFile(block_dev_path + '/ioerr_cnt')
                        iorequest_count = io.file.readFile(block_dev_path + '/iorequest_cnt')
                        queue_depth = io.file.readFile(block_dev_path + '/queue_depth')
                        scsi_level = io.file.readFile(block_dev_path + '/scsi_level')
                        state = io.file.readFile(block_dev_path + '/state')
                        timeout = io.file.readFile(block_dev_path + '/timeout')
                        firmware = io.file.readFile(block_dev_path + '/rev')
                        majorminor = io.file.readFile(tapedevnamelink + '/dev')
                        majorminor_list = majorminor[0].split(':');
                        
                        props['iodone_count'] = int(iodone_count[0].strip(), 16)
                        props['ioerror_count'] = int(ioerror_count[0].strip(), 16)
                        props['iorequest_count'] = int(iorequest_count[0].strip(), 16)
                        props['queue_depth'] = queue_depth[0].strip()
                        props['scsi_level'] = scsi_level[0].strip()
                        props['state'] = state[0].strip()
                        props['timeout'] = timeout[0].strip()
                        props['block.major'] = majorminor_list[0].strip()
                        props['block.minor'] = majorminor_list[1].strip()
                        props['storage.firmware_version'] = firmware[0].strip()
                        props['storage.vendor'] = props['scsi.vendor']
                        props['storage.model'] = props['scsi.model']
                        
                        if rportmatch:
                            rportdir = glob.glob(rportmatch.group(1) + 'fc_remote_ports*')
                            rportstate = io.file.readFile(rportdir[0] + '/port_state')
                            rportname = io.file.readFile(rportdir[0] + '/port_name')
                            props['rportstate'] = rportstate[0].strip()
                            props['targetport'] = rportname[0].strip()
                            
                        if hwmatch:
                            props['hwpath'] = hwmatch.group(1)
                         
                        if hostmatch:
                            props['srcport'] = hostmatch.group(1)
                        
                        self.tapedesc[devname.group(1)] = props

    def getUdevDesc(self):
        """
        Method: getUdevDesc
        
        Method gets info about tapes if Udev is used on the system
        
        @rtype: void
        """
        
        # getting block devices, filtering out just tapes
        import gudev
        client = gudev.Client(["scsi_tape"])
        devs = client.query_by_subsystem("scsi_tape")

        for dev in devs:
            devicename = dev.get_property('DEVNAME')
            devpath = dev.get_property('DEVPATH')
            devname = dev.get_name();
            devtype = dev.get_property('ID_TYPE')
            devnameregex = re.compile('^st[0-9a-z]+$')
            
            if devtype == 'tape' and devnameregex.search(devname):
                props = {}
                self.tapedesc[devname] = {}

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
                    rportstate = io.file.readFile(rportpath[0] + '/' + 'port_state')
                    rportname = io.file.readFile(rportpath[0] + '/' + 'port_name')
                    props['rportstate'] = rportstate[0].strip()
                    props['targetport'] = rportname[0].strip()

                props['storage.vendor'] = dev.get_property('ID_VENDOR')
                props['storage.model'] = dev.get_property('ID_MODEL')
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

                self.tapedesc[devname] = props
