# Systeminfo - Simple utility for gathering hardware summary information
# Copyright (C) 2013, 2014  Pavol Ipoth  <pavol.ipoth@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# -*- coding: utf-8 -*-

"""
Module: base.py

Class: Base

This class is base class for all types of assets

@author: Pavol Ipoth
@license: GPLv3+
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

import systeminfo.io.file
from systeminfo.template.tabletemplate import TableTemplate
from systeminfo.template.propertytemplateall import PropertyTemplateAll
import ConfigParser
import os
import sys
import copy
import cPickle as pickle

class Base(object):

        cacheDir = ""
        """
        @type: string
        @ivar: Holds cache files directory
        """

        confDir = ""
        """
        @type: string
        @ivar: Holds configuration files directory
        """
        
        def __init__(self, configDir, cachingDir, viewDir):
            """
            Method: __init__
            
            method initializies all device objects
            
            @rtype void
            """
            self.confDir = configDir
            self.cacheDir = cachingDir
            self.viewDir = viewDir
            
        def getData(self, options):
            """
            Method: getData

            This method gets all info about asset

            @type options: dict
            @param options: passed options
            @rtype: void
            """
            pass

        def getCache(self, options):
            """
            Method: getCache

            This method checks if there is cache file, if not creates it, if yes get data from it

            @type options: dict
            @param options: passed options
            @rtype: void
            """

            cache_file = Base.cacheDir + self.__class__.__name__.lower() + '.cache'

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
            """
            Method: summary

            This method gets and outputs data about asset type in the list form, always writes cache file

            @type options: dict
            @param options: passed options
            @rtype: void
            """

            # get data from cache or fresh one, then create cache, then output
            getattr(self, options['get_data_action'])(options)
            self.createCache()
            self.view(options)

        def detail(self, options):
            """
            Method: detail

            This method gets and outputs data about specified asset type and instance in the detail form
            , it doesn't write cache file!!

            @type options: dict
            @param options: passed options
            @rtype: void
            """

            # get data from cache or fresh one, filter out specified instance, output (doesn't create cache file)
            getattr(self, options['get_data_action'])(options)
            instance = options['instance']

            for info in self.asset_info:
                if info['toolindex'] == instance:
                    self.asset_info = [info]
                    self.view(options)
                    break

        def view(self, options):
            """
            Method: view

            This method is the one which is used for formatting output for data and printing

            @type options: dict
            @param options: passed options
            @rtype: void
            """

            # getting configuration, names of fields
            config = ConfigParser.ConfigParser()
            config.optionxform = str
            abspath = self.confDir + 'lang-en.conf'
            config.read([abspath])
            names = dict(config.items(self.__class__.__name__))

            origbody = copy.copy(self.asset_info)

            # creating name of view which will be used, then importing variables with
            # template from view
            templ_name = self.__class__.__name__.lower() + 'tpl' + options['outlength'] + '.j2'

            templ_path = os.path.abspath(self.viewDir)
            templ_object = globals()[options['template_body_type']](origbody, names)

            cached_path = self.cacheDir + 'view/compiled'
            templ_object.render(templ_path, templ_name, cached_path)

        def createCache(self):
            """
            Method createCache

            This method creates cache file, pickles data and writes to file

            @rtype: void
            """

            cache_file = self.cacheDir + self.__class__.__name__.lower() + '.cache'
            cache_file_obj = open(cache_file, 'w+')

            # pickling asset data
            pickle.dump(self.asset_info, cache_file_obj)

            cache_file_obj.close()
        
        def createCustomCache(self, cacheName, cachedData):
            """
            Method: createCustomCache
            
            method creates cache with specified name and with provided data
            
            @type cacheName: str
            @param cacheName: specifies name from which we will construct cache file name
            @type cachedData: dict
            @param cachedData: data which we want to store in cache
            @rtype void
            """
            if not cacheName:
                print 'You forgot to supply cache name!'
                raise Exception('Missing name')
                
            cache_file = self.cacheDir + cacheName.lower() + '.cache'
            cache_file_obj = open(cache_file, 'w')

            # pickling custom data
            pickle.dump(cachedData, cache_file_obj)

            cache_file_obj.close()
        
        def getCustomCache(self, cacheName):
            """
            Method: getCustonCache

            This method checks if there is cache file and gets data if possible

            @type cacheName: str
            @param cacheName: name of file which should be used for construction of file name of cache
            @rtype: dict
            """
            cachedData = {}           
            cache_file = self.cacheDir + cacheName + '.cache'

            if os.path.exists(cache_file):
                if os.access(cache_file, os.R_OK) and os.path.getsize(cache_file) > 0:
                    cache_file_obj = open(cache_file, 'r')
                    cachedData = pickle.load(cache_file_obj)
                    cache_file_obj.close()

            return cachedData
                                
        def setCacheDir(self, dir_location):
            """
            Method setCacheDir

            This method sets the dir for saving cache files

            @type dir_location: string
            @param dir_location: location of cache files directory
            @rtype: void
            """

            if not dir_location:
                raise Exception("Cannot set empty cache directory location!")

            if not os.path.isdir(dir_location):
                raise Exception("Supplied cache directory: " + dir_location + " doesn't exist!")

            self.cacheDir = dir_location

        def setConfDir(self, dir_location):
            """
            Method setConfDir

            This methos sets the dir for configuration files

            @type dir_location: string
            @param dir_location: location of configuration directory
            @rtype: void
            """

            if not dir_location:
                raise Exception("Cannot set empty config directory location!")

            if not os.path.isdir(dir_location):
                raise Exception("Supplied config directory: " + dir_location + " doesn't exist!")


            self.confDir = dir_location
