
__docformat__ = "javadoc"

"""
Module: base.py

Class: Base

Copyright 2013 Pavol Ipoth <pavol.ipoth@gmail.com>

This class is base class for all types of assets

@author: Pavol Ipoth
"""

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
        
        """
            Method: getData
            
            This method gets all info about asset
            
            @param options dict
            @return void
        """
        def getData(self, options):
            pass
            
        """
            Method: getCache
            
            This method checks if there is cache file, if not creates it, if yes get data from it
            
            @param options dict
            @return void
        """
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
         
        """
            Method: summary
            
            This method gets and outputs data about asset type in the list form, always writes cache file
            
            @param options dict
            @return void
        """
        def summary(self, options):
            # get data from cache or fresh one, then create cache, then output
            getattr(self, options['get_data_action'])(options)
            self.createCache()
            self.view(options)
        
        """
            Method: detail
            
            This method gets and outputs data about specified asset type and instance in the detail form
            , it doesn't write cache file!!
            
            @param options dict
            @return void
        """
        def detail(self, options):
            # get data from cache or fresh one, filter out specified instance, output (doesn't create cache file)
            getattr(self, options['get_data_action'])(options)
            instance = options['instance']
            
            for info in self.asset_info:
                if info['toolindex'] == instance:
                    self.asset_info = [info]
                    self.view(options)
                    break
        
        """
            Method: view
            
            This method is the one which is used for formatting output for data and printing
            
            @param options dict
            @return void
        """
        def view(self, options):
                # getting configuration, names of fields
                config = ConfigParser.ConfigParser()
                config.optionxform = str
                abspath = os.path.dirname(sys.argv[0]) + '/settings/lang-en.conf'
                config.read([abspath])
                names = dict(config.items(self.__class__.__name__))
                
                origheader = copy.copy(self.asset_info)
                origbody = copy.copy(self.asset_info)
                
                # creating name of view which will be used, then importing variables with
                # template from view
                templ_module = self.__class__.__name__.lower() + 'tpl' + options['outlength']
                templ_vars = __import__('view.' + templ_module, globals(), locals(),['tpl'])
                
                # this will need to be reworked
                # creating template objects for header, body, processing assigned variables
                templ_header = globals()[options['template_header_type']](origheader, names, templ_vars.tplh)
                templ_body = globals()[options['template_body_type']](origbody, names, templ_vars.tpl)
                
                # printing processed templates
                if len(templ_vars.tplh) > 0:
                    print templ_header
                
                if len(templ_vars.tpl) > 0:
                    print templ_body
                    
        """
            Method createCache
            
            This method creates cache file, pickles data and writes to file
            
            @return void
        """
        def createCache(self):
                cache_file = os.path.dirname(sys.argv[0]) + '/cache/' + self.__class__.__name__.lower() + '.cache'
                cache_file_obj = open(cache_file, 'w')
                
                # pickling asset data
                pickle.dump(self.asset_info, cache_file_obj)
                
                cache_file_obj.close()
                
