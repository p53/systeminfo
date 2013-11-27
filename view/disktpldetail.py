#!/usr/bin/python

tplh = ""
tpl = """%(device|ljust)s
%(targetport|ljust)s
%(lunid|ljust)s
%(id|ljust)s
%(vendor|ljust)s
%(model|ljust)s
%(size|ljust)s
%(hwpath|ljust)s
%(srcport|ljust)s
%(rportstate|ljust)s"""