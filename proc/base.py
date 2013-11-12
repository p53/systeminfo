import io.file
import re
from string import Template
import template.tabletemplate
import ConfigParser
import string
import os
import sys
import copy

class Base:

        def show(self, options):
                config = ConfigParser.ConfigParser()
                config.optionxform = str
                abspath = os.path.dirname(sys.argv[0]) + '/settings/lang-en.conf'
                config.read([abspath])
                headers = dict(config.items(self.__class__.__name__))

                originfo = copy.copy(self.asset_info)
                self.asset_info.insert(0, headers)
                templ_module = self.__class__.__name__.lower() + 'tpl' + options['outlength']
                templ_vars = __import__('view.' + templ_module, globals(), locals(),['tpl'])
                
                templ_header = template.tabletemplate.TableTemplate(self.asset_info, templ_vars.tplh)
                templ_body = template.tabletemplate.TableTemplate(self.asset_info, templ_vars.tpl)
                
                templ_header.tableData = [headers]
                templ_body.tableData = originfo
                
                print templ_header
                print templ_body
