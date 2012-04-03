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

__ALL__ = [
            'HTTP400BadRequestError',
            'HTTP401UnauthorizedError',
            'HTTP403ForbiddenError',
            'HTTP404NotFoundError',
            'HTTP422UnprocessableEntityError',
            'HTTP500ServerError'
          ]

import logging
import urllib2

class BaseException(Exception):
    def __init__(self, *args, **kwargs):
        logging.debug("[python-worksnaps]:" + unicode(s) for s in args)
        super(BaseException, self).__init__()

class HTTP400BadRequestError(urllib2.HTTPError, BaseException):
    pass

class HTTP401UnauthorizedError(urllib2.HTTPError, BaseException):
    pass

class HTTP403ForbiddenError(urllib2.HTTPError, BaseException):
    pass

class HTTP404NotFoundError(urllib2.HTTPError, BaseException):
    pass

class HTTP422UnprocessableEntityError(urllib2.HTTPError, BaseException):
    pass

class HTTP500ServerError(urllib2.HTTPError, BaseException):
    pass

class AuthenticationError(BaseException):
    pass