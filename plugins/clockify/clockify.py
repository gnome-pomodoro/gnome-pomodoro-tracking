import requests
import json
from urllib.parse import urljoin
import configparser

class Clockify:
    GTP_CONFIG = "clockify"
    url = "https://api.clockify.me/"
    
    def __init__(self, gptracking):
        self.gptracking = gptracking        
        self.token= None
        self.check_config()        

    def check_config(self):
        try:
            self.token = self.gptracking.gptconfig_get(self.GTP_CONFIG, "token")
        except configparser.NoSectionError as e:
            self.gptracking.gptconfig_set_section(self.GTP_CONFIG)
            self.check_params()
        except configparser.NoOptionError as e:            
            params = self.check_params()
            if 'token' in str(e):
                self.token = params.clockify_token
                try:
                    data, err  = self.get_user()
                    if not err:
                        self.gptracking.gptconfig_set(self.GTP_CONFIG, "token", self.token)
                except Exception as e:
                    self.gptracking.exit(str(e))

    def check_params(self, required=True):
        if required:
            self.gptracking.parse.add_argument('-ct',
                    action='store', 
                    dest='clockify_token', 
                    help=' e.g XtGTMKadTS8sJ/E', 
                    required=True
                    )
        return self.gptracking.gptparse_params()
    
    def gptparse_args(self, required=True):
        if required: 
            pass
        else:
            self.gptracking.parse.add_argument('-cw', 
                    action='store_const', 
                    dest='clockify_workspaces', 
                    help='List clockify workspaces',     
                    const=True,                
                    )
            self.gptracking.parse.add_argument('-cp', 
                    action='store_const', 
                    dest='clockify_projects', 
                    help='List clockify projects',     
                    const=True,
                    )
    def get_user(self):
        return self.get("/api/v1/user")
    
    def cli(self):
        params = self.gptracking.gptparse_params()
        if params.clockify_workspaces:
            try:                
                data, err = self.workspaces()
                if err:
                    raise Exception(err)
                try:
                    workspace = self.gptracking.gptconfig_get(self.GTP_CONFIG, "workspace")
                except:
                    workspace = ""
                for w in data:
                    active = "A" if workspace == w.get('id') else '|'                    
                    if params.write:
                        lenmatch = len(params.write)
                        if params.write == w.get('id')[:lenmatch]:
                            self.gptracking.gptconfig_set(self.GTP_CONFIG, "workspace",w.get('id') )
                            active = "S"
                    print( "{} {} {}".format(w.get('id'),active,w.get('name')))
            except Exception as e:
                self.gptracking.exit(e)
        elif params.clockify_projects:
            try:
                workspace_id = self.gptracking.gptconfig_get(self.GTP_CONFIG, "workspace")
            except:
                workspace, err = self.workspaces(filter='first')
                workspace_id = workspace.get('id')
            try:
                data, err = self.projects(workspace_id)
                try:
                    current_project_id = self.gptracking.gptconfig_get(self.GTP_CONFIG, "project")
                except:
                    current_project_id = ""
                for row in data:
                    active = "A" if current_project_id == row.get('id') else '|'
                    if params.write:
                        lenmatch = len(params.write)
                        if params.write == row.get('id')[:lenmatch]:
                            self.gptracking.gptconfig_set(self.GTP_CONFIG, "project",row.get('id') )
                            active = "S"
                    print( "{} {} {}".format(row.get('id'),active,row.get('name')))
            except Exception as e:
                pass
            
                   


    def headers (self):
        return {'content-type': 'application/json', 'X-Api-Key': self.token}
    
    def http_call(self, url, method, **kwargs):        
        if 'headers' in kwargs:
            kwargs['headers'].update(self.headers())
        else:
            kwargs['headers'] = self.headers()
        # start_time = datetime.datetime.now()
        response = requests.request(method, url, **kwargs)
        # duration = datetime.datetime.now() - start_time
        # print("Duration: ", duration)
        if response.ok:
            try:
                return response.json(), None
            except Exception as e:
                return None, e
        raise Exception(response.text)

    def get(self, action, headers=None):
        return self.http_call(urljoin(self.url, action), 'GET', headers=headers or {})
    
    def post(self, action, params=None, headers=None):
        return self.http_call(urljoin(self.url, action), 'POST', json=params or {}, headers=headers or {})
    
    def workspaces(self, filter=""):
        data, err = self.get("/api/v1/workspaces")
        if filter =='first':
            if not err:
                return len(data) and data[0], err
        return data, err

    def projects(self, workspace_id, filter=""):
        data, err = self.get("/api/v1/workspaces/{}/projects".format(workspace_id))
        if filter =='first' :
            if not err:
                return len(data) and data[0], err
        return data, err

    def add_time_entry(self, description, start, end ):
        workspace_id  = ""
        try:
            workspace_id = self.gptracking.gptconfig_get(self.GTP_CONFIG, "workspace")
        except:
            try:
                workspace, err = self.workspaces(filter='first')
                workspace_id = workspace.get('id')
            except:
                pass
        project_id = None
        try:
            project_id = self.gptracking.gptconfig_get(self.GTP_CONFIG, "project")
        except:
            pass        
        time_entry = {
            "start": start,
            #"billable": "true",
            "description": description,
            "projectId": project_id,
            #"taskId": "5b1e6b160cb8793dd93ec120",
            "end": end,
            #"tagIds": [
            #    "5a7c5d2db079870147fra234"
            #],
        }
        try:
            time_entry_resp, ok = self.post(
                "api/v1/workspaces/{}/time-entries".format(workspace_id),
                params= time_entry
            )

            if "id" in time_entry_resp.keys():
                return True
        except Exception as e:
            pass
        return False
     