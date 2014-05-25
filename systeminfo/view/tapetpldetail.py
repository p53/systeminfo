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
tpl = """%(device|ljust)s
%(id|ljust)s
%(major|ljust)s
%(minor|ljust)s
%(hwpath|ljust)s
%(vendor|ljust)s
%(model|ljust)s
%(srcport|ljust)s
%(targetport|ljust)s
%(rportstate|ljust)s
%(firmware|ljust)s
%(iodone_count|ljust)s
%(ioerror_count|ljust)s
%(iorequest_count|ljust)s
%(queue_depth|ljust)s
%(scsi_level|ljust)s
%(state|ljust)s
%(timeout|ljust)s"""
