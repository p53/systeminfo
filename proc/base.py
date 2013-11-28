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
import cPickle as pickle

class Base:
        
        def getData(self, options):
            pass
            
        def getCache(self, options):
            cache_file = os.path.dirname(sys.argv[0]) + '/cache/' + self.__class__.__name__.lower() + '.cache'
            
            if os.path.exists(cache_file):
                if os.access(cache_file, os.R_OK) and os.path.getsize(cache_file) > 0:
                    cache_file_obj = open(cache_file, 'r')
                    
                    self.asset_info = pickle.load(cache_file_obj)
                    
                    cache_file_obj.close()
                else:
                    self.getData(options)
            else:
                self.getData(options)
                
        def summary(self, options):
            getattr(self, options['get_data_action'])(options)
            self.createCache()
            self.view(options)
        
        def detail(self, options):
            getattr(self, options['get_data_action'])(options)
            instance = options['instance']
            
            for info in self.asset_info:
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
                
                templ_header = globals()[options['template_header_type']](origheader, names, templ_vars.tplh)
                templ_body = globals()[options['template_body_type']](origbody, names, templ_vars.tpl)
                
                if len(templ_vars.tplh) > 0:
                    print templ_header
                
                if len(templ_vars.tpl) > 0:
                    print templ_body
                    
        def createCache(self):
                cache_file = os.path.dirname(sys.argv[0]) + '/cache/' + self.__class__.__name__.lower() + '.cache'
                cache_file_obj = open(cache_file, 'w')
                
                pickle.dump(self.asset_info, cache_file_obj)
                
                cache_file_obj.close()
                