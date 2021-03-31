# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import os
from tests.test_gpt_plugin import TestGPTPlugin
from mock import patch

class TestClockify(TestGPTPlugin):

    plugin = "clockify"
    token = os.getenv("GP_TRACKING_CLOCKIFY_TOKEN", "X/oWnmt2eyj4ZCbh")

    fake_workspaces = [
        {'id': '5e9ca62da2686b699ed5748d', 'name': "Workspace C1"},
        {'id': '5e9ca62da2786b699ed5748d', 'name': "Workspace C2"}]
    fake_projects = [
        {'id': '5eab188c991f8972bb9a1fa3', 'name': 'Project C1', 'workspaceId':'5e9ca62da2686b699ed5748d'},
        {'id': '5eab188c991f8972bb9a1fa4', 'name': 'Project C2', 'workspaceId':'5e9ca62da2786b699ed5748d'}]
    
    fake_auth = True    
    fake_time_entry = '6065003e9341062dc3acf936'

    def setUp(self) -> None:
        super(TestClockify, self).setUp()
        self.gpt.gptconfig_settings("plugin", self.plugin)
        self.gpt.gptconfig_set(self.plugin, "token", self.token)
        
        patch("plugins.clockify.Clockify.auth", return_value=self.fake_auth).start()
        patch("plugins.clockify.Clockify.workspaces", return_value=self.fake_workspaces).start()
        patch("plugins.clockify.Clockify.projects", return_value=self.fake_projects).start()
        patch("plugins.clockify.Clockify.add_time_entry", return_value=self.fake_time_entry).start()

        self.load_plugin()

    def test_cli(self):

        args = {'clockify_workspaces': True}
        idA = self.cli_list( args)
        args.update({"set": idA})
        idB = self.cli_set(args)
        assert idA == idB

        args.update({'clockify_projects': True, 'clockify_workspaces': False, 'set': False})
        idA = self.cli_list( args)
        args.update({"set": idA})
        idB = self.cli_set(args)
        assert idA == idB

        args.update({'test_time_entry': True, 'set': False, 'clockify_projects': False})
        self.cli_time_entry(args)
