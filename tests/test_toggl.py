import os
import pdb
from .test_plugin_gpt import TestPluginGPT


class TestToggl(TestPluginGPT):

    plugin = "toggl"

    def test_load_plugin(self):        
        gpt = self.gpt()
        gpt.gptconfig_settings("plugin", self.plugin)
        token = os.getenv("GP_TRACKING_TOGGL_TOKEN", "")
        gpt.gptconfig_set(self.plugin, "token", token)
        assert gpt.load_plugin() == True, "The plugin do not exists!"

    def test_command_toggl_workspaces(self):
        args = {'toggl_workspaces': True}
        self.cli_params_list( args)
    
        id, idErr  = self.get_id_stdout()
        args.update({"set": id})
        self.cli_params_set(args)

    def test_command_toggl_projects(self):
       args = {'toggl_projects': True}
       self.cli_params_list( args)

       id, idErr  = self.get_id_stdout()
       args.update({"set": id})
       self.cli_params_set(args)


    def test_time_entry(self): 
        gpt = self.load_plugin()
        parse_defaults =  {"test_time_entry": True}
        gpt.parse.set_defaults(**parse_defaults)
        gpt.cli()