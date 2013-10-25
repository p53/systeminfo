#!/usr/bin/python

import sys
import getopt
import re
from string import Template
import proc.cpu
import proc.memory
import proc.pci
import proc.fcms
import proc.lun

def main():
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'h', ['help', 'get='])
        except getopt.GetoptError, e:
            print str(e)
            print args
        for o, a in opts:
            if o in ('h', '--help'):
                print 'helping'
            elif o in ('--get'):
                if a in ('cpu'):
                    cpu()
                elif a in ('memory'):
                    memory()
                elif a in ('pci'):
                    pci()
                elif a in ('fcms'):
                    fcms()
                elif a in ('lun'):
                    lun()
            else:
                print "unknow option"
                exit(2)

def cpu():
    cpuObj = proc.cpu.Cpu()
    cpuObj.show()

def memory():
    memObj = proc.memory.Memory()
    memObj.show()
        
def pci():
    pciObj = proc.pci.Pci()
    pciObj.show()

def fcms():
    fcmsObj = proc.fcms.Fcms()
    fcmsObj.show()
    
def lun():
    lunObj = proc.lun.Lun()
    lunObj.show()

main()


