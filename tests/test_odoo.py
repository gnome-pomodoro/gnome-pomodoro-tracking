import os
from .test_gpt_plugin import TestGPTPlugin


class TestOdoo(TestGPTPlugin):

    plugin = "odoo"

    def test_load_plugin(self):        
        gpt = self.gpt()
        gpt.gptconfig_settings("plugin", self.plugin)
        gpt.gptconfig_set(self.plugin, "url",os.getenv("GP_TRACKING_ODOO_URL", ""))
        gpt.gptconfig_set(self.plugin, "database",os.getenv("GP_TRACKING_ODOO_DATABASE", ""))
        gpt.gptconfig_set(self.plugin, "username",os.getenv("GP_TRACKING_ODOO_USERNAME", ""))
        gpt.gptconfig_set(self.plugin, "password",os.getenv("GP_TRACKING_ODOO_PASSWORD", ""))
        assert gpt.load_plugin() == True, "The plugin do not exists!"

    def test_command_odoo_projects(self):
        args = {'odoo_projects': True}
        idA = self.cli_list( args)
        args.update({"set": idA})
        idB = self.cli_set(args)
        assert idA == idB

    def test_command_odoo_tasks(self):
        args = {'odoo_tasks': True}
        idA = self.cli_list( args)
        args.update({"set": idA})
        idB = self.cli_set(args)
        assert idA == idB

    def test_time_entry(self): 
        super(TestOdoo, self).test_time_entry()