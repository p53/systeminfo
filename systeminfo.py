#!/usr/bin/python
#
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
SystemInfo

Module: systeminfo.py

This python script was written for system administration purposes, to have command line
tool where you can have good and quick overview of properties of different hardware types.

@author: Pavol Ipoth
@license: GPLv3+
@copyright: Copyright 2015 Pavol Ipoth
@contact: pavol.ipoth@gmail.com
@version: 1.5.0

"""

import os
import sys

# we are checking if effective user runnig script is root
# because of using sysfs we can get results just with root permissions
effective_uid = os.geteuid()

if effective_uid > 0:
    print "To run this utility you need root priveleges!"
    sys.exit(4)

import argparse
import systeminfo.misc.config

options = {'outlength': 'short', 'get_data_action': 'getData'}
"""
@type: dict
@var: this is variable with default values passed to action method
"""

asset_types = ['cpu', 'memory', 'pci', 'fcms', 'disk', 'system', 'tape', 'eth']
"""
@type: list
@var: list of asset types currently supported by tool
"""

def main():
    """
    Function: main

    This is the main function of the tool, processes options and invokes
    responsible classes and methods

    @rtype: void
    """

    # Action which we want to perform on asset_types
    action = ''

    # Asset type on which we want to perform aciont
    asset_param = ''

    parser = argparse.ArgumentParser(
        description="description: Utility for viewing HW information"
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-l", 
        "--long", 
        help="display in long table format",
        action='store_const', 
        dest='outlength',
        const='long'
    )
    group.add_argument(
        "-p", 
        "--parsable",
        help="display in parsable format",
        action='store_const', 
        dest='outlength',
        const='parsable'
    )
    group.add_argument(
        "-d",
        "--detail",
        help="display detail of hw instance",
        dest='identifier'
    )
    group.add_argument(
        "-j",
        "--json",
        help="display results in json format",
        action='store_const', 
        dest='outlength',
        const='json'
    )
    parser.add_argument(
        "-g", 
        "--get", 
        help="specify type of hardware to get info for, required argument",
        choices=asset_types,
        required=True
    )
    parser.add_argument(
        "-c", 
        "--cached",
        help="display results from cache",
        action='store_const', 
        dest='',
        const='getCache'
    )

    results = parser.parse_args()
    
    if results.outlength:
        options['outlength'] = results.outlength
    
    action = 'summary'
    asset_param = results.get
    options['template_body_type'] = 'TableTemplate'

    if results.identifier:
        action = 'detail'
        options['template_body_type'] = 'PropertyTemplateAll'
        options['outlength'] = 'detail'
        options['instance'] = results.identifier

    if results.outlength == 'json':
        action = 'summary'
        options['template_body_type'] = 'PropertyTemplateAll'

    # instantiating object, his class is asset type
    # and then invoking action on it, depending on passed options
    # , also passing parameters assigned in previous option checking
    asset_type = asset_param.title()
    configDir = systeminfo.misc.config.confDir
    cachingDir = systeminfo.misc.config.cacheDir
    viewDir = systeminfo.misc.config.viewDir
    
    mod = __import__('systeminfo.proc.' + asset_param, globals(), locals(), [asset_type], -1)
    asset_python_class = getattr(mod, asset_type)
    asset = asset_python_class(configDir, cachingDir, viewDir)

    getattr(asset, action)(options)

if __name__ == '__main__':
    main()
