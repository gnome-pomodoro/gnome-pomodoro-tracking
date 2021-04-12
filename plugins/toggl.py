# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import configparser
from .gpt_plugin import GPTPlugin
from .gpt_utils import printtbl, join_url,\
    find_by_id, only_columns, config_attrs

class Toggl(GPTPlugin):

    name = "toggl"
    url = "https://api.track.toggl.com/api/v8"
    token = None

    def __init__(self, gpt):
        super().__init__(gpt)

    def setup(self):
        try:
            self.token = self.gpt.get_config(self.name, "token")
        except configparser.NoSectionError as e:
            self.gpt.logger.error(e)
            self.gpt.add_section_config(self.name)
            self.add_parse_args(kind="setup-args")
        except configparser.NoOptionError as e:
            self.gpt.logger.error(e)
            self.add_parse_args(kind="setup-args")
            params =  self.gpt.parse.parse_args()
            self.token = params.toggl_token
            try:
                if self.auth():
                    self.gpt.set_config(self.name, "token", self.token)
                    print(f"{self.name} now can do you use.")
                else:
                    raise Exception("Fail auth")
            except Exception as e:
                self.gpt.logger.critical(e)
                exit(0)

    def add_parse_args(self, kind):
        if kind == "setup-args":
            self.gpt.parse.add_argument('--toggl-token',
                                        action='store',
                                        dest='toggl_token',
                                        help=' e.g 23bc78d4e46edd5479885db4260ecsf3',
                                        required=True)
        else:
            self.gpt.parse.add_argument('--toggl-workspaces',
                                        action='store_const',
                                        dest='toggl_workspaces',
                                        help='List workspaces',
                                        const=True)
            self.gpt.parse.add_argument('--toggl-projects',
                                        action='store_const',
                                        dest='toggl_projects',
                                        help='List projects',
                                        const=True)

    def http_auth(self):
        return (self.token, "api_token")

    def auth(self):
        try:
            req = self.rget(join_url(self.url, "me" ), auth=self.http_auth())
            if req.ok:
                data = req.json()
                if data['data']['id']:
                    return True
            else:
                raise Exception(req.text)
        except Exception as e:
            self.gpt.logger.exception(e)
        return False

    def cli(self):
        params = self.gpt.parse.parse_args()

        if hasattr(params, 'toggl_workspaces') and params.toggl_workspaces:
            try:
                rows = self.workspaces()
                if rows:
                    rows = only_columns(rows)
                    if params.set:
                        row = find_by_id(rows, params.set)
                        if row:
                            self.gpt.set_config(self.name, "workspace_id", row.get('id') )
                            self.gpt.set_config(self.name, "workspace_name", row.get('name') )

                            self.gpt.set_config(self.name, "project_id", "")
                            self.gpt.set_config(self.name, "project_name", "" )

                            printtbl([row])
                        else:
                            print('The workspace ID was not found')
                    else:
                        printtbl(rows)
                else:
                    raise Exception("Fail to get workspaces")
            except Exception as e:
                self.gpt.logger.exception(e)
        elif hasattr(params, 'toggl_projects') and params.toggl_projects:
            try:
                workspace_id = self.gpt.get_config(self.name, "workspace_id")
            except Exception as e:
                workspace = self.workspaces(filter='first')
                workspace_id = workspace.get('id')
            try:
                rows = self.projects(workspace_id)
                if rows:
                    rows = only_columns(rows)
                    if params.set:
                        row = find_by_id(rows, params.set)
                        if row:
                            self.gpt.set_config(self.name, "project_id", row.get('id') )
                            self.gpt.set_config(self.name, "project_name", row.get('name') )
                            printtbl([row])
                        else:
                            print('The project ID was not found')
                    else:
                        printtbl(rows)
                else:
                    raise Exception("Fail to get projects")
            except Exception as e:
                self.gpt.logger.exception(e)

    def workspaces(self, filter=""):
        url = join_url(self.url, "workspaces")
        try:
            req = self.rget(url, auth=self.http_auth())
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

    def projects(self, workspace_id, filter=""):
        try:
            url = join_url(self.url, "workspaces/{}/projects".format(workspace_id))
            req = self.rget(url, auth=self.http_auth())
            if req.ok:
                data = req.json()
                self.gpt.logger.info(data)
                if filter == 'first':
                    return len(data) and data[0]
            else:
                raise Exception(req.text)
            return data
        except Exception as e:
            self.gpt.logger.exception(e)
        return None

    def add_time_entry(self, **kwargs):
        name = kwargs.get('name')
        start = kwargs.get('start')
        end = kwargs.get('end')
        minutes = kwargs.get('minutes')

        workspace_id  = None
        try:
            workspace_id = self.gpt.get_config(self.name, "workspace_id")
        except Exception as e:
            try:
                workspace, err = self.workspaces(filter='first')
                workspace_id = workspace.get('id')
            except Exception as e:
                pass
        project_id = None
        try:
            project_id = self.gpt.get_config(self.name, "project_id")
        except Exception as e:
            pass

        time_entry = {
            "start": start,  # Required
            "description": name,
            "projectId": project_id,
            "stop": end,  # Required
            "duration": float(minutes) * 60,
            "created_with": "gp-tracking"
        }

        if workspace_id:
            time_entry.update({'wid': workspace_id})

        if project_id:
            time_entry.update({'pid': project_id})

        try:
            url = join_url(self.url, "time_entries")
            req = self.rpost(
                url, auth=self.http_auth(),
                json={"time_entry": time_entry}
            )
            if req.ok:
                data = req.json()
                self.gpt.logger.info(data)
                return {'id': data['data']['id'], 'name': name}
            else:
                raise Exception(req.text)
        except Exception as e:
            self.gpt.logger.exception(e)
        return None

    def status(self):
        attrs = ['workspace_name', 'project_name']
        items = config_attrs(self.gpt, self.name, attrs, formatter='status')
        printtbl(items)