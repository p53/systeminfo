#!/usr/bin/python

"""
SystemInfo

Module: systeminfo.py

This python script was written for system administration purposes, to have command line
tool where you can have good and quick overview of properties of different hardware types.

@author: Pavol Ipoth
@license: GPL
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com
@version: 1.2

"""

import os
import sys

# we are checking if effective user runnig script is root
# because of using sysfs we can get results just with root permissions
effective_uid = os.geteuid()

if effective_uid > 0:
    print "To run this utility you need root priveleges!"
    sys.exit(4)
        
import getopt
import re
import systeminfo.misc.config
from string import Template
from systeminfo.proc.cpu import Cpu
from systeminfo.proc.memory import Memory
from systeminfo.proc.pci import Pci
from systeminfo.proc.fcms import Fcms
from systeminfo.proc.disk import Disk
from systeminfo.proc.system import System
from systeminfo.proc.tape import Tape

options = {'outlength': 'short', 'get_data_action': 'getData'}
"""
@type: dict
@var: this is variable with default values passed to action method
"""

asset_types = ['cpu', 'memory', 'pci', 'fcms', 'disk', 'system', 'tape']
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
    
    # Dict for storing list of passed options and their values
    processed_options = {}
    
    # List of passed options
    opt_curr = []
    
    # List of allowed options
    opt_possibilities = [
                            '--parsable', 
                            '--long', 
                            '--help',
                            '--get',
                            '--detail',
                            '--cached',
                            '--h',
                            '--l',
                            '--c'
                        ]
        
    # we are using getopt module although there are more advanced modules
    # because of compatibility with older versions of python
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hlpc', ['parsable', 'long', 'help', 'get=', 'detail=', 'cached'])
    except getopt.GetoptError, e:
        print "Bad required option"
        help()
        sys.exit(3)

    # checking if passed options are among possible ones,
    # if yes insert into dict option - value
    for o, a in opts:
        if o not in opt_possibilities:
            print "Bad option"
            help()
            sys.exit(2)
            
        processed_options[o] = a
    
    # extracting passed options to list
    opt_curr = processed_options.keys()
    
    # checking if several conditions are met and assigning values to parameters 
    # passed later to invoked action method
    if ('l' in opt_curr or '--long' in opt_curr) and '--get' not in opt_curr:
        print "Bad option"
        help()
        sys.exit(2)
    elif 'l' in opt_curr or '--long' in opt_curr:
        options['outlength'] = 'long'

    if ('p' in opt_curr or '--parsable' in opt_curr) and '--get' not in opt_curr:
        print "Bad option"
        help()
        sys.exit(2)
    elif 'p' in opt_curr or '--parsable' in opt_curr:
        options['outlength'] = 'parsable'
    
    if ('c' in opt_curr or '--cached' in opt_curr) and '--get' not in opt_curr:
        print "Bad option"
        help()
        sys.exit(2)
    elif 'c' in opt_curr or '--cached' in opt_curr:
        options['get_data_action'] = 'getCache'
                    
    if 'h' in opt_curr or '--help' in opt_curr:
        help()
        sys.exit()
    
    if '--get' in opt_curr and processed_options['--get'] in asset_types:
        action = 'summary'
        asset_param = processed_options['--get']
        options['template_body_type'] = 'TableTemplate'
        options['template_header_type'] = 'HeaderTableTemplate'
        
        if processed_options['--get'] == 'system':
            options['template_body_type'] = 'PropertyTemplate'
            options['template_header_type'] = 'VoidTemplate'
            
        if '--detail' in opt_curr:
            action = 'detail'
            options['template_body_type'] = 'PropertyTemplate'
            options['template_header_type'] = 'VoidTemplate' 
            options['outlength'] = 'detail'
            options['instance'] = str(processed_options['--detail'])
    else:
        print "Bad option"
        help()
        sys.exit(2)
    
    # instantiating object, his class is asset type
    # and then invoking action on it, depending on passed options
    # , also passing parameters assigned in previous option checking
    asset_type = asset_param.title()
    asset = globals()[asset_type]()
    getattr(asset, 'setConfDir')(systeminfo.misc.config.confDir)
    getattr(asset, 'setCacheDir')(systeminfo.misc.config.cacheDir)
    getattr(asset, action)(options)

def help():
    """
    Usage:

    %(program)s action asset_type [output_type] [caching]

    %(program)s is utility for viewing hardware information
    NOTICE: requires root priveleges
    
    action - this is what we want to do with asset_type
             --get - gets info about specified asset_type

    asset_type - this is asset_type on which we want to perform action
                 currently you can choose from this asset types:
                 cpu, memory, pci, fcms, disk, system, tape

    output_type - this specifies format and length of output
                  currently these are available:

                  default is short output, there is no option for that
                  --l or --long - specifies long output
                  --p or --parsable - is long and parsable output
                  --detail - specifies detail - requires instance identifier,
                  instance identifier is always marked with *

    caching - this options specifies if we want to get info from
              cache, this should be faster (currently speed up
              isn't so big, but will be improved in future version).
              If you want to refresh data use no options or --l or --p
              options.
                
    Examples:

            This gets information about system in short format:

                systeminfo --get system

            This gets information about disks in long format:

                systeminfo --get disk --l
                or
                systeminfo --get disk --long

            This gets information about fcms HBA's in parsable format:

                systeminfo --get fcms --p

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
                        
        Author: Pavol Ipoth
        License: GPLv3
"""

    print help.__doc__ % {'program': os.path.split(sys.argv[0])[1]}

main()
