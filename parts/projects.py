#-*- coding: utf-8 -*-
"""
    Python bindings to worksnaps API
    Copyright (C) 2012  Crystalnix company

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = 'Kirill Yakovenko, kirill.yakovenko@gmail.com'

from worksnaps.namespace import Namespace

class Projects(Namespace):
    api_url = '/projects'
    root_tag = 'project'

    def get_projects(self):
        result = self.get()
        if result['projects']:
            result = result['projects']['project']
            if isinstance(result, list):
                return result
            else:
                return [result, ]
        else:
            return None

    def get_project(self, id):
        result = self.get( str(id) )
        return result['project']

    def update_project(self, id, **kwargs):
        result = self.put( str(id), data=kwargs)
        return result['reply']['project']

    def create_project(self, name, description = ''):
        result = self.post(data = {'name': name, 'description': description})
        return result['reply']['project']

    def delete_project(self, id):
        result = self.delete(str(id))
        return result['reply']['status'] == '1'
