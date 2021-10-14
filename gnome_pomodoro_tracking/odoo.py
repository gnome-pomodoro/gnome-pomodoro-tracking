# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import xmlrpc.client
from urllib.parse import urlparse
import configparser
from datetime import datetime

from gnome_pomodoro_tracking.plugin import Plugin
from gnome_pomodoro_tracking.utils import printtbl, join_url, find_by_id, config_attrs

class Odoo(Plugin):

    name = "odoo"

    def __init__(self, gpt):
        super().__init__(gpt)

    def setup(self):
        try:
            self.session.update({
                "username": self.gpt.get_config(self.name, "username"),
                "password": self.gpt.get_config(self.name, "password"),
                "url": self.gpt.get_config(self.name, "url"),
                "database": self.gpt.get_config(self.name, "database"),
            })

            if not self.auth():
                raise Exception("Fail auth check credentials")
        except configparser.NoSectionError as e:
            self.gpt.logger.error(e)
            self.gpt.add_section_config(self.name)            
        except configparser.NoOptionError as e:
            self.gpt.logger.error(e)

    def add_parse_args(self, kind):
        
        self.gpt.parse.add_argument('-p','--projects',
                                        action='store_const',
                                        dest='odoo_projects',
                                        help='List projects',
                                        const=True)
        self.gpt.parse.add_argument('-t','--tasks',
                                        action='store_const',
                                        dest='odoo_tasks',
                                        help='List tasks',
                                        const=True)
        self.gpt.parse.add_argument('--username',  
                                    action='store',
                                    dest='odoo_username')
        self.gpt.parse.add_argument('--password',
                                    action='store',
                                    dest='odoo_password')        
        self.gpt.parse.add_argument('--database',
                                    action='store',
                                    dest='odoo_database')
        self.gpt.parse.add_argument('--url',
                                    action='store',
                                    dest='odoo_url')
    def auth(self):
        up = urlparse(self.session.get('url'))
        url = '{}://{}'.format( up.scheme or 'https', up.netloc)
        self.session.update({"url": url})
        uid = self.common().authenticate(
            self.session.get('database'),
            self.session.get('username'),
            self.session.get('password'), {})
        self.session.update({"uid": uid})
        return self.session.get("uid", "") != ""

    # Odoo operations
    def version(self):
        return self.common().version().get('server_version')

    def common(self):
        return xmlrpc.client.ServerProxy(join_url(self.session.get("url", ""), 'xmlrpc/2/common'))

    def models(self, model, method, domain, options=False):
        if not self.session.get("uid"):
            return False
        x = xmlrpc.client.ServerProxy( join_url(self.session.get("url"), 'xmlrpc/2/object'))
        return x.execute_kw(
            self.session.get("database"),
            self.session.get("uid"),
            self.session.get("password"),
            model, method, domain, options)

    def cli(self, **kwargs):
        # Overwrite
        params = self.gpt.parse.parse_args()
        
        if hasattr(params, 'odoo_username') and params.odoo_username and \
            hasattr(params, 'odoo_password') and params.odoo_password and \
            hasattr(params, 'odoo_url') and params.odoo_url and \
            hasattr(params, 'odoo_database') and params.odoo_database:
                self.session.update({
                    "username": params.odoo_username,
                    "password": params.odoo_password,
                    "url":  params.odoo_url,
                    "database": params.odoo_database})
                if self.auth():
                    for p in ['username', 'password', 'url', 'database']:
                        self.gpt.set_config(self.name, p, self.session.get(p))
                else:
                    print("Fail auth check your username/password/url/database!")
                    exit(0)
            

        if hasattr(params, 'odoo_projects') and params.odoo_projects:
            try:
                rows = self.projects()
                if params.set:
                    row = find_by_id(rows, params.set)
                    if row:
                        self.gpt.set_config(self.name, "project_id", row.get('id'))
                        self.gpt.set_config(self.name, "project_name", row.get('name'))
                        self.gpt.set_config(self.name, "task_id", "")
                        self.gpt.set_config(self.name, "task_name", "")
                        printtbl([row])
                    else:
                        print('The project ID was not found')
                else:
                    printtbl(rows)
            except Exception as e:
                self.gpt.logger.exception(e)
        elif hasattr(params, 'odoo_tasks') and params.odoo_tasks:
            try:
                rows = self.tasks()
                if params.set:
                    row = find_by_id(rows, params.set)
                    if row:
                        self.gpt.set_config(self.name, "task_id", row.get('id'))
                        self.gpt.set_config(self.name, "task_name", row.get('name'))
                        self.gpt.set_config(self.name, "project_id", row.get('project_id'))
                        self.gpt.set_config(self.name, "project_name", row.get('project_name'))
                        printtbl([row])
                    else:
                        print('The task ID was not found')
                else:
                    printtbl(rows)
            except Exception as e:
                self.gpt.logger.exception(e)

    def data_order(self, rows):
        nrows = []
        for row in rows:
            nrows.append(dict(sorted(row.items(), key=lambda c: str(c[1]))))
        return len(nrows) and nrows or rows

    def projects(self):
        projects = self.models('project.project', 'search_read', [[['active', '=', True]]], {'fields': ['id', 'name']})
        projects = self.data_order(projects)
        self.gpt.logger.info(projects)
        return projects

    def tasks(self):
        project_id = self.gpt.get_config(self.name, "project_id")
        if project_id and project_id.isdigit():
            domain = [[['active', '=', True], ['project_id', '=', int(project_id)]]]
        else:
            domain = [[['active', '=', True]]]
        tasks = self.models('project.task', 'search_read', domain, {'fields': ['id', 'name', 'project_id' ]})
        tasks = self.data_order(tasks)
        if len(tasks):
            ntasks = []
            for t in tasks:
                tb = t.pop('project_id')
                ntasks.append({**t, 'project_id': tb[0],  'project_name': tb[1]})
            tasks = ntasks
        self.gpt.logger.info(tasks)
        return tasks

    def add_time_entry(self, **kwargs):
        # Overwrite
        description = kwargs.get('name')
        dt_start = kwargs.get('start')
        dt_end = kwargs.get('end')
        minutes = float(kwargs.get('minutes', 0))
        name = description
        try:
            project_id = int(self.gpt.get_config(self.name, "project_id"))
            if project_id > 0:
                task_id = self.gpt.get_config(self.name, "task_id")
                task_id = int(task_id) if task_id and task_id.isdigit() else False
                id = self.models('account.analytic.line', 'create', [{
                    'date': datetime.now().strftime("%Y-%m-%d"),  # Required
                    'name': name,  # Required
                    'project_id': project_id,  # Required
                    'task_id': task_id,
                    'unit_amount': minutes / 60 }])
                self.gpt.logger.info(id)
                return {'id': id, 'name': name}
            else:
                raise Exception("First select the project  --odoo-projects --set ID")
        except Exception as e:
            self.gpt.logger.exception(e)
        return None

    # Optional params
    def status(self, **kwargs):
        attrs = ['project_name', 'task_name']
        items = config_attrs(self.gpt, self.name, attrs, formatter='status')
        printtbl(items)
