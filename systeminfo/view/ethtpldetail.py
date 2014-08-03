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
tpl = """%(intf|ljust)s
%(sysfspath|ljust)s  
%(device|ljust)s
%(vendor|ljust)s
%(driver|ljust)s
%(mac|ljust)s
%(operstate|ljust)s
%(speed|ljust)s
%(duplex|ljust)s
%(mtu|ljust)s
%(localcpus|ljust)s
%(localcpulist|ljust)s
%(numanode|ljust)s
%(irq|ljust)s
%(addr|ljust)s"""