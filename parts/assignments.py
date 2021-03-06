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

class Assignments(Namespace):
    api_url = '/projects'
    root_tag = 'user_assignment'

    def get_project_assignments(self, project_id):
        url = '%s/user_assignments' % project_id
        result = self.get(url)
        result = result['user_assignments']['user_assignment']
        return result if isinstance(result, list) else [result, ]