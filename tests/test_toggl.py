# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import os
from tests.test_plugin import TestPlugin
from mock import patch


class TestToggl(TestPlugin):

    plugin = "toggl"
    token = os.getenv("GP_TRACKING_TOGGL_TOKEN", "19c98455494ab3f5d72d91de5c26b116")

    workspaces = [
        {"id": 4755497, "name": "Workspace T1"},
        {"id": 4755487, "name": "Workspace T2"},
    ]
    projects = [
        {"id": 164238639, "name": "Project T1", "wid": 4755497},
        {"id": 168573879, "name": "Project T2", "wid": 4755487},
    ]

    auth = True
    time_entry = {"id": 1950743713, "name": "Time entry"}

    def setUp(self) -> None:
        super(TestToggl, self).setUp()
        self.gpt.settings_config("plugin", self.plugin)
        self.gpt.set_config(self.plugin, "token", self.token)

        if self.token == "19c98455494ab3f5d72d91de5c26b116":
            patch(
                "gnome_pomodoro_tracking.toggl.Toggl.auth", return_value=self.auth
            ).start()
            patch(
                "gnome_pomodoro_tracking.toggl.Toggl.workspaces",
                return_value=self.workspaces,
            ).start()
            patch(
                "gnome_pomodoro_tracking.toggl.Toggl.projects",
                return_value=self.projects,
            ).start()
            patch(
                "gnome_pomodoro_tracking.toggl.Toggl.add_time_entry",
                return_value=self.time_entry,
            ).start()

        self.load_plugin()

    def test_cli(self):

        args = {"toggl_workspaces": True}
        idA = self.cli_list(args)
        args.update({"set": idA})
        idB = self.cli_set(args)
        assert idA == idB

        args.update({"toggl_projects": True, "toggl_workspaces": False, "set": False})
        idA = self.cli_list(args)
        args.update({"set": idA})
        idB = self.cli_set(args)
        assert idA == idB

        args.update({"time_entry": True, "set": False, "toggl_projects": True})
        self.cli_time_entry(args)
