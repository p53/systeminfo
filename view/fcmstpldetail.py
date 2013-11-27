#!/usr/bin/python

tplh = ""
tpl = """%(pci.vendor|ljust)s
%(linux.sysfs_path|ljust)s
%(nodename|ljust)s
%(portname|ljust)s
%(portstate|ljust)s
%(porttype|ljust)s
%(speed|ljust)s
%(pcicard|ljust)s"""