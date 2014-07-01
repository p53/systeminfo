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

tplh = ""
tpl = """%(SystemManufacturer)s#%(SystemSerialNumber)s#%(SystemProductName)s#%(SystemUUID)s#%(ChassisManufacturer)s#%(ChassisSerialNumber)s#%(load)s#%(machinetype)s#%(nodename)s#%(osrelease)s#%(osname)s#%(distname)s#%(distver)s#%(distid)s#%(OSCoreCount)s#%(OSCoreEnabled)s#%(OSThreadCount)s#%(OSPhyscpuCount)s#%(MemoryMemTotal)s#%(MemoryMemFree)s#%(MemorySwapTotal)s#%(MemorySwapFree)s#%(MemoryShmem)s#%(MemoryHardwareCorrupted)s"""
