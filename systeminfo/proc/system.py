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
Module: system.py

Class: System

This class is class for system asset type

@author: Pavol Ipoth
@license: GPLv3+
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

import dmidecode
import ConfigParser
import re
import sys
import os
import platform
import systeminfo.io
import systeminfo.proc.cpu
import systeminfo.proc.base

class System(systeminfo.proc.base.Base):

    asset_info = [{}]
    """
    @type: list
    @ivar: holds info about system asset type
    """

    def getData(self, options):
        """
        Method getData

        Gets all information for system asset type

        @type options: dict
        @param options: passed options
        @rtype: void
        """
        # getting data from dmidecode and parsing (chassis, system)
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

        # counting totals for cpus, cores
        for hwinfo in dmidecode.processor().iteritems():
            if hwinfo[1]['dmi_type'] == 4 and type(hwinfo[1]['data']) == dict:
                phys_cpu_count += 1
                for iteminfo in hwinfo[1]['data'].iteritems():
                    if iteminfo[1] is not None and iteminfo[1] != '':
                        p = re.compile('\s+')
                        key = p.sub('', iteminfo[0])
                        if key == 'CoreCount':
                            core_count += iteminfo[1]
                        elif key == 'CoreEnabled':
                            core_enabled_count += iteminfo[1]
                        elif key == 'ThreadCount':
                            thread_count += iteminfo[1]

        # we need this part in case dmidecode doesn't provide information
        # for cores and threads
        if thread_count == 0 or core_count == 0:
            cpuObj = systeminfo.proc.cpu.Cpu(self.confDir, self.cacheDir, self.viewDir)
            cpuObj.getData({})
            logic_count = len(cpuObj.asset_info)
            phys_to_cores = {}

            for logic_cpu in cpuObj.asset_info:
                if logic_cpu.get('physicalid'):
                    phys_cpu = logic_cpu.get('physicalid')
                    cores = int(logic_cpu.get('cpucores'), 0)

                    if not phys_to_cores.get('physcpu' + phys_cpu):
                        phys_to_cores['physcpu' + phys_cpu] = cores
                        core_count += cores

            if logic_count > core_count and phys_cpu_count != 0:
                thread_count = logic_count

        # getting memory info
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

        # getting info about distribution, first one is deprecated in newer versions of python
        try:
            distinfo = platform.dist()
        except AttributeError:
            distinfo = platform.linux_distribution()

        self.asset_info[0]['distname']  = distinfo[0]
        self.asset_info[0]['distver']  = distinfo[1]
        self.asset_info[0]['distid']  = distinfo[2]
        self.asset_info[0]['toolindex'] = self.asset_info[0]['SystemSerialNumber']

    def getMemInfo(self):
        """
        Method: getMemInfo

        Method gets information about memory from /proc/meminfo

        @rtype: void
        """

        lines = systeminfo.io.file.readFile('/proc/meminfo')
        for line in lines:
                m = re.search('(.*?)\s*:\s*(.*)', line)
                if m:
                        tmpinfo = {}
                        key = m.group(1)
                        value = m.group(2)
                        p = re.compile('\s+')
                        optim = p.sub('', key)
                        self.asset_info[0]['Memory' + key] = str(value)
