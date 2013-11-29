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

options = {'outlength': 'short'}
asset_types = ['cpu', 'memory', 'pci', 'fcms', 'disk', 'system']

def main():
        cmds = []
        action = ''
        asset_param = ''
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hlp', ['parsable', 'long', 'help', 'get='])
        except getopt.GetoptError, e:
            print "Bad required option"
            help()
            sys.exit(3)

        for o, a in opts:
            if o in ('l', '--long'):
                options['outlength'] = 'long'
            elif o in ('p', '--parsable'):
                options['outlength'] = 'parsable'
            elif o in ('h', '--help'):
                help()
                sys.exit()
            elif o in ('--get') and a in asset_types:
                action = 'show'
                asset_param = a
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