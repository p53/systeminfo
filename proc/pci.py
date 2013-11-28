import io.file
import os
import re
import string
import template.tabletemplate
import ConfigParser
import sys
import proc.base

class Pci(proc.base.Base):
        pciids = {'vendors' : {}, 'devices' : {}, 'classes' : {}, 'subclasses' : {}, 'subdevs' : {}}
        pcidevs = []
        asset_info = []

        def getData(self, options):
            isclasssection = 0
            currentclass = ''
            currentvend = ''
                
            f = open('/usr/share/hwdata/pci.ids', 'r')
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

            self.pcidevs = os.listdir('/sys/bus/pci/devices')

            for i in self.pcidevs:
                vendorInfo = io.file.readFile('/sys/bus/pci/devices/' + i + '/vendor')
                classInfo = io.file.readFile('/sys/bus/pci/devices/' + i + '/class')
                deviceInfo = io.file.readFile('/sys/bus/pci/devices/' + i + '/device')
                subvend = io.file.readFile('/sys/bus/pci/devices/' + i + '/subsystem_vendor')
                subdev = io.file.readFile('/sys/bus/pci/devices/' + i + '/subsystem_device')

                vendor = vendorInfo[0].strip()
                classi = classInfo[0].strip()
                device = deviceInfo[0].strip()
                subvend = subvend[0].strip()
                subdev = subdev[0].strip()
                vendor = string.replace(vendor, '0x', '')
                classi = string.replace(classi, '0x', '')
                device = string.replace(device, '0x', '')
                subvend = string.replace(subvend, '0x', '')
                subdev = string.replace(subdev, '0x', '')
                subdevid = subvend + subdev
                subdevice = ''

                classreg = re.search('^(\w{2})(\w{2})(\w{2})', classi)

                if vendor in self.pciids['subdevs'].keys():
                    if subdevid in self.pciids['subdevs'][vendor].keys():
                        subdevice = self.pciids['subdevs'][vendor][subvend+subdev]

                self.asset_info.append({
                            'toolindex': i,
                            'addr': i, 
                            'vendor' : self.pciids['vendors'][vendor],
                            'device' : self.pciids['devices'][vendor][device],
                            'class' : self.pciids['classes'][classreg.group(1)],
                            'subclass' : self.pciids['subclasses'][classreg.group(1)][classreg.group(2)],
                            'subdevice' : subdevice
                        })

