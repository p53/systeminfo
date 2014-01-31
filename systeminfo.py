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
NAME
       %(program)s - utility for displaying hardware information

SYNOPSIS
       %(program)s --get asset_type [--p|--l|--d identifier] [--c]

DESCRIPTION
       %(program)s is utility for getting hardware information it aims to be simple and provide output in well formated output

OPTIONS
       asset_type
               can be one of these types: system, cpu, memory, disk, pci, fcms, tape

       --l, --long
               specifies to display long output

       --p, --parsable
               specifies to display parsable output

       --d, --detail identifier
               specifies to display detail, requires identifier

               identifier

               column which you should use as identifier is marked in column header with asterisk

       --c, --cached
               use cache to get data, should be faster, but doesn't generate fresh data

EXAMPLES
       This gets information about system in short format:

           %(program)s --get system

       This gets information about disks in long format:

           %(program)s --get disk --l
           or
           %(program)s --get disk --long

       This gets information about fcms HBA's in parsable format:

           %(program)s --get fcms --p

       This get detail about disk device:

           %(program)s --get disk --detail 24:0:2:0

       This refreshes cache info about disks:

           %(program)s --get disk
           %(program)s --get disk --l
           %(program)s --get disk --p

       This doesn't refresh cache:

           (gets fresh data but doesn't update cache)
           %(program)s --get disk --detail 24:0:2:0
           or (these two examples get data from cache)
           %(program)s --get disk --detail 24:0:2:0 --c
           or
           %(program)s --get disk --c
           or
           %(program)s --get disk --l --c
           
NOTES
       This utility should be run with root priveleges

AUTHOR
       Pavol Ipoth

COPYRIGHT AND LICENSE
       Copyright 2013, 2014 Pavol Ipoth

       GPLv3
"""

    print help.__doc__ % {'program': os.path.split(sys.argv[0])[1]}

main()
