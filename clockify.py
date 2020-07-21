import requests
import json
from urllib.parse import urljoin

class Clockify:
    url = "https://api.clockify.me/"

    def __init__(self, token):
        self.token= token

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
    
    def workspaces(self):
        return self.get("workspaces/")

    def add_time_entry(self, description, start, end ):
        workspaces_id = "5ec2c95096f46724f62f284d"
        time_entry = {
            "start": start,
            #"billable": "true",
            "description": description,
            #"projectId": "5b1667790cb8797321f3d664",
            #"taskId": "5b1e6b160cb8793dd93ec120",
            "end": end,
            #"tagIds": [
            #    "5a7c5d2db079870147fra234"
            #],
        }
        try:
            time_entry_resp, ok = self.post(
                "api/v1/workspaces/{}/time-entries".format(workspaces_id),
                params= time_entry
            )

            if "id" in time_entry_resp.keys():
                return time_entry, True
        except Exception as e:
            print(e)
        return None, False
     