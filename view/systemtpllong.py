#!/usr/bin/python

tpl = """%(SystemManufacturer|ljust)s
%(SystemSerialNumber|ljust)s
%(SystemProductName|ljust)s
%(SystemUUID|ljust)s
%(ChassisManufacturer|ljust)s
%(ChassisSerialNumber|ljust)s
%(load|ljust)s
%(machinetype|ljust)s
%(nodename|ljust)s
%(osrelease|ljust)s
%(osname|ljust)s
%(osversion|ljust)s
%(distname|ljust)s
%(distver|ljust)s
%(distid|ljust)s
%(OSCoreCount|ljust)s
%(OSCoreEnabled|ljust)s
%(OSThreadCount|ljust)s
%(OSPhyscpuCount|ljust)s
%(MemoryMemTotal|ljust)s
%(MemoryMemFree|ljust)s
%(MemorySwapTotal|ljust)s
%(MemorySwapFree|ljust)s
%(MemoryShmem|ljust)s
%(MemoryHardwareCorrupted|ljust)s"""

