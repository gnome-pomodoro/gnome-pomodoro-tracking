# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import xmlrpc.client
from urllib.parse import urlparse
import configparser
from datetime import datetime

from .gpt_plugin import GPTPlugin
from .gpt_utils import printtbl, println, join_url, printlg

class Odoo(GPTPlugin):

    name = "odoo"

    def __init__(self, gpt):
        super().__init__(gpt)

    def setup(self):
        try:
            self.session.update({
                "username": self.gpt.gptconfig_get(self.name, "username"),
                "password": self.gpt.gptconfig_get(self.name, "password"),
                "url": self.gpt.gptconfig_get(self.name, "url"),
                "database": self.gpt.gptconfig_get(self.name, "database"),
            })

            if not self.auth():
                raise Exception("Fail auth check credentials")
        except configparser.NoSectionError as e:
            printlg(error=e)
            self.gpt.gptconfig_set_section(self.name)
            self.add_parse_args("setup-args")
        except configparser.NoOptionError as e:
            printlg(error=e)
            self.add_parse_args("setup-args")
            params = self.gpt.gptparse_params()
            try:
                self.session.update({
                    "username": params.odoo_username,
                    "password": params.odoo_password,
                    "url":  params.odoo_url,
                    "database": params.odoo_database})
                if self.auth():
                    for p in ['username', 'password', 'url', 'database']:
                        self.gpt.gptconfig_set(self.name, p, self.session.get(p))
                    print(f"{self.name} now can do you use.")
            except Exception as e:
                printlg(exception=e)

    def add_parse_args(self, kind):
        if kind == "setup-args":
            self.gpt.parse.add_argument('--odoo-username',
                                        action='store',
                                        dest='odoo_username',
                                        required=True)
            self.gpt.parse.add_argument('--odoo-password',
                                        action='store',
                                        dest='odoo_password',
                                        required=True)
            self.gpt.parse.add_argument('--odoo-url',
                                        action='store',
                                        dest='odoo_url',
                                        required=True)
            self.gpt.parse.add_argument('--odoo-database',
                                        action='store',
                                        dest='odoo_database',
                                        required=True)

        else:
            # Overwrite
            self.gpt.parse.add_argument('--odoo-projects',
                                        action='store_const',
                                        dest='odoo_projects',
                                        help='Odoo projects',
                                        const=True)
            self.gpt.parse.add_argument('--odoo-tasks',
                                        action='store_const',
                                        dest='odoo_tasks',
                                        help='Odoo projects/tasks',
                                        const=True)

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
        params = self.gpt.gptparse_params()

        def findbyid(rows, id):
            for row in rows:
                for k in row.keys():
                    if k == 'id' and row.get(k) == id:
                        return row
            return None

        if params.odoo_projects:
            try:
                rows = self.projects()
                if params.set:
                    row = findbyid(rows, int(params.set))
                    if row:
                        self.gpt.gptconfig_set(self.name, "project_id", row.get('id'))
                        self.gpt.gptconfig_set(self.name, "project_name", row.get('name'))
                        self.gpt.gptconfig_set(self.name, "task_id", "")
                        self.gpt.gptconfig_set(self.name, "task_name", "")
                        printtbl([row])
                    else:
                        println('The project ID was not found')
                else:
                    printtbl(rows)
            except Exception as e:
                printlg(exception=e)
        elif params.odoo_tasks:
            try:
                rows = self.tasks()
                if params.set:
                    row = findbyid(rows, int(params.set))
                    if row:
                        self.gpt.gptconfig_set(self.name, "task_id", row.get('id'))
                        self.gpt.gptconfig_set(self.name, "task_name", row.get('name'))
                        self.gpt.gptconfig_set(self.name, "project_id", row.get('project_id'))
                        self.gpt.gptconfig_set(self.name, "project_name", row.get('project_name'))
                        printtbl([row])
                    else:
                        println('The task ID was not found')
                else:
                    printtbl(rows)
            except Exception as e:
                printlg(exception=e)

    def projects(self):
        projects = self.models('project.project', 'search_read', [[['active', '=', True]]], {'fields': ['id', 'name']})
        return projects

    def tasks(self, project_id=None):
        if project_id:
            domain = [[['active', '=', True], ['project_id', '=', int(project_id)]]]
        else:
            domain = [[['active', '=', True]]]
        tasks = self.models('project.task', 'search_read', domain, {'fields': ['id', 'name', 'project_id' ]})
        if len(tasks):
            ntasks = []
            for t in tasks:
                tb = t.pop('project_id')
                ntasks.append({**t, 'project_id': tb[0],  'project_name': tb[1]})
            tasks = ntasks

        return tasks

    def add_time_entry(self, **kwargs):
        # Overwrite
        description = kwargs.get('name')
        dt_start = kwargs.get('start')
        dt_end = kwargs.get('end')
        minutes = float(kwargs.get('minutes', 0))
        name = "%s - DTS:%s DTE:%s" % (description, dt_start, dt_end)
        try:
            project_id = int(self.gpt.gptconfig_get(self.name, "project_id"))
            if project_id > 0:
                task_id = self.gpt.gptconfig_get(self.name, "task_id")
                task_id = int(task_id) if len(task_id) else False
                id = self.models('account.analytic.line', 'create', [{
                    'date': datetime.now().strftime("%Y-%m-%d"),  # Required
                    'name': name,  # Required
                    'project_id': project_id,  # Required
                    'task_id': task_id,
                    'unit_amount': minutes / 60 }])
                return id
            else:
                raise Exception("First select the project  --odoo-projects --set ID")
        except Exception as e:
            printlg(exception=e)
        return False

    # Optional params
    def status(self, **kwargs):
        # Overwrite
        items = []

        def getstate(param):
            try:
                id = self.gpt.gptconfig_get(self.name, param + "_id")
                name = self.gpt.gptconfig_get(self.name, param + "_name")
                if len(id) and len(name):
                    items.append({
                        'key': str(param).title(),
                        'value': "%s  %s" % ( id, name)})
            except Exception:
                pass
        getstate('task')
        getstate('project')
        printtbl(items)
