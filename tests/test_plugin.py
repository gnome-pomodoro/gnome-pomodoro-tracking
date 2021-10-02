# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import unittest
from gnome_pomodoro_tracking.tracking import Tracking

class TestPlugin(unittest.TestCase):

    def setUp(self) -> None:
        self.gpt = Tracking("gnome-pomodoro-tracking.template")
        self.gpt.parse.set_defaults(debug=True)

    def load_plugin(self):
        self.gpt.load_plugin()
        self.gpt.add_parse_args()

    def cli_list(self, parse_defaults):
        self.gpt.parse.set_defaults(**parse_defaults)
        self.gpt.cli()
        id = self.get_stdout_id()
        return id

    def cli_set(self, parse_defaults):
        self.gpt.parse.set_defaults(**parse_defaults)
        self.gpt.cli()
        id = self.get_stdout_id()
        return id

    def get_stdout_id(self):
        id = None
        with open(".gnome-pomodoro-tracking.log", 'r') as f:
            lines = f.readlines()
            line_split = str(lines[len(lines) - 1]).split("gp_tracking.py:write")
            if len(line_split) == 2:
                id  = line_split[1].strip().split(' ')[0] or None
            f.close()
        assert isinstance(id, str)
        return id

    def cli_time_entry(self, parse_defaults):
        self.gpt.parse.set_defaults(**parse_defaults)
        self.gpt.cli()
