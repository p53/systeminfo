#!/usr/bin/python

tplh = ""
tpl = """%(pci.vendor)s#%(pcicard)s#%(portname)s#%(porttype)s#%(portstate)s#%(speed)s#%(linux.sysfs_path)s#%(nodename)s#%(fabricname)s#%(portid)s#%(symbolicname)s#%(supportedclasses)s#%(supportedspeeds)s#%(driver)s#%(maxnpivvports)s#%(npivvportsinuse)s#%(localcpus)s#%(localcpulist)s#%(numanode)s#%(irq)s
"""