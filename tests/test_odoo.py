# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import os
from .test_gpt_plugin import TestGPTPlugin

class TestOdoo(TestGPTPlugin):

    plugin = "odoo"

    def test_plugin(self):
        self.gpt.gptconfig_settings("plugin", self.plugin)
        self.gpt.gptconfig_set(self.plugin, "url", os.getenv("GP_TRACKING_ODOO_URL"))
        self.gpt.gptconfig_set(self.plugin, "database", os.getenv("GP_TRACKING_ODOO_DATABASE"))
        self.gpt.gptconfig_set(self.plugin, "username", os.getenv("GP_TRACKING_ODOO_USERNAME"))
        self.gpt.gptconfig_set(self.plugin, "password", os.getenv("GP_TRACKING_ODOO_PASSWORD"))

    def test_cli(self):
        self.load_plugin()
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

        args.update({'test_time_entry': True, 'set': False, 'odoo_tasks': False})
        self.cli_time_entry(args)
