# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import os
from tests.test_gpt_plugin import TestGPTPlugin
from mock import patch

class TestToggl(TestGPTPlugin):

    plugin = "toggl"
    token = os.getenv("GP_TRACKING_TOGGL_TOKEN", "19c98455494ab3f5d72d91de5c26b116")

    workspaces = [
        {'id': 4755497, 'name': "Workspace T1"},
        {'id': 4755487, 'name': "Workspace T2"}]
    projects = [
        {'id': 164238639, 'name': 'Project T1', "wid": 4755497},
        {'id': 168573879, 'name': 'Project T2', 'wid': 4755487}]

    auth = True
    time_entry = 1950743713

    def setUp(self) -> None:
        super(TestToggl, self).setUp()
        self.gpt.gptconfig_settings("plugin", self.plugin)
        self.gpt.gptconfig_set(self.plugin, "token", self.token)

        if self.token == '19c98455494ab3f5d72d91de5c26b116':
            patch("plugins.toggl.Toggl.auth", return_value=self.auth).start()
            patch("plugins.toggl.Toggl.workspaces", return_value=self.workspaces).start()
            patch("plugins.toggl.Toggl.projects", return_value=self.projects).start()
            patch("plugins.toggl.Toggl.add_time_entry", return_value=self.time_entry).start()

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

        args.update({'time_entry': True, 'set': False, 'toggl_projects': True})
        self.cli_time_entry(args)
