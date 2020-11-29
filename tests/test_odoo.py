import os
import pdb
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
        self.cli_params_list( args)

        id, idErr  = self.get_id_stdout()
        args.update({"set": id})
        self.cli_params_set(args)

    def test_command_odoo_tasks(self):
        args = {'odoo_tasks': True}
        self.cli_params_list( args)

        id, idErr  = self.get_id_stdout()
        args.update({"set": id})
        self.cli_params_set(args)


    def test_time_entry(self): 
        gpt = self.load_plugin()
        parse_defaults =  {"test_time_entry": True}
        gpt.parse.set_defaults(**parse_defaults)
        gpt.cli()