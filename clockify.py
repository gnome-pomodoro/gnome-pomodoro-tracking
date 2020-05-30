#! /bin/env python3
import requests
from urllib.parse import urljoin
import json
from datetime import datetime

import argparse
import configparser
import os 
import time


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
      
class GpClockify:

    def __init__(self, ffile):
        self.config = configparser.RawConfigParser()
        self.config.read(ffile)
        self.ffile = ffile

    def _write(self):
        with open(self.ffile, "w") as f: 
            self.config.write(f)

    def settings(self, key, value=None):
        if value:
            self.config.set("settings", key, value)
            self._write()
        else:
            return self.config.get("settings", key)

    def pomodoro(self, key, value=None):
        if value:
            self.config.set("pomodoro", key, value)
            self._write()
        else:
            return self.config.get("pomodoro", key)

    def clean_pomodoro(self):
        for k in ["start","end", "name"]: 
            self.config.set("pomodoro", k, "")
        self._write()

today = lambda : datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

parse = argparse.ArgumentParser(description="Simple integration gnome-pomodoro and clockify")

parse.add_argument('-e',
    action='store', 
    dest='state', 
    help='State', 
    default="pomodoro")

parse.add_argument('-t', 
    action='store', 
    dest='trigger', 
    help='Trigger')
parse.add_argument('-d', 
    action='store', 
    dest='duration', 
    help='Duration')
parse.add_argument('-l', 
    action='store', 
    dest='elapsed', 
    help='Elapsed')

parse.add_argument('-n', 
    action='store',
    dest='activity_name', 
    help='Activity name')

results = parse.parse_args()
print(results)

path = os.path.dirname(os.path.abspath(__file__)) +"/.gp-clockify.cfg"
if not os.path.exists(path):
    raise Exception("File:{} does not exist".format(path))

g = GpClockify(path)
c = Clockify(g.settings("token"))

def from_cli(activity_name):
    os.system("gnome-pomodoro --start")
    time.sleep(3)
    GpClockify(path).pomodoro( "name", activity_name)

def from_gp(activity_name):
    start = g.pomodoro("start")
    if start:
        end = today()
        _, ok = c.add_time_entry(g.pomodoro("name"),start, end)
        if ok:
            g.clean_pomodoro()
    else:
        g.pomodoro( "name", activity_name)
        g.pomodoro("start", today())


if results.state == 'pomodoro':
    if results.activity_name: from_cli(results.activity_name)
    else: from_gp("Pomodoro")
elif results.state == 'short-break':
    if results.activity_name: from_cli(results.activity_name)
    else: from_gp("Short break")
elif results.state == 'long-break':
    if results.activity_name: from_cli(results.activity_name)
    else: from_gp("Long break")



#

