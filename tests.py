#!/usr/bin/env python
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

import unittest

import os, sys

sys.path.append(os.path.realpath( os.path.join(os.path.dirname(__file__), '..') ))

from worksnaps.client import Client

token = ''
if not token:
    raise Exception('Token must be set up.')

class UsersTest(unittest.TestCase):

    user_info = {'login': '123login123',
                 'email': 'test@test.com',
                 'password': 'password',
                 'first_name': 'First name'}

    def setUp(self):
        self.client = Client(token)

    def test_me(self):
        me = self.client.users.get_me()
        self.assertTrue( isinstance(me, dict) )

    def test_user(self):
        me = self.client.users.get_me()
        user = self.client.users.get_user(me['id'])
        self.assertTrue( isinstance(user, dict) )

    def test_update_user(self):
        me = self.client.users.get_me()
        user = self.client.users.update_user(me['id'], **self.user_info)
        self.assertEqual(user['login'], self.user_info['login'])
        self.assertEqual(user['email'], self.user_info['email'])
        self.assertEqual(user['first_name'], self.user_info['first_name'])
        #back
        self.user_info['login'] = me['login']
        self.user_info['email'] = me['email']
        user = self.client.users.update_user(me['id'], **self.user_info)
        self.assertTrue( user )

#    def test_create_user(self):
#        user_info = {'login': 'test_login',
#                     'email': 'test@test.com',
#                     'password': 'password',
#                     'first_name': 'First name'}
#        m = self.client.users.create_user(**user_info)
#        self.assertTrue( m['id'] )
#        self.assertEqual( m['login'], user_info['login'] )
#        self.assertEqual( m['email'], user_info['email'] )
#        self.assertEqual( m['password'], user_info['password'] )
#        self.assertEqual( m['first_name'], user_info['first_name'] )
#        self.assertEqual( m['last_name'], user_info['last_name'] )

new_project = None
class ProjectsTest(unittest.TestCase):
    project_info = {'name': 'Test project2', 'description': 'Empty description2'}

    def setUp(self):
        self.client = Client(token)

    def test_projects(self):
        prs = self.client.projects.get_projects()
        self.assertTrue( isinstance(prs, list) )

    def test_get_project(self):
        prs = self.client.projects.get_projects()
        if prs:
            project = self.client.projects.get_project(prs[0]['id'])
            self.assertTrue( project )
        else:
            self.fail("There is no project.")

    def test_update_project(self):
        prs = self.client.projects.get_projects()
        id = prs[0]['id']
        project = self.client.projects.update_project(id, **self.project_info)
        self.assertTrue( isinstance(project, dict) )
        self.assertEqual( project['id'], str(id) )
        self.assertEqual( project['name'], self.project_info['name'] )
        self.assertEqual( project['description'], self.project_info['description'] )

    def test_create_project(self):
        global new_project
        new_project = self.client.projects.create_project(**self.project_info)
        self.assertTrue( isinstance(new_project, dict) )
        self.assertTrue( new_project.has_key('id') )
        self.assertEqual( new_project['name'], self.project_info['name'] )
        self.assertEqual( new_project['description'], self.project_info['description'] )

    def test_delete_project(self):
        global new_project
        if new_project:
            self.client.projects.delete_project(new_project['id'])

class TimeEntriesTest(unittest.TestCase):

    def setUp(self):
        self.client = Client(token)

    def test_user_time_entries(self):
        from datetime import date, timedelta
        me = self.client.users.get_me()
        prs = self.client.projects.get_projects()
        project_id = prs[0]['id']
        entries = self.client.time.get_user_time_entries(project_id, me['id'], date.today(), date.today() + timedelta(days=1))
        self.assertTrue( isinstance(entries, list) )
        id = entries[0]['id']
        # get time entry
        entry = self.client.time.get_time_entry(project_id, id)
        self.assertEqual( entry['id'], str(id) )
        # get screenshots
        entry = self.client.time.get_screenshots(project_id, id)
        self.assertTrue( entry )
        # update time entry
        entry_info = {'task' : 0, 'user_comment': "comment from api"}
        entry = self.client.time.update_time_entry(project_id, id, **entry_info)
        self.assertEqual( entry['id'], id )
        self.assertEqual( entry['task'], entry_info['task'] )
        self.assertEqual( entry['user_comment'], entry_info['user_comment'] )

class AssignmentsTest(unittest.TestCase):

    def setUp(self):
        self.client = Client(token)

    def test_get_assignments(self):
        prs = self.client.projects.get_projects()
        if prs:
            assignments = self.client.assignments.get_project_assignments( prs[0]['id'] )
            self.assertTrue( isinstance(assignments, list) )
        else:
            self.fail("There is no project.")

if __name__ == '__main__':
    unittest.main()
