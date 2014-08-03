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
tpl = """%(vendor)s#%(addr)s#%(portname)s#%(porttype)s#%(portstate)s#%(speed)s#%(sysfspath)s#%(nodename)s#%(fabricname)s#%(portid)s#%(symbolicname)s#%(supportedclasses)s#%(supportedspeeds)s#%(driver)s#%(maxnpivvports)s#%(npivvportsinuse)s#%(localcpus)s#%(localcpulist)s#%(numanode)s#%(irq)s
"""
