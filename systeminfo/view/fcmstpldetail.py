#!/usr/bin/python

tplh = ""
tpl = """%(pci.vendor|ljust)s
%(linux.sysfs_path|ljust)s
%(nodename|ljust)s
%(portname|ljust)s
%(portstate|ljust)s
%(porttype|ljust)s
%(speed|ljust)s
%(fabricname|ljust)s
%(portid|ljust)s
%(symbolicname|ljust)s
%(supportedclasses|ljust)s
%(supportedspeeds|ljust)s
%(pcicard|ljust)s
%(driver|ljust)s
%(maxnpivvports|ljust)s
%(npivvportsinuse|ljust)s
%(localcpus|ljust)s
%(localcpulist|ljust)s
%(numanode|ljust)s
%(irq|ljust)s"""