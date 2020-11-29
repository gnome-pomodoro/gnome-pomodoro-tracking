import pdb
import requests
import json
from urllib.parse import urljoin
import configparser
import logging

logger = logging.getLogger(__name__)

class Clockify:
    GTP_CONFIG = "clockify"
    url = "https://api.clockify.me/"
    
    def __init__(self, gptracking):
        self.gptracking = gptracking        
        self.token= None
        self.setup_config()
    
    # Check setup config & params 
    def setup_config(self):
        try:
            self.token = self.gptracking.gptconfig_get(self.GTP_CONFIG, "token")
        except configparser.NoSectionError as e:
            #logger.error(str(e))
            self.gptracking.gptconfig_set_section(self.GTP_CONFIG)
            self.setup_params()
        except configparser.NoOptionError as e:            
            #logger.error(str(e))
            self.setup_params()
            params =  self.gptracking.gptparse_params()
            self.token = params.clockify_token
            try:
                data, err  = self.auth()
                if not err:
                    self.gptracking.gptconfig_set(self.GTP_CONFIG, "token", self.token)
            except Exception as e:
                logger.error(str(e))
                exit(0)

    def setup_params(self):
        self.gptracking.parse.add_argument('--clockify-token',
            action='store', 
            dest='clockify_token', 
            help=' e.g XtGTMKadTS8sJ/E', 
            required=True
        )
        
    
    ## Optional params
    def gptparse_args(self, **kwargs):
       # Overwrite
        self.gptracking.parse.add_argument('--clockify-workspaces', 
                action='store_const', 
                dest='clockify_workspaces', 
                help='List clockify workspaces',     
                const=True,                
                )
        self.gptracking.parse.add_argument('--clockify-projects', 
                action='store_const', 
                dest='clockify_projects', 
                help='List clockify projects',     
                const=True,
                )

    # Operations clockify 
    def auth(self):
        return self.http_call("/api/v1/user", 'GET')
    
    def cli(self):
        # Overwrite        
        params = self.gptracking.gptparse_params() 
        def findbyid(rows, id):
            for row in rows:
                for k in row.keys():
                    if k == 'id' and row.get(k) == id:
                        return row
            return None

        def onlycolumns(rows):
            l = []
            for r in rows: 
                l.append( { 'id': r.get('id'), 'name':  r.get('name')})
            return l
        
        

        if params.clockify_workspaces:
            try:

                rows, err = self.workspaces()
                rows = onlycolumns(rows)
                title ="Clockify workspaces"
                if params.set:
                    row = findbyid(rows, params.set)
                    if row: 
                        self.gptracking.gptconfig_set(self.GTP_CONFIG, "workspace_id",row.get('id') )
                        self.gptracking.gptconfig_set(self.GTP_CONFIG, "workspace_name",row.get('name') )
                        self.gptracking.print_cli([], title= 'the workspace was added successfully')
                    else:
                        self.gptracking.print_cli([], title= 'the workspace id was not found')
                else:
                    self.gptracking.print_cli(rows, title=title)
            except Exception as e:
                self.gptracking.exit(e)
        elif params.clockify_projects:
            try:
                workspace_id = self.gptracking.gptconfig_get(self.GTP_CONFIG, "workspace_id")
            except Exception as e:
                logger.error(e)
                workspace, err = self.workspaces(filter='first')
                workspace_id = workspace.get('id')
            try:
                rows, err = self.projects(workspace_id)                
                rows = onlycolumns(rows)
                title ="Clockify projects"
                if params.set:
                    row = findbyid(rows, params.set)
                    if row: 
                        self.gptracking.gptconfig_set(self.GTP_CONFIG, "project_id",row.get('id') )
                        self.gptracking.gptconfig_set(self.GTP_CONFIG, "project_name",row.get('name') )
                        self.gptracking.print_cli([], title= 'the project was added successfully')
                    else:
                        self.gptracking.print_cli([], title= 'the project id was not found')
                else: 
                    self.gptracking.print_cli(rows, title=title)
            except Exception as e:
                raise Exception(e)

  
    
    def http_call(self, url, method, **kwargs):
        
        headers = lambda : {'content-type': 'application/json', 'X-Api-Key': self.token}

        if 'headers' in kwargs:
            kwargs['headers'].update(headers())
        else:
            kwargs['headers'] = headers()
        
        url = urljoin(self.url, url)
        response = requests.request(method, url, **kwargs)
        
        if response.ok:
            try:
                return response.json(), None
            except Exception as e:
                return None, e
        raise Exception(response.text)

    def workspaces(self, filter=""):
        data, err = self.http_call("/api/v1/workspaces", 'GET')
        if filter =='first':
            if not err:
                return len(data) and data[0], err
        return data, err

    def projects(self, workspace_id, filter=""):
        data, err = self.http_call("/api/v1/workspaces/{}/projects".format(workspace_id), 'GET')
        if filter =='first' :
            if not err:
                return len(data) and data[0], err
        return data, err

    def add_time_entry(self, **kwargs ):
        # Overwrite
        description = kwargs.get('description')
        start= kwargs.get('start')
        end= kwargs.get('end')

        workspace_id  = ""
        try:
            workspace_id = self.gptracking.gptconfig_get(self.GTP_CONFIG, "workspace_id")
        except:
            try:
                workspace, err = self.workspaces(filter='first')
                workspace_id = workspace.get('id')
            except:
                pass
        project_id = None
        try:
            project_id = self.gptracking.gptconfig_get(self.GTP_CONFIG, "project_id")
        except:
            pass        
        time_entry = {
            "start": start, # Required 
            "description": description,
            "projectId": project_id,
            "end": end, # Required
        }
        try:
            time_entry_resp, ok = self.http_call(
                "api/v1/workspaces/{}/time-entries".format(workspace_id), 'POST',
                json= time_entry
            )

            if "id" in time_entry_resp.keys():
                return time_entry_resp
            raise Exception(ok)
        except Exception as e:
            raise Exception(e)
        return False
    
    ## Optional params
    def state(self, **kwargs):
        # Overwrite
        items = []
        def getstate(param):
            try:
                id = self.gptracking.gptconfig_get(self.GTP_CONFIG, param+"_id")
                name =self.gptracking.gptconfig_get(self.GTP_CONFIG, param+"_name")
                if len(id) and len(name):
                    items.append({'name': "%s: %s - %s " % (str(param).title(), id, name)})
            except:
                pass
        getstate('workspace')
        getstate('project')
        self.gptracking.print_cli(items)