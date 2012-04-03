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

class Namespace(object):
    """
    A special 'proxy' class to keep API methods organized
    """

    base_url = 'http://worksnaps.net/api'
    api_url = None
    root_tag = None

    def __init__(self, client):
        self.client = client

    def full_url(self, url = None):
        """
        Gets relative URL of API method and returns a full URL
        """
        return "%s%s/%s" % (self.base_url, self.api_url, url) if url else "%s%s" % (self.base_url, self.api_url)

    #Proxied client's methods
    def get(self, url = None, query = {}, data={}):
        return self.client.get(self.full_url(url), query, data)

    def post(self, url = None, query = {}, data={}):
        data['root_tag'] = self.root_tag
        return self.client.post(self.full_url(url), query, data)

    def put(self, url = None, query = {}, data={}):
        data['root_tag'] = self.root_tag
        return self.client.put(self.full_url(url), query, data)

    def delete(self, url = None, query = {}, data={}):
        return self.client.delete(self.full_url(url), query, data)