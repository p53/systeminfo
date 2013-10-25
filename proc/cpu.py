import io.file
import re
from string import Template
import template.tabletemplate
import ConfigParser
import string
import view.cputpl
import os
import sys

class Cpu:
        cpuinfo = [{}]
        def __init__(self):
                lines = io.file.readFile('/proc/cpuinfo')
                index = 0
                for line in lines:

                        m = re.search('(.*?)\s*:\s*(.*)', line)
                        if m:
                                key = m.group(1)
                                value = m.group(2)
                                p = re.compile('\s+')
                                optim = p.sub('', key)
                                self.cpuinfo[index][optim] = value

                        if re.match('^\n$', line):
                                self.cpuinfo.append({})
                                index = index + 1

        def show(self):
                config = ConfigParser.ConfigParser()
                config.optionxform = str
                abspath = os.path.dirname(sys.argv[0]) + '/settings/lang-en.conf'
                config.read([abspath])
                headers = dict(config.items('CPU'))

                self.cpuinfo.insert(0, headers)

                print template.tabletemplate.TableTemplate(self.cpuinfo, view.cputpl.tpl)


