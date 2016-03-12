Systeminfo
==========

Simple utility for gathering hardware summary information

##### NAME

       systeminfo - utility for displaying hardware information

##### SYNOPSIS
     
       systeminfo --get asset_type [--p|--l|--j|--d identifier] [--c]

##### DESCRIPTION

       systeminfo is utility for getting hardware information it aims 
       to be simple and provide output in well formatted output

##### OPTIONS

       asset_type
               can be one of these types: system, cpu, memory, disk, pci, fcms, tape, eth


       --l, --long
               specifies to display long output


       --p, --parsable
               specifies to display parsable output


       --j, --json
               specifies to display output in json


       --d, --detail identifier
               specifies to display detail, requires identifier

               identifier

               column which you should use as identifier is marked in column header with asterisk


       --c, --cached
               use cache to get data, should be faster, but doesn't generate fresh data

##### EXAMPLES

       This gets information about system in short format:

           systeminfo --get system

       This gets information about disks in long format:

           systeminfo --get disk --l
           or
           systeminfo --get disk --long

       This gets information about fcms HBA's in parsable format:

           systeminfo --get fcms --p

       This gets information about memory in json format:

           systeminfo --get memory --j

       This get detail about disk device:

           systeminfo --get disk --detail 24:0:2:0

       This refreshes cache info about disks:

           systeminfo --get disk
           systeminfo --get disk --l
           systeminfo --get disk --p

       This doesn't refresh cache:

           (gets fresh data but doesn't update cache)
           systeminfo --get disk --detail 24:0:2:0
           or (these two examples get data from cache)
           systeminfo --get disk --detail 24:0:2:0 --c
           or
           systeminfo --get disk --c
           or
           systeminfo --get disk --l --c

##### NOTES
       This utility should be run with root priveleges
       Utility works with python 2.7<, doesn't work with python3 yet

License and Copyright
=====================

Copyright (C) 2013, 2014  Pavol Ipoth  <pavol.ipoth@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
