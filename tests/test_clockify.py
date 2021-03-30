# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import os
from .test_gpt_plugin import TestGPTPlugin

class TestClockify(TestGPTPlugin):

    plugin = "clockify"

    def test_load_plugin(self):
        gpt = self.gpt()
        gpt.gptconfig_settings("plugin", self.plugin)
        token = os.getenv("GP_TRACKING_CLOCKIFY_TOKEN", "")
        gpt.gptconfig_set(self.plugin, "token", token)
        assert gpt.load_plugin() is True, "The plugin do not exists!"

    def test_command_clockify_workspaces(self):
        args = {'clockify_workspaces': True}
        idA = self.cli_list( args)
        args.update({"set": idA})
        idB = self.cli_set(args)
        assert idA == idB

    def test_command_clockify_projects(self):
        args = {'clockify_projects': True}
        idA = self.cli_list( args)
        args.update({"set": idA})
        idB = self.cli_set(args)
        assert idA == idB

    def test_time_entry(self):
        super(TestClockify, self).test_time_entry()