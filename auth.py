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

import base64
import urllib2
from worksnaps.exceptions import AuthenticationError

class BasicAuth(object):

    api_url = 'auth/'

    def __init__(self, username, password = ''):
        if username:
            self.__base64string = base64.encodestring('%s:%s' % (username, password))[:-1]

    def create_request(self, url, method, headers={}, data = None):
        headers.update({ "Authorization": "Basic %s" % self.__base64string })
        request = urllib2.Request(url, data, headers=headers)
        request.get_method = lambda: method
        return request