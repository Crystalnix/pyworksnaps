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

import urllib
import urllib2

from xml.etree import cElementTree

from worksnaps.exceptions import *
from worksnaps.auth import BasicAuth
from worksnaps.utils import convert_xml_to_dict, convert_dict_to_xml

errors = { 400: HTTP400BadRequestError,
           401: HTTP401UnauthorizedError,
           403: HTTP403ForbiddenError,
           404: HTTP404NotFoundError,
           422: HTTP422UnprocessableEntityError,
           500: HTTP500ServerError }

def raise_http_error(e):
    '''Raise custom exception'''
    http_error_class = errors.get(e.code)
    message = e.fp.read() or e.msg
    if http_error_class:
        raise http_error_class(e.filename, e.code, message, e.hdrs, None)
    else:
        raise e

class BaseClient(object):
    """
    """

    def __init__(self, public_key, secret_key = ''):
        self.public_key = public_key
        self.secret_key = secret_key
        self.auth = None

    def data_encode(self, data={}, format=None):
        assert format == 'xml', "Only XML format is supported at the moment"
        data = data.copy()
        root_tag = data.pop('root_tag', '')
        if data and format == 'xml':
            # root_tag is a small hack to get name of root element in xml
            return convert_dict_to_xml(root_tag, data)
        else:
            return urllib.urlencode(data)

    def urlopen(self, url, query={}, data={}, method='GET', headers={}):
        self.last_method = method
        self.last_url = url
        self.last_data = data

        if query:
            url = '%s?%s' % (url, urllib.urlencode(query))

        if method == 'GET':
            data = None
        request = self.auth.create_request(url=url, data=data, method=method, headers=headers)
        return urllib2.urlopen(request)

    def fetch(self, url, query={}, data={}, method='GET', format='xml'):
        """
        Returns parsed Python object or raises an error
        """
        assert format == 'xml', "Only XML format is supported at the moment"
        url += '.' + format
        try:
            headers = {'Content-Type': 'application/%s' % format}
            response = self.urlopen(url, query, self.data_encode(data, format), method, headers)
        except urllib2.HTTPError, e:
            raise_http_error(e)

        if format == 'xml':
            result = convert_xml_to_dict( response )
        return result

class Client(BaseClient):
    """
    Main API client
    """

    def __init__(self, public_key, secret_key = '',
                 #oauth_access_token=None, oauth_access_token_secret=None, # it's here for future
                 format='xml', auth='base'):

        super(Client, self).__init__(public_key, secret_key)
        self.format = format

        if auth == 'base':
            self.auth = BasicAuth(username = public_key, password = secret_key)

        from worksnaps.parts.users import Users
        from worksnaps.parts.projects import Projects
        from worksnaps.parts.time_entries import Time
        from worksnaps.parts.assignments import Assignments

        self.time = Time(self)
        self.users = Users(self)
        self.projects = Projects(self)
        self.assignments = Assignments(self)

    #Shortcuts for HTTP methods
    def get(self, url, query={}, data = {}):
        return self.fetch(url, query, data, method = 'GET', format = self.format)

    def post(self, url, query={}, data = {}):
        return self.fetch(url, query, data, method = 'POST', format = self.format)

    def put(self, url, query={}, data = {}):
        return self.fetch(url, query, data, method = 'PUT', format = self.format)

    def delete(self, url, query={}, data = {}):
        return self.fetch(url, query, data, method = 'DELETE', format = self.format)
