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
Module: template.py

Class: Template

This class processes template string
It is used for generating body of table output

@author: Pavol Ipoth
@license: GPLv3+
@copyright: Copyright 2013 Pavol Ipoth
@contact: pavol.ipoth@gmail.com

"""

from jinja2 import Environment, FileSystemLoader, ModuleLoader, exceptions

class Template():

        _iteration = 0
        """
        @type: int
        @ivar: holds index for iterating over items
        """

        _maxInfo = {}
        """
        @type: dict
        @ivar: holds maximum length for each column
        """
        _property_names = {}
        """
        @type: dict
        @ivar: holds names for each property
        """

        def render(self, templ_path, templ_name, cached_path):
            templ_compiled_path = cached_path
            template = ''
            
            JINJA_ENVIRONMENT = Environment(
                loader=ModuleLoader(templ_compiled_path),
                autoescape=False
            )
            
            try:
                template = JINJA_ENVIRONMENT.get_template(templ_name)
            except exceptions.TemplateNotFound:
                JINJA_COMPILE_ENVIRONMENT = Environment(
                   loader=FileSystemLoader(templ_path),
                   autoescape=False
                )
                
                JINJA_COMPILE_ENVIRONMENT.compile_templates(
                    templ_compiled_path, 
                    zip=None
                )
                
                template = JINJA_ENVIRONMENT.get_template(templ_name)

            template_values = {
                'data': self.tableData,
                'maxInfo': self._maxInfo,
                'properties': self._property_names
            }

            print template.render(template_values)