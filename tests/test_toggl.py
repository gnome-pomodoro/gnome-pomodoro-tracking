# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import os
from tests.test_gpt_plugin import TestGPTPlugin

class TestToggl(TestGPTPlugin):

    plugin = "toggl"

    def test_plugin(self):
        self.gpt.gptconfig_settings("plugin", self.plugin)
        token = os.getenv("GP_TRACKING_TOGGL_TOKEN")
        self.gpt.gptconfig_set(self.plugin, "token", token)

    def test_cli(self):
        self.load_plugin()
        args = {'toggl_workspaces': True}
        idA = self.cli_list(args)
        args.update({"set": idA})
        idB = self.cli_set(args)
        assert idA == idB

        args.update({'toggl_projects': True, 'toggl_workspaces': False, 'set': False})
        idA = self.cli_list(args)
        args.update({"set": idA})
        idB = self.cli_set(args)
        assert idA == idB

        args.update({'test_time_entry': True, 'set': False, 'toggl_projects': True})
        self.cli_time_entry(args)
