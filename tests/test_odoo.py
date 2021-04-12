# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import os
from .test_gpt_plugin import TestGPTPlugin
from mock import patch

class TestOdoo(TestGPTPlugin):

    plugin = "odoo"
    url = os.getenv("GP_TRACKING_ODOO_URL", "http://local.host")
    database = os.getenv("GP_TRACKING_ODOO_DATABASE", "localhost")
    username = os.getenv("GP_TRACKING_ODOO_USERNAME", "username@local.host")
    password = os.getenv("GP_TRACKING_ODOO_PASSWORD", "password@local.host")

    projects = [
        {'id': 1, 'name': 'Project O1'},
        {'id': 2, 'name': 'Project O2'}]
    tasks = [
        {'id': 13, 'name': 'Task O1', 'project_id': 1, 'project_name': 'Project O1'},
        {'id': 14, 'name': 'Task O2', 'project_id': 2, 'project_name': 'Project O1'}]

    auth = True
    time_entry = {'id': 4, 'name': 'Time entry'}

    def setUp(self) -> None:
        super(TestOdoo, self).setUp()
        self.gpt.settings_config("plugin", self.plugin)
        self.gpt.set_config(self.plugin, "url", self.url)
        self.gpt.set_config(self.plugin, "database", self.database)
        self.gpt.set_config(self.plugin, "username", self.username)
        self.gpt.set_config(self.plugin, "password", self.password)

        if self.url == 'http://local.host':
            patch("plugins.odoo.Odoo.auth", return_value=self.auth).start()
            patch("plugins.odoo.Odoo.projects", return_value=self.projects).start()
            patch("plugins.odoo.Odoo.tasks", return_value=self.tasks).start()
            patch("plugins.odoo.Odoo.add_time_entry", return_value=self.time_entry).start()

        self.load_plugin()

    def test_cli(self):

        args = {'odoo_projects': True}
        idA = self.cli_list(args)
        args.update({"set": idA})
        idB = self.cli_set(args)
        assert idA == idB

        args.update({'odoo_tasks': True, 'odoo_projects': False, 'set': False})
        idA = self.cli_list(args)
        args.update({"set": idA})
        idB = self.cli_set(args)
        assert idA == idB

        args.update({'time_entry': True, 'set': False, 'odoo_tasks': False})
        self.cli_time_entry(args)
