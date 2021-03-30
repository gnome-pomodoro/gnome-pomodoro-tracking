# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import gp_tracking as gpt

class TestGPTPlugin(object):

    def gpt(self):
        DIRHOME = "./tests"
        return gpt.GPTracking("gnome-pomodoro-tracking.template", "Remove", DIRHOME)

    def load_plugin(self):
        gpt = self.gpt()
        gpt.load_plugin()
        gpt.add_parse_args()
        return gpt

    def cli_list(self, parse_defaults):
        gpt = self.load_plugin()
        gpt.parse.set_defaults(**parse_defaults)
        gpt.cli()
        id, err  = self.get_stdout_id()
        assert err is None, err
        return id

    def cli_set(self, parse_defaults):
        gpt = self.load_plugin()
        gpt.parse.set_defaults(**parse_defaults)
        gpt.cli()
        id, err = self.get_stdout_id()
        assert err is None, err
        return id

    def get_stdout_id(self):
        id, err = None, None
        with open("/tmp/gnome-pomodoro-tracking.stdout", 'r') as f:
            lines = f.readlines()
            index = 1 if len(lines) > 1 else 0
            line_split = str(lines[index]).split(" ")
            if len(line_split) > 1:
                id  = line_split[0].strip()
            else:
                err = "Not found Id"
            f.close()
        return id, err

    def test_time_entry(self):
        gpt = self.load_plugin()
        parse_defaults =  {"test_time_entry": True}
        gpt.parse.set_defaults(**parse_defaults)
        gpt.cli()