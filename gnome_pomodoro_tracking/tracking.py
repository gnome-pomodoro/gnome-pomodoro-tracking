# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import os
import argparse
import configparser
import sys
from datetime import datetime, timedelta
import logging
import gnome_pomodoro_tracking.utils as utils

class Tracking:

    def __init__(self, config_path):
        self.config_path = config_path
        self.code_path = os.path.dirname(os.path.realpath(__file__))
        self.config = configparser.RawConfigParser()
        self.setup()

    def setup(self):
        if not os.path.exists(self.config_path) or not os.path.isfile(self.config_path):
            config_template = """[settings]\nplugin =\nmintrace = 0\n"""
            config_template += """[pomodoro]\ntype =\nname =\nstart =\nend =\n"""
            config_template += """[toggl]\n[clockify]\n[odoo]"""
            with open(self.config_path, "w") as f:
                f.write(config_template)
        
        self.config.read(self.config_path)
        self.parse = argparse.ArgumentParser(
            prog="gnome-pomodoro-tracking",
            epilog="GONME Pomodoro Tracking <https://gnomepomodoro.org>",
        )
        self.plugin = None
        self.logger = logging.getLogger(__name__)

    def add_section_config(self, section):
        self.config.add_section(section)
        self._write_config()

    def set_config(self, section, key, value):
        self.config.set(section, key, value)
        self._write_config()

    def get_config(self, section, key):
        return self.config.get(section, key)

    def _write_config(self):
        with open(self.config_path, "w") as f:
            self.config.write(f)

    def settings_config(self, key, value=None):
        if value:
            self.config.set("settings", key, value)
            self._write_config()
        else:
            return self.config.get("settings", key)

    def pomodoro_config(self, key, value=None):
        if value:
            self.config.set("pomodoro", key, value)
            self._write_config()
        else:
            return self.config.get("pomodoro", key)

    def pomodoro_config_clean(self):
        for k in ["start", "end", "type", 'name']:
            self.config.set("pomodoro", k, "")
        self._write_config()

    def logger_config(self):
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")

        fileh = logging.FileHandler('.gnome-pomodoro-tracking.log', 'a')
        fileh.setFormatter(formatter)
        self.logger.addHandler(fileh)

        class StreamToLogger(object):
            def __init__(self, logger, log_level=logging.INFO):
                self.logger = logger
                self.log_level = log_level
                self.linebuf = ''

            def write(self, buf):
                for line in buf.rstrip().splitlines():
                    self.logger.log(self.log_level, line.rstrip())

            def flush(self):
                pass

        sys.stdout = StreamToLogger(self.logger, logging.INFO)
        sys.stderr = StreamToLogger(self.logger, logging.ERROR)

        self.logger.setLevel(logging.DEBUG)

    def load_plugin(self):

        try:
            plugin = self.settings_config("plugin")

            if not len(plugin):
                raise configparser.NoOptionError("plugin", "settings")
            path_plugin = "%s/%s.py" % (self.code_path, plugin)
            if not os.path.isfile(path_plugin):
                raise configparser.NoOptionError("plugin", "settings")
            globals()[plugin] = __import__("gnome_pomodoro_tracking.%s" % plugin)
            pluginClass = getattr( getattr(globals()[plugin], plugin), plugin.title())
            __import__("gnome_pomodoro_tracking.%s" % plugin)
            self.plugin = pluginClass(self)
            return True
        except configparser.NoSectionError as e:
            self.logger.critical("In the file .gnome-pomodoro-tracking.conf no exists secction [settings]."
                                 "\nTry re-install for regenerate file config.\n")
        except configparser.NoOptionError as e:
            self.logger.critical("Exec the command gnome-pomodoro-tracking --plugin NAME for set.\n")
        #except ModuleNotFoundError as e:
        #    self.logger.critical("Fail load the plugin module. Exec the command"
        #                         "gnome-pomodoro-tracking --plugin NAME for  replace.\n")
        except Exception as e:
            self.logger.critical(e)

        return False

    def add_parse_args(self):
        self.parse.add_argument('--plugin',
                                action='store',
                                dest='plugin',
                                help='Time Tracking Service',
                                choices=['odoo', 'clockify', 'toggl'])

        self.parse.add_argument('-gps', '--gp-state',
                                action='store',
                                dest='gp_state',
                                choices=['pomodoro', 'short-break', 'long-break'],
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
                                help='Pomodoro name')
        self.parse.add_argument('-r', '--restart',
                                action='store_const',
                                dest='reset',
                                const=True,
                                help='Pomodoro restart')
        self.parse.add_argument('-k', '--stop',
                                action='store_const',
                                dest='stop',
                                const=True,
                                help='Pomodoro stop')
        self.parse.add_argument('-s', '--status',
                                action='store_const',
                                dest='status',
                                const=True,
                                help='Pomodoro status')
        self.parse.add_argument('-d', '--debug',
                                action='store_const',
                                dest='debug',
                                const=True,
                                help=argparse.SUPPRESS)
        self.parse.add_argument('--set',
                                action='store',
                                dest='set',
                                help=argparse.SUPPRESS)
        self.parse.add_argument('--time-entry',
                                action='store_const',
                                dest='time_entry',
                                const=True,
                                help=argparse.SUPPRESS)
        self.parse.add_argument('--min-trace',
                                dest='min_trace',
                                type=int,
                                default=0,
                                help=argparse.SUPPRESS)
        if getattr(self.plugin, 'add_parse_args', False):
            getattr(self.plugin, 'add_parse_args')(None)

    def cli(self):
        params = self.parse.parse_args()
        if params.debug:
            self.logger_config()

        if not self.gnome_pomodoro():
            if params.plugin:
                plugin = self.settings_config("plugin")
                self.settings_config("plugin", params.plugin)
                if not self.load_plugin():
                    self.settings_config("plugin", plugin)

            if params.min_trace:
                if utils.config_attr(self, 'settings', 'mintrace', params.min_trace):
                    utils.printtbl([{'key': 'Min Trace', 'value': '%s Min' % params.min_trace}])
            if params.reset or params.stop:
                params.trigger = 'skip'
                params.duration = "0"
                params.elapsed = "0"
                self.gnome_pomodoro(params=params)
                os.system("gnome-pomodoro --stop")
                if params.reset:
                    os.system("gnome-pomodoro --start --no-default-window")
            if params.name:
                if not len(self.pomodoro_config("name")) and not len(self.pomodoro_config("start")):
                    os.system("gnome-pomodoro --stop")
                    os.system("gnome-pomodoro --start --no-default-window")
                self.pomodoro_config("name", params.name)
            if params.status:
                items = [
                    {'key': 'Plugin', 'value': str(self.settings_config("plugin")).title()}
                ]
                dt_start = utils.now()
                for k in ["type", 'start', 'name']:
                    try:
                        if k == 'start':
                            dt_start = self.pomodoro_config(k)
                        else:
                            items.append({'key': str(k).title(), 'value': self.pomodoro_config(k)})
                    except Exception:
                        pass
                items.append({'key': 'Elapsed', 'value': '{0:.2f} Min'.format(
                    utils.time_elapsed(dt_start, utils.now(), formatter='minutes')) })
                utils.printtbl(items)
                if getattr(self.plugin, 'status', False):
                    getattr(self.plugin, 'status')()

            if params.time_entry:
                if getattr(self.plugin, 'add_time_entry', False):
                    end = datetime.utcnow()
                    start = end - timedelta(minutes=25)
                    result = getattr(self.plugin, 'add_time_entry')(
                        name="Time entry",
                        start=start.strftime(utils.DATETIME_FORMAT),
                        end=end.strftime(utils.DATETIME_FORMAT),
                        minutes=25,
                    )
                    utils.printtbl([result])

            if getattr(self.plugin, 'cli', False):
                getattr(self.plugin, 'cli')()

    def gnome_pomodoro(self, params=None):
        """
           gnome-pomodoro-tracking -gps $(state) -gpt "$(triggers)" -gpd $(duration) -gpe $(elapsed)
        """
        params = self.parse.parse_args() if not params else params
        for p in ['gp_state', 'gp_trigger', 'gp_duration', 'gp_elapsed']:
            if not getattr(params, p, False):
                return False
        # Start timer
        if 'start' in params.gp_trigger or 'resume' in params.gp_trigger:
            self.pomodoro_config("type", params.gp_state.title())
            self.pomodoro_config("start", utils.now())
        # Stop timer
        elif 'skip' in params.gp_trigger or 'pause' in params.gp_trigger or 'complete' in params.gp_trigger:
            try:
                name = self.pomodoro_config("name") or self.pomodoro_config("type")
                start = self.pomodoro_config("start")
                end = utils.now()
                minutes = utils.time_elapsed(start, end, formatter='minutes')
                mt = utils.config_attr(self, 'settings', 'mintrace')
                mintrace = 0
                if mt and isinstance(mt, dict):
                    _mintrace = mt.get('value', '')
                    if _mintrace.isdigit():
                        mintrace = int(_mintrace)
                if minutes > mintrace:
                    if getattr(self.plugin, 'add_time_entry', False):
                        result = getattr(self.plugin, 'add_time_entry')(
                            name=name,
                            start=start,
                            end=end,
                            minutes=minutes)
                        utils.printtbl([result])
                        self.pomodoro_config_clean()
                else:
                    self.pomodoro_config_clean()
            except Exception as e:
                print(e)
        return True
