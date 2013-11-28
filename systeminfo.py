#!/usr/bin/python

import sys
import getopt
import re
import os
from string import Template
from proc.cpu import Cpu
from proc.memory import Memory
from proc.pci import Pci
from proc.fcms import Fcms
from proc.disk import Disk
from proc.system import System

options = {'outlength': 'short', 'get_data_action': 'getData'}
asset_types = ['cpu', 'memory', 'pci', 'fcms', 'disk', 'system']

def main():
        cmds = []
        action = ''
        asset_param = ''
        processed_options = {}
        opt_curr = []
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
        
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hlpc', ['parsable', 'long', 'help', 'get=', 'detail=', 'cached'])
        except getopt.GetoptError, e:
            print "Bad required option"
            help()
            sys.exit(3)

        for o, a in opts:
            if o not in opt_possibilities:
                print "Bad option"
                help()
                sys.exit(2)
                
            processed_options[o] = a
            
        opt_curr = processed_options.keys()
        
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
            
        asset_type = asset_param.title()
        asset = globals()[asset_type]()
        getattr(asset, action)(options)

def help():
    """
    Usage:

    %(program)s <action> <asset_type> <output_type>

    <action> - this is what we want to do with asset_type

            --get - gets info about specified asset_type

    <asset_type> - this is asset_type on which we want to perform action

                   currently you can choose from this asset types:

                   cpu, memory, pci, fcms, disk, system

    <output_type> - this specifies format and length of output

                    currently these are available:

                    default is short output, there is no option for that

                    --l or --long - specifies long output

                    --p or --parsable - is long and parsable output


    Examples:

            This gets information about system in short format:

                systeminfo --get system

            This gets information about disks in long format:

                systeminfo --get disk --l

                or

                systeminfo --get disk --long

            This gets information about fcms HBA's in parsable format:

                        systeminfo --get fcms --p

        Author:

            Pavol Ipoth

        License:

            GPLv3

"""

    print help.__doc__ % {'program': os.path.split(sys.argv[0])[1]}

main()