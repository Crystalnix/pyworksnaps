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

class Users(Namespace):
    api_url = '/users'
    root_tag = 'user'

    def get_me(self):
        url = '/me'
        result = self.client.get('%s%s' % (self.base_url, url) )
        return result['user']

    def get_user(self, id):
        result = self.get(str(id))
        return result['user']

    def update_user(self, id, **kwargs):
        result = self.put(url = str(id), data = kwargs)
        return result['reply']['user']

    def create_user(self, login, email, password, first_name = '', last_name = '', timezone = 0):
        d = { 'login'      : login,
              'first_name' : first_name,
              'last_name'  : last_name,
              'password'   : password,
              'email'      : email,
              'timezone_id': timezone }
        result = self.post(data = d)
        return result['user']
