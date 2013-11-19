import io.file
import re
from string import Template
import template.tabletemplate
import ConfigParser
import string
import os
import sys
import proc.base

class Cpu(proc.base.Base):
        asset_info = []
        def __init__(self):
                lines = io.file.readFile('/proc/cpuinfo')
                index = 0
                self.asset_info.append({})
                for line in lines:

                        m = re.search('(.*?)\s*:\s*(.*)', line)
                        if m:
                                key = m.group(1)
                                value = m.group(2)
                                p = re.compile('\s+')
                                optim = p.sub('', key)
                                self.asset_info[index][optim] = value

                        if re.match('^\n$', line):
                                self.asset_info.append({})
                                index = index + 1
