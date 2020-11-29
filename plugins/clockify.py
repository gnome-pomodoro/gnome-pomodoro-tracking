import json
import configparser
import logging

from .gpt_plugin import GPTPlugin
from .gpt_utils import join_url

logger = logging.getLogger(__name__)

class Clockify(GPTPlugin):
    name = "clockify"
    url = "https://api.clockify.me"
    
    def __init__(self, gpt):
        super().__init__(gpt)
            
    def setup(self):
        try:
            self.session.update({"token": self.gpt.gptconfig_get(self.name, "token")})
        except configparser.NoSectionError as e:
            #logger.error(str(e))
            self.gpt.gptconfig_set_section(self.name)
            self.add_parse_args(kind="setup-args")
        except configparser.NoOptionError as e:            
            #logger.error(str(e))
            self.add_parse_args(kind="setup-args")
            params =  self.gpt.gptparse_params()
            self.session.update({"token": params.clockify_token})
            try:
                if self.auth():
                    self.gpt.gptconfig_set(self.name, "token", self.token())
                    print(f"{self.name} now can do you use.")
            except Exception as e:
                logger.error(str(e))
                exit(0)        
    
    token = lambda self: self.session.get("token", "")
    http_headers = lambda self: {'X-Api-Key': self.token()}

    def add_parse_args(self, kind):
        if kind == "setup-args":
            self.gpt.parse.add_argument('--clockify-token',
                action='store', 
                dest='clockify_token', 
                help=' e.g XtGTMKadTS8sJ/E', 
                required=True
            )
        else:
        # Overwrite
            self.gpt.parse.add_argument('--clockify-workspaces', 
                    action='store_const', 
                    dest='clockify_workspaces', 
                    help='List clockify workspaces',     
                    const=True,                
                    )
            self.gpt.parse.add_argument('--clockify-projects', 
                    action='store_const', 
                    dest='clockify_projects', 
                    help='List clockify projects',     
                    const=True,
                    )
    
    def auth(self):
        url = join_url(self.url, "/api/v1/user")
        try:
            data = self.http_call('GET', url, headers= self.http_headers())
            return data.get("id") != ""
        except Exception as e :
            msg =""
            try:
                err = json.loads(str(e))
                msg = err.get("message", "Fail Auth")
            except Exception as jl:
                pass
            raise Exception(msg)

        return False
    
    def cli(self):
        # Overwrite        
        params = self.gpt.gptparse_params() 
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
                rows = self.workspaces()
                if rows:
                    rows = onlycolumns(rows)
                    title ="Clockify workspaces"
                    if params.set:
                        row = findbyid(rows, params.set)
                        if row: 
                            self.gpt.gptconfig_set(self.name, "workspace_id",row.get('id') )
                            self.gpt.gptconfig_set(self.name, "workspace_name",row.get('name') )
                            self.gpt.print_cli([], title= 'the workspace was added successfully')
                        else:
                            self.gpt.print_cli([], title= 'the workspace id was not found')
                    else:
                        self.gpt.print_cli(rows, title=title)
                else:
                    raise Exception("Fail get workspaces")
            except Exception as e:
                self.gpt.exit(e)
        elif params.clockify_projects:
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
                    raise Exception("Fail get projects")
            except Exception as e:
                raise Exception(e)
    
    def workspaces(self, filter=""):
        url = join_url(self.url, "/api/v1/workspaces")
        try:
            data = self.http_call('GET', url, headers = self.http_headers())
            if filter =='first':
                if data:
                    return len(data) and data[0]
            return data
        except:
            pass
        return None

    def projects(self, workspace_id, filter=""):
        url =join_url(self.url,f"/api/v1/workspaces/{workspace_id}/projects")
        try:            
            data = self.http_call('GET', url, headers = self.http_headers())
            if filter =='first' :            
                return len(data) and data[0]
            return data
        except:
            pass
        return None
    
    def add_time_entry(self, **kwargs ):
        # Overwrite
        description = kwargs.get('description')
        start= kwargs.get('start')
        end= kwargs.get('end')

        workspace_id  = ""
        try:
            workspace_id = self.gpt.gptconfig_get(self.name, "workspace_id")
        except:
            try:
                workspace = self.workspaces(filter='first')
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
            "end": end, # Required
        }
        try:
            url = join_url(self.url, f"api/v1/workspaces/{workspace_id}/time-entries")
            data = self.http_call('POST', url,json= time_entry, headers= self.http_headers())
            return data["id"]
        except Exception as e:
            pass
        return -1
    
    def state(self, **kwargs):
        # Overwrite
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

    