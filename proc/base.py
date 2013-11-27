import io.file
import re
from string import Template
from template.tabletemplate import TableTemplate
from template.propertytemplate import PropertyTemplate
from template.voidtemplate import VoidTemplate
from template.headertabletemplate import HeaderTableTemplate
import ConfigParser
import string
import os
import sys
import copy
import pickle

class Base:

        template_header_type = 'HeaderTableTemplate'
        template_body_type = 'TableTemplate'
        
        def getData():
            pass
            
        def show(self, options):
                self.getData()
                self.createCache()
                self.view(options)
        
        def showCache(self, options):
                instance = options['instance']
                self.template_header_type = options['template_header_type']
                self.template_body_type = options['template_body_type']
                
                cache_file = os.path.dirname(sys.argv[0]) + '/cache/' + self.__class__.__name__.lower() + '.cache'
                cache_file_obj = open(cache_file, 'r')
                
                cached_info = pickle.load(cache_file_obj)
                
                cache_file_obj.close()
                
                for info in cached_info:
                    if info['toolindex'] == instance:
                        self.asset_info = [info]
                        self.view(options)
                        break
                
        def view(self, options):
                config = ConfigParser.ConfigParser()
                config.optionxform = str
                abspath = os.path.dirname(sys.argv[0]) + '/settings/lang-en.conf'
                config.read([abspath])
                names = dict(config.items(self.__class__.__name__))
                
                origheader = copy.copy(self.asset_info)
                origbody = copy.copy(self.asset_info)

                templ_module = self.__class__.__name__.lower() + 'tpl' + options['outlength']
                templ_vars = __import__('view.' + templ_module, globals(), locals(),['tpl'])
                
                templ_header = globals()[self.template_header_type](origheader, names, templ_vars.tplh)
                templ_body = globals()[self.template_body_type](origbody, names, templ_vars.tpl)
                
                if len(templ_vars.tplh) > 0:
                    print templ_header
                
                if len(templ_vars.tpl) > 0:
                    print templ_body
                    
        def createCache(self):
                cache_file = os.path.dirname(sys.argv[0]) + '/cache/' + self.__class__.__name__.lower() + '.cache'
                cache_file_obj = open(cache_file, 'w')
                
                pickle.dump(self.asset_info, cache_file_obj)
                
                cache_file_obj.close()
                