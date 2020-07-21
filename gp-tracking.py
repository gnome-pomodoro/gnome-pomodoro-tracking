#! /usr/bin/python3

from datetime import datetime
import argparse
import configparser
import os 
import time
from os.path import expanduser
from clockify import Clockify

class GpTracking:

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

today = lambda : datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

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
    dest='name', 
    help='Activity name')

params = parse.parse_args()
home = expanduser("~")
path = "{}/.config/gp-tracking.conf".format(home)
if not os.path.exists(path):
    raise Exception("File:{} does not exist".format(path))

g = GpTracking(path)
c = Clockify(g.settings("token"))

def convert_minutes(seconds):
    return seconds/60.0
    

def from_cli(name):
    os.system("gnome-pomodoro --stop")
    os.system("gnome-pomodoro --start --no-default-window")
    time.sleep(3)
    GpTracking(path).pomodoro( "name", name)

def from_gp(name, trigger, elapsed):
    if 'start' in trigger or 'resume' in trigger:
        #Start timer
        g.pomodoro( "name", name)
        g.pomodoro("start", today())
    if 'skip' in trigger or 'pause' in trigger or 'complete' in trigger:
        # Stop timer    
        minutes = convert_minutes(float(elapsed))
        if minutes > 2: 
            start = g.pomodoro("start")
            end = today()
            _, ok = c.add_time_entry(g.pomodoro("name"),start, end)
            if ok:
                g.clean_pomodoro()
        else: 
            g.clean_pomodoro()

if params.state == 'pomodoro':
    if params.name: from_cli(params.name)
    else: from_gp("Pomodoro", params.trigger, params.elapsed)
elif params.state == 'short-break':
    if params.name: from_cli(params.name)
    else: from_gp("Short break", params.trigger, params.elapsed)
elif params.state == 'long-break':
    if params.name: from_cli(params.name)
    else: from_gp("Long break", params.trigger, params.elapsed)
