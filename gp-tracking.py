#! /usr/bin/python3
import os 
import argparse
import configparser
import sys
from datetime import datetime, timedelta
import asyncio
import logging

logger = logging.getLogger(__name__)

DIRPATH = os.path.dirname(os.path.realpath(__file__))
DIRHOME = os.path.expanduser("~")
GPT_CONF = "{}/.gp-tracking.conf".format(DIRHOME)
PLUGING = "{}/plugins".format(DIRPATH)

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

class GPTracking:

    def __init__(self, gptconfig, dirpath, dirhome):
        self.gptconfig = gptconfig
        self.dirpath = dirpath
        self.dirhome = dirhome

        self.config = configparser.RawConfigParser()
        self.config.read(self.gptconfig)
        self.parse = argparse.ArgumentParser(
            prog="gp-tracking",
            description='''
            It is a custom action for Gnome Pomodoro, 
            whose main function is to connect with Time Tracking Software
            and create Time Entries.
            ''',
            epilog="Enjoy the program Gnome Pomodoro Tracking.",
        )
        self.plugin = None
    
    def gptconfig_set_section(self, section):
        self.config.add_section(section)
        self.gptconfig_write()

    def gptconfig_set(self, section, key, value):
        self.config.set(section, key, value)
        self.gptconfig_write()

    def gptconfig_get(self, section, key):
        return self.config.get(section, key)


    def gptconfig_write(self):
        with open(self.gptconfig, "w") as f: 
            self.config.write(f)

    def gptconfig_settings(self, key, value=None):
        if value:
            self.config.set("settings", key, value)
            self.gptconfig_write()
        else:
            return self.config.get("settings", key)

    def gptconfig_pomodoro(self, key, value=None):
        if value:
            self.config.set("pomodoro", key, value)
            self.gptconfig_write()
        else:
            return self.config.get("pomodoro", key)

    def gptconfig_pomodoro_clean(self):
        for k in ["start","end", "name",'description']: 
            self.config.set("pomodoro", k, "")
        self.gptconfig_write()
    
    @classmethod
    def today (cls, dt=None):        
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    def convert2minutes(self, seconds):
        return seconds/60.0

    def diff_elapsed(self, start, end):
        try:
            dt_start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
            dt_end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%SZ")
            elapsed = dt_end - dt_start
            return elapsed.total_seconds()
        except Exception as e:
            pass
        return 0
        
        

    @classmethod
    def exists(cls, path, msg="does not exist"):
        return os.path.exists(path)

    @classmethod
    def exit(cls, msg, code = 0):
        print(msg)
        exit(code)

    def load_plugin(self):

        try:
            plugin = self.gptconfig_settings("plugin")            
            if not len(plugin):
              raise configparser.NoOptionError("plugin", "settings")
            
            path_plugin = "%s/plugins/%s" % (self.dirpath, plugin)
            if not GPTracking.exists(path_plugin):
                raise configparser.NoOptionError("plugin", "settings")
            
            sys.path.insert(1, path_plugin)
            globals()[plugin] = __import__(plugin)
            pluginClass = getattr(globals()[plugin], plugin.title())
            self.plugin = pluginClass(self)
            
            return True
        except configparser.NoSectionError as e :
            logger.critical("In the file .gp-tracking.conf no exists secction [settings].\nTry re-install for regenerate file config.\n")
        except configparser.NoOptionError as e:            
            logger.critical("Exec the command gp-tracking --plugin NAME for set.\n")
        except ModuleNotFoundError as e:
            logger.critical("Fail load the plugin module. Exec the command gp-tracking --plugin NAME for  replace.\n")
        except Exception as e :
            logger.critical(e)

        return False

    def gptparse_params(self):
        return self.parse.parse_args()

    def gptparse_args(self, **kwargs):
        
        self.parse.add_argument('--plugin',
            action='store', 
            dest='plugin', 
            help='''
                Select Time Tracking Software
            ''', 
            choices= ['odoo', 'clockify', 'toggl'],
        )
    
        self.parse.add_argument('-gps','--gp-state',
            action='store', 
            dest='gp_state', 
            choices= ['pomodoro', 'short-break', 'long-break'],
            help=argparse.SUPPRESS)
        self.parse.add_argument('-gpt', '--gp-trigger',
            action='store', 
            dest='gp_trigger', 
            help=argparse.SUPPRESS)
        self.parse.add_argument('-gpd', '--gp-duration',
            action='store', 
            dest='gp_duration', 
            help=argparse.SUPPRESS)
        self.parse.add_argument('-gpe', '--gp-elapsed',
            action='store', 
            dest='gp_elapsed', 
            help=argparse.SUPPRESS)

        self.parse.add_argument('-n', '--name',
            action='store',
            dest='name', 
            help='''
                Enter the name of the time entry (Promodoro, short/long break). 
                If there is no active Pomodoro start a new one.
            ''')
        self.parse.add_argument('-r', '--reset',
            action='store_const',
            dest='reset', 
            const=True,
            help=''' 
                Stop the active Pomodoro starts a new time entry
            ''')
        self.parse.add_argument('-k', '--kill',
            action='store_const',
            dest='kill', 
            const=True,
            help='''
                Stop the active Pomodoro
            ''')
        self.parse.add_argument('-s', '--state',
            action='store_const',
            dest='state', 
            const=True,
            help='''
                Displays the summary of the time entry (Plugin, Time elapsed, Name...)
            ''')
        
        self.parse.add_argument('--set', 
            action='store',
            dest='set', 
            help=argparse.SUPPRESS)
        
        self.parse.add_argument('--test-time-entry', 
            action='store_const',
            dest='test_time_entry', 
            const=True,
            help=argparse.SUPPRESS)

        if getattr(self.plugin, 'gptparse_args',False):
            getattr(self.plugin, 'gptparse_args')()
    
    def print_cli(self, items, **kwargs):
        title = kwargs.get('title', None)
        if title:
            print("-" *  len(title))
            print(title)
            print("-" *  len(title))
        for item in items:
            line = ""
            for k in item.keys():
                line += "| %s " %item.get(k)
            print(line)
    """
        Gnome pomodoro methods
    """
    def cli(self):

        params = self.gptparse_params()
        if gpt.gnome_pomodoro():
            return

        if params.plugin:
            plugin = self.gptconfig_settings("plugin")
            self.gptconfig_settings("plugin", params.plugin)
            if not self.load_plugin():            
                self.gptconfig_settings("plugin", plugin)

        if params.reset or params.kill:
            params.trigger = 'skip'
            params.duration = "0"
            params.elapsed = "0"
            self.gnome_pomodoro(params=params)
            os.system("gnome-pomodoro --stop")
            if params.reset:
                os.system("gnome-pomodoro --start --no-default-window")
        if params.name:
            if not len(self.gptconfig_pomodoro("name")) and not len(self.gptconfig_pomodoro("start")):            
                os.system("gnome-pomodoro --stop")
                os.system("gnome-pomodoro --start --no-default-window")
            self.gptconfig_pomodoro("description", params.name)
        if params.state:
            items = []
            dt_start = self.today()
            for k in ["plugin", "start", "name", "description"]:
                try:
                    if k in ["start", "name", "description"]:
                        dt_start = self.gptconfig_pomodoro(k) if k == 'start' else self.today()
                        items.append({'name': "%s: %s" % ( str(k).title(), self.gptconfig_pomodoro(k) )})
                    else:
                        items.append({'name': "%s: %s" % ( str(k).title(), self.gptconfig_settings(k) )})
                except: 
                    pass
            items.append({'name': 'Elapsed: {0:.2f} Min'.format(self.convert2minutes(self.diff_elapsed(dt_start, self.today() ))) })
            self.print_cli(items, title="Gnome Pomodoro Tracking")
            if getattr(self.plugin, 'state',False):
                getattr(self.plugin, 'state')()

        if params.test_time_entry:
            if getattr(self.plugin, 'add_time_entry',False):
                end = datetime.utcnow()
                start = end - timedelta(minutes=25)
                result = getattr(self.plugin, 'add_time_entry')(
                    description= "Test Time entry ", 
                    start=start.strftime(DATETIME_FORMAT), 
                    end=end.strftime(DATETIME_FORMAT),
                    minutes= 25,
                )

        if getattr(self.plugin, 'cli',False):
                getattr(self.plugin, 'cli')()

    def gnome_pomodoro(self, params=None):        
        """
           gp-tracking -gps $(state) -gpt "$(triggers)" -gpd $(duration) -gpe $(elapsed)
        """
        params = self.gptparse_params() if not params else params
        for p in ['gp_state', 'gp_trigger','gp_duration','gp_elapsed']:
            if not getattr(params, p):
                return False        
        #Start timer
        if 'start' in params.gp_trigger or 'resume' in params.gp_trigger:          
            self.gptconfig_pomodoro("name", params.gp_state.title())
            self.gptconfig_pomodoro("start", self.today())
        # Stop timer
        elif 'skip' in params.gp_trigger or 'pause' in params.gp_trigger or 'complete' in params.gp_trigger:
            try:
                name = self.gptconfig_pomodoro("description") or self.gptconfig_pomodoro("name")
                start = self.gptconfig_pomodoro("start")            
                end = self.today()
                minutes = self.convert2minutes(self.diff_elapsed(start, end))            
                if minutes > 0:                                 
                    if getattr(self.plugin, 'add_time_entry',False):
                        # Check param --test-time-entry
                        add_time_entry = getattr(self.plugin, 'add_time_entry')(
                            description=name, 
                            start=start, 
                            end=end,
                            minutes= minutes,
                        )
                        if add_time_entry:
                            logger.info("The time entry is added successfully %s " % add_time_entry)
                        self.gptconfig_pomodoro_clean()
                else: 
                    self.gptconfig_pomodoro_clean()
            except Exception as e:
                print(e)
        return True


if not GPTracking.exists(GPT_CONF):
    GPTracking.exit( "The file {} not exists. Try re-install" .format(GPT_CONF),1)
  
gpt = GPTracking(GPT_CONF, DIRPATH, DIRHOME)
gpt.load_plugin()
gpt.gptparse_args()
gpt.cli()

