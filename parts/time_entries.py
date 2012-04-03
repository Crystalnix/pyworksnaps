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

import time
from worksnaps.namespace import Namespace

class Time(Namespace):
    api_url = '/projects'
    root_tag = 'time_entry'

    @staticmethod
    def __get_url(project_id, entry_id):
        return '%s/time_entries/%s' % (project_id, entry_id)

    def get_time_entry(self, project, entry):
        result = self.get( self.__get_url(project, entry) )
        return result['time_entry']

    def get_user_time_entries(self, project, user, from_datetime, to_datetime, only_online = None):
        url = '%s/users/%s/time_entries' % (project, user)
        query = { 'from_timestamp': time.mktime(from_datetime.timetuple()),
                  'to_timestamp'  : time.mktime(to_datetime.timetuple()), }
        if only_online is not None:
            query['time_entry_type'] = 'online' if only_online else 'offline'
        result = self.get(url, query)
        result = result['time_entries']
        return result['time_entry'] if result else []

    def update_time_entry(self, project, entry, task, user_comment):
        result = self.put( self.__get_url(project, entry), data = {'task_id': task, 'user_comment': user_comment} )
        return result['reply']['time_entry']

    def get_screenshots(self, project, entry):
        result = self.get( self.__get_url(project, entry), {'full_resolution_url': 1} )
        return result['time_entry']