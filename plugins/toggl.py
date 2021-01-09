from os import name
import pdb
import requests
import json
from urllib.parse import urljoin
import configparser
import logging
from .gpt_plugin import GPTPlugin

logger = logging.getLogger(__name__)

class Toggl(GPTPlugin):

    name = "toggl"
    url = "https://api.track.toggl.com/api/v8"
    token = None

    def __init__(self, gpt):    
        super().__init__(gpt)
    
    def setup(self):
        try:
            self.token = self.gpt.gptconfig_get(self.name, "token")
        except configparser.NoSectionError as e:
            logger.error(str(e))
            self.gpt.gptconfig_set_section(self.name)
            self.add_parse_args(kind="setup-args")
        except configparser.NoOptionError as e:
            self.add_parse_args(kind="setup-args")
            params =  self.gpt.gptparse_params()
            self.token = params.toggl_token
            try:
                if self.auth():
                    self.gpt.gptconfig_set(self.name, "token", self.token)
                    print("Now you can use the plugin. Try gp-tracking -h %s" % self.name)
                else: 
                    raise Exception("Fail auth")
            except Exception as e:
                logger.error(str(e))
                exit(0)

    def add_parse_args(self, kind):
        if kind == "setup-args":
            self.gpt.parse.add_argument('--toggl-token',
                action='store', 
                dest='toggl_token', 
                help=' e.g 23bc78d4e46edd5479885db4260ecsf3', 
                required=True
            )
        else:
            self.gpt.parse.add_argument('--toggl-workspaces', 
                action='store_const', 
                dest='toggl_workspaces', 
                help='List workspaces',     
                const=True,                
            )
            self.gpt.parse.add_argument('--toggl-projects', 
                action='store_const', 
                dest='toggl_projects', 
                help='List projects',     
                const=True,
            )

    http_auth = lambda self: (self.token, "api_token")

    def auth(self):
        try:
            data =  self.http_call('GET', "%s/me" % self.url, auth=self.http_auth())
            if data['data']['id']:
                return True
        except Exception as e :
            pass
        return False
    
    def cli(self):
        params = self.gpt.gptparse_params()

        def findbyid(rows, id):
            for row in rows:
                for k in row.keys():
                    if k == 'id' and str(row.get(k)) == id:
                        return row
            return None

        def onlycolumns(rows):
            l = []
            for r in rows: 
                l.append( { 'id': r.get('id'), 'name':  r.get('name')})
            return l

        if params.toggl_workspaces:
            try:
                rows = self.workspaces()
                if rows:
                    rows = onlycolumns(rows)
                    title ="Toggl Workspaces"
                    if params.set:
                        row = findbyid(rows, params.set)
                        if row: 
                            self.gpt.gptconfig_set(self.name, "workspace_id",row.get('id') )
                            self.gpt.gptconfig_set(self.name, "workspace_name",row.get('name') )

                            self.gpt.gptconfig_set(self.name, "project_id", "")
                            self.gpt.gptconfig_set(self.name, "project_name","" )

                            self.gpt.print_cli([], title= 'the workspace was added successfully')
                        else:
                            self.gpt.print_cli([], title= 'the workspace id was not found')
                    else:
                        self.gpt.print_cli(rows, title=title)
                else:
                    raise Exception("Fail to get workspaces")
            except Exception as e:
                self.gpt.exit(e)
        elif params.toggl_projects:
            try:
                workspace_id = self.gpt.gptconfig_get(self.name, "workspace_id")
            except Exception as e:
                #logger.error(e)
                workspace = self.workspaces(filter='first')
                workspace_id = workspace.get('id')
            try:
                rows = self.projects(workspace_id)
                if rows:
                    rows = onlycolumns(rows)
                    title ="Clockify projects"
                    if params.set:
                        row = findbyid(rows, params.set)
                        if row: 
                            self.gpt.gptconfig_set(self.name, "project_id",row.get('id') )
                            self.gpt.gptconfig_set(self.name, "project_name",row.get('name') )
                            self.gpt.print_cli([], title= 'the project was added successfully')
                        else:
                            self.gpt.print_cli([], title= 'the project id was not found')
                    else: 
                        self.gpt.print_cli(rows, title=title)
                else:
                    raise Exception("Fail to get projects")
            except Exception as e:
                logger.error(e)
   
    def workspaces(self, filter=""):
        url = self.url +  "/workspaces"
        try:
            data = self.http_call('GET', url, auth=self.http_auth())
            if filter =='first':            
                return len(data) and data[0]
            return data
        except:
            pass
        return None

    def projects(self, workspace_id, filter=""):
        try:
            url = "{}/workspaces/{}/projects".format(self.url,workspace_id)
            data = self.http_call('GET',url, auth=self.http_auth())
            if filter =='first' :
                    return len(data) and data[0]
            return data
        except :
            pass
        return None
    
    def add_time_entry(self, **kwargs):        
        description = kwargs.get('name')
        start= kwargs.get('start')
        end= kwargs.get('end')
        minutes = kwargs.get('minutes')
        
        workspace_id  = None
        try:
            workspace_id = self.gpt.gptconfig_get(self.name, "workspace_id")
        except:
            try:
                workspace, err = self.workspaces(filter='first')
                workspace_id = workspace.get('id')
            except:
                pass
        
        project_id = None
        try:
            project_id = self.gpt.gptconfig_get(self.name, "project_id")
        except:
            pass
        
        time_entry = {
            "start": start, # Required 
            "description": description,
            "projectId": project_id,
            "stop": end, # Required
            "duration": float(minutes) * 60,
            "created_with": "gp-tracking"
        }

        if workspace_id:
            time_entry.update({'wid': workspace_id})

        if project_id:
            time_entry.update({'pid': project_id})
        
        try:
            url = self.url + "/time_entries"
            data = self.http_call(
                'POST',url, auth= self.http_auth(),
                json= {"time_entry": time_entry}
            )
            return data["data"]["id"]
        except Exception as e:
            logger.error(e)
        return -1
    
    def status(self):
        items = []
        def getstate(param):
            try:
                id = self.gpt.gptconfig_get(self.name, param+"_id")
                name =self.gpt.gptconfig_get(self.name, param+"_name")
                if len(id) and len(name):
                    items.append({'name': "%s: %s - %s " % (str(param).title(), id, name)})
            except:
                pass
        getstate('workspace')
        getstate('project')
        self.gpt.print_cli(items) 
    




