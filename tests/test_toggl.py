# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import os
from tests.test_gpt_plugin import TestGPTPlugin
from mock import patch

class TestToggl(TestGPTPlugin):

    plugin = "toggl"
    token = os.getenv("GP_TRACKING_TOGGL_TOKEN", "")

    fake_workspces = [
        {'id': 4755497, 'name': "Workspace 1"},
        {'id': 4755487, 'name': "Workspace 2"}]
    fake_projects = [
        {'id': 164238639, 'name': 'Project 1', "wid": 4755497}, 
        {'id': 168573879, 'name': 'Project 2', 'wid': 4755487}]

    fake_auth = True    
    fake_time_entry = 1950743713

    def setUp(self) -> None:
        super(TestToggl, self).setUp()        
        self.gpt.gptconfig_settings("plugin", self.plugin)
        self.gpt.gptconfig_set(self.plugin, "token", self.token)

        patch("plugins.toggl.Toggl.auth", return_value=self.fake_auth).start()
        patch("plugins.toggl.Toggl.workspaces", return_value=self.fake_workspces).start()
        patch("plugins.toggl.Toggl.projects", return_value=self.fake_projects).start()
        patch("plugins.toggl.Toggl.add_time_entry", return_value=self.fake_time_entry).start()
        self.load_plugin()

    def test_cli(self):

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
