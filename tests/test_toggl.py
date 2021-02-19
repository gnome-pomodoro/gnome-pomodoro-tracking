import os
from .test_gpt_plugin import TestGPTPlugin


class TestToggl(TestGPTPlugin):

    plugin = "toggl"

    def test_load_plugin(self):        
        gpt = self.gpt()
        gpt.gptconfig_settings("plugin", self.plugin)
        token = os.getenv("GP_TRACKING_TOGGL_TOKEN", "")
        gpt.gptconfig_set(self.plugin, "token", token)
        assert gpt.load_plugin() == True, "The plugin do not exists!"

    def test_command_toggl_workspaces(self):
        args = {'toggl_workspaces': True}
        idA = self.cli_list( args)
        args.update({"set": idA})
        idB = self.cli_set(args)
        assert idA == idB

    def test_command_toggl_projects(self):
       args = {'toggl_projects': True}
       idA = self.cli_list( args)
       args.update({"set": idA})
       idB = self.cli_set(args)
       assert idA == idB


    def test_time_entry(self): 
        super(TestToggl, self).test_time_entry()