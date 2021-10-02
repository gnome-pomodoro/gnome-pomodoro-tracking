# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import configparser
from gnome_pomodoro_tracking.plugin import Plugin
from gnome_pomodoro_tracking.utils import join_url, printtbl, config_attrs,\
    find_by_id, only_columns

class Clockify(Plugin):
    name = "clockify"
    url = "https://api.clockify.me"

    def __init__(self, gpt):
        super().__init__(gpt)

    def setup(self):
        try:
            self.session.update({"token": self.gpt.get_config(self.name, "token")})
        except configparser.NoSectionError as e:
            self.gpt.logger.error(e)
            self.gpt.add_section_config(self.name)
        except configparser.NoOptionError as e:
            pass
        except Exception as e:
            self.gpt.logger.error(e)

    def token(self):
        return self.session.get("token", "")

    def http_headers(self):
        return{'X-Api-Key': self.token()}

    def add_parse_args(self, kind=None):
        self.gpt.parse.add_argument('-w','--workspaces',
                                        action='store_const',
                                        dest='clockify_workspaces',
                                        help='List workspaces',
                                        const=True)
        self.gpt.parse.add_argument('-p','--projects',
                                        action='store_const',
                                        dest='clockify_projects',
                                        help='List projects',
                                        const=True)
        self.gpt.parse.add_argument('--token',
                                        action='store',
                                        dest='clockify_token')
    def auth(self):
        url = join_url(self.url, "api/v1/user")
        try:
            req = self.rget(url, headers=self.http_headers())
            if req.ok:
                data = req.json()
                return data.get("id") != ""
            else:
                raise Exception(req.text)
        except Exception as e:
            self.gpt.logger.exception(e)
        return False

    def cli(self):
        # Overwrite
        params = self.gpt.parse.parse_args()

        if hasattr(params, 'clockify_token') and params.clockify_token:
            self.session.update({"token": params.clockify_token})            
            if self.auth():
                self.gpt.set_config(self.name, "token", self.token())
            else:
                print("Fail auth check your token!")
                exit(0)            

        if hasattr(params, 'clockify_workspaces') and params.clockify_workspaces:
            try:
                rows = self.workspaces()
                if rows:
                    rows = only_columns(rows)
                    if params.set:
                        row = find_by_id(rows, params.set)
                        if row:
                            self.gpt.set_config(self.name, "workspace_id", row.get('id'))
                            self.gpt.set_config(self.name, "workspace_name", row.get('name'))
                            printtbl([row])
                        else:
                            print('The workspace ID was not found')
                    else:
                        printtbl(rows)
                else:
                    raise Exception("Fail get workspaces")
            except Exception as e:
                self.gpt.logger.exception(e)
        elif hasattr(params, 'clockify_projects') and params.clockify_projects:
            try:
                workspace_id = self.gpt.get_config(self.name, "workspace_id")
            except Exception as e:
                self.gpt.logger.error(e)
                workspace = self.workspaces(filter='first')
                workspace_id = workspace.get('id')
            try:
                rows = self.projects(workspace_id)
                if rows:
                    rows = only_columns(rows)
                    if params.set:
                        row = find_by_id(rows, params.set)
                        if row:
                            self.gpt.set_config(self.name, "project_id", row.get('id'))
                            self.gpt.set_config(self.name, "project_name", row.get('name'))
                            printtbl([row])
                        else:
                            print('The project ID was not found')
                    else:
                        printtbl(rows)
                else:
                    raise Exception("Fail get projects")
            except Exception as e:
                self.gpt.logger.exception(e)

    def workspaces(self, filter=""):
        url = join_url(self.url, "api/v1/workspaces")
        try:
            req = self.rget(url, headers=self.http_headers())
            if req.ok:
                data = req.json()
                self.gpt.logger.info(data)
                if filter == 'first':
                    if data:
                        return len(data) and data[0]
                return data
            else:
                raise Exception(req.text)
        except Exception as e:
            self.gpt.logger.exception(e)
        return None

    def projects(self, workspace_id, filter=""):
        url = join_url(self.url, "api/v1/workspaces/%s/projects" % workspace_id)
        try:
            req = self.rget(url, headers=self.http_headers())
            if req.ok:
                data = req.json()
                self.gpt.logger.info(data)
                if filter == 'first':
                    return len(data) and data[0]
                return data
            else:
                raise Exception(req.text)
        except Exception as e:
            self.gpt.logger.exception(e)
        return None

    def add_time_entry(self, **kwargs):
        # Overwrite
        name = kwargs.get('name')
        start = kwargs.get('start')
        end = kwargs.get('end')

        workspace_id  = ""
        try:
            workspace_id = self.gpt.get_config(self.name, "workspace_id")
        except Exception:
            try:
                workspace = self.workspaces(filter='first')
                workspace_id = workspace.get('id')
            except Exception:
                pass
        project_id = None
        try:
            project_id = self.gpt.get_config(self.name, "project_id")
        except Exception:
            pass
        time_entry = {
            "start": start,  # Required
            "description": name,
            "projectId": project_id,
            "end": end,  # Required
        }
        try:
            url = join_url(self.url, "api/v1/workspaces/%s/time-entries" % workspace_id)
            req = self.rpost(url, json=time_entry, headers=self.http_headers())
            if req.ok:
                data = req.json()
                self.gpt.logger.info(data)
                return {'id': data['id'], 'name': name}
            else:
                raise Exception(req.text)
        except Exception as e:
            self.gpt.logger.exception(e)
        return None

    def status(self, **kwargs):
        attrs = ['workspace_name', 'project_name']
        items = config_attrs(self.gpt, self.name, attrs, formatter='status')
        printtbl(items)