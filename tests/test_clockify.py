# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import os
from tests.test_plugin import TestPlugin
from mock import patch


class TestClockify(TestPlugin):

    plugin = "clockify"
    token = os.getenv("GP_TRACKING_CLOCKIFY_TOKEN", "X/oWnmt2eyj4ZCbh")

    workspaces = [
        {"id": "5e9ca62da2686b699ed5748d", "name": "Workspace C1"},
        {"id": "5e9ca62da2786b699ed5748d", "name": "Workspace C2"},
    ]
    projects = [
        {
            "id": "5eab188c991f8972bb9a1fa3",
            "name": "Project C1",
            "workspaceId": "5e9ca62da2686b699ed5748d",
        },
        {
            "id": "5eab188c991f8972bb9a1fa4",
            "name": "Project C2",
            "workspaceId": "5e9ca62da2786b699ed5748d",
        },
    ]

    auth = True
    time_entry = {"id": "6065003e9341062dc3acf936", "name": "Time entry"}

    def setUp(self) -> None:
        super(TestClockify, self).setUp()
        self.gpt.settings_config("plugin", self.plugin)
        self.gpt.set_config(self.plugin, "token", self.token)

        if self.token == "X/oWnmt2eyj4ZCbh":
            patch(
                "gnome_pomodoro_tracking.clockify.Clockify.auth", return_value=self.auth
            ).start()
            patch(
                "gnome_pomodoro_tracking.clockify.Clockify.workspaces",
                return_value=self.workspaces,
            ).start()
            patch(
                "gnome_pomodoro_tracking.clockify.Clockify.projects",
                return_value=self.projects,
            ).start()
            patch(
                "gnome_pomodoro_tracking.clockify.Clockify.add_time_entry",
                return_value=self.time_entry,
            ).start()

        self.load_plugin()

    def test_cli(self):

        args = {"clockify_workspaces": True}
        idA = self.cli_list(args)
        args.update({"set": idA})
        idB = self.cli_set(args)
        assert idA == idB

        args.update(
            {"clockify_projects": True, "clockify_workspaces": False, "set": False}
        )
        idA = self.cli_list(args)
        args.update({"set": idA})
        idB = self.cli_set(args)
        assert idA == idB

        args.update({"time_entry": True, "set": False, "clockify_projects": False})
        self.cli_time_entry(args)
