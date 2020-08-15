#! /usr/bin/python3
import os 
import argparse
import configparser
import sys
from datetime import datetime
import asyncio


DIRPATH = os.path.dirname(os.path.realpath(__file__))
DIRHOME = os.path.expanduser("~")
GPT_CONF = "{}/.gp-tracking.conf".format(DIRHOME)
PLUGING = "{}/plugins".format(DIRPATH)


#get_params = lambda : 

class GPTracking:

    def __init__(self, gptconfig, dirpath, dirhome):
        self.gptconfig = gptconfig
        self.dirpath = dirpath
        self.dirhome = dirhome

        self.config = configparser.RawConfigParser()
        self.config.read(self.gptconfig)
        self.parse = argparse.ArgumentParser(
            prog="gp-tracking",
            description="GNOME POMODORO TRACKING",
            epilog="Enjoy the program! :)",
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

    def gpconfig_settings(self, key, value=None):
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
    def today (cls):
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
    def exists(cls, file_or_dir, msg="does not exist"):
        if not os.path.exists(file_or_dir):
            print("Error: {} {}".format(file_or_dir,msg))
            exit
        return True
    
    @classmethod
    def exit(cls, msg):
        print(msg)
        exit(1)

    def load_plugin(self):
        try:
            plugin = self.gpconfig_settings("plugin")
            if not len(plugin):
              raise configparser.NoOptionError("plugin", "settings")
            path_plugin = "%s/plugins/%s" % (self.dirpath, plugin)
            GPTracking.exists(path_plugin, "the plugin does not exist.")            
        except configparser.NoOptionError as e:
            self.gptparse_args(['plugin'])
            params = self.gptparse_params()
            path_plugin = "%s/plugins/%s" % (self.dirpath, params.plugin)
            GPTracking.exists(path_plugin, "the plugin does not exist.")
            self.gpconfig_settings("plugin", params.plugin)
            plugin = params.plugin

        sys.path.insert(1, path_plugin)
        try:            
            globals()[plugin] = __import__(plugin)
            pluginClass = getattr(globals()[plugin], plugin.title())
            self.plugin = pluginClass(self)
        except ModuleNotFoundError as e:
            GPTracking.exit("Fail import plugin %s" % plugin)
        except Exception as e:
            GPTracking.exit("Fail import plugin %s" % plugin)
        
    def gptparse_params(self):
        return self.parse.parse_args()

    def gptparse_args(self, required=True):
        
        if isinstance(required, list):                
            required_args = {}                
            for p in required:
                required_args.update({p: True})            
            self.parse.add_argument('-p',
                action='store', 
                dest='plugin', 
                help='Check plugins available ', 
                required=required_args.get('plugin', False)
            )
    
        self.parse.add_argument('-s',
            action='store', 
            dest='state', 
            choices= ['pomodoro', 'short-break', 'long-break'],
            help='Pomodoro state', 
            default="pomodoro")

        self.parse.add_argument('-t', 
            action='store', 
            dest='trigger', 
            help='Pomodoro  trigger')
        self.parse.add_argument('-d', 
            action='store', 
            dest='duration', 
            help='Pomodoro  duration')

        self.parse.add_argument('-e', 
            action='store', 
            dest='elapsed', 
            help='Pomodoro elapsed')

        self.parse.add_argument('-n', 
            action='store',
            dest='name', 
            help='Pomodoro name')

        self.parse.add_argument('-r', 
            action='store_const',
            dest='reset', 
            const=True,
            help='Reset pomodoro')
        self.parse.add_argument('-k', 
            action='store_const',
            dest='kill', 
            const=True,
            help='Kill pomodoro')
        self.parse.add_argument('-w', 
            action='store',
            dest='write', 
            help='Write value in file config')

        if getattr(self.plugin, 'gptparse_args',False):
            getattr(self.plugin, 'gptparse_args')(required=False)
    """
        Gnome pomodoro methods
    """
    def cli(self):        
        params = self.gptparse_params()
        if gpt.gnome_pomodoro():
            return
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

        if getattr(self.plugin, 'cli',False):
                getattr(self.plugin, 'cli')()

    def gnome_pomodoro(self, params=None):        
        """
            -s $(state) -t "$(triggers)" -d $(duration) -e $(elapsed)
        """
        params = self.gptparse_params() if not params else params
        for p in ['state', 'trigger','duration','elapsed']:
            if not getattr(params, p):
                return False
        params.name = params.name.title() if params.name else params.state.title()
        #Start timer
        if 'start' in params.trigger or 'resume' in params.trigger:          
            self.gptconfig_pomodoro("name", params.name)
            self.gptconfig_pomodoro("start", self.today())
        # Stop timer
        elif 'skip' in params.trigger or 'pause' in params.trigger or 'complete' in params.trigger:
            try:
                name = self.gptconfig_pomodoro("description") or self.gptconfig_pomodoro("name")
                start = self.gptconfig_pomodoro("start")            
                end = self.today()
                minutes = self.convert2minutes(self.diff_elapsed(start, end))            
                if minutes > 2:                                 
                    if getattr(self.plugin, 'add_time_entry',False):
                        getattr(self.plugin, 'add_time_entry')(name, start, end)
                        self.gptconfig_pomodoro_clean()
                else: 
                    self.gptconfig_pomodoro_clean()
            except Exception as e:
                print(e)
        return True

GPTracking.exists(GPT_CONF,)

gpt = GPTracking(GPT_CONF, DIRPATH, DIRHOME)
gpt.load_plugin()
gpt.gptparse_args()

gpt.gptparse_params()
gpt.cli()




#def from_cli(name):
#    time.sleep(3)
#    GpTracking(path).pomodoro( "name", name)


