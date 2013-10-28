#!/usr/bin/python

import sys
import getopt
import re
from string import Template
from proc.cpu import Cpu
from proc.memory import Memory
from proc.pci import Pci
from proc.fcms import Fcms
from proc.disk import Disk

options = {'outlength': 'short'}
asset_types = ['cpu', 'memory', 'pci', 'fcms', 'disk']

def main():
        cmds = []
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hl', ['long', 'help', 'get='])
        except getopt.GetoptError, e:
            print str(e)
            print args
        for o, a in opts:
            if o in ('l', '--long'):
                options['outlength'] = 'long'
            else:
                cmds.append((o, a))
                
        for o, a in cmds:
                
            if o in ('h', '--help'):
                print 'helping'
            elif o in ('--get'):
                if a in asset_types:
                    asset_type = a.title()
                    asset = globals()[asset_type]()
                    asset.show(options)
            else:
                print "unknow option"
                exit(2)

main()
