from os import supports_effective_ids
import pdb
import gp_tracking as gpt
import os
import re

class TestPluginGPT(object):

    def gpt(self):
        #DIRPATH = gpt.GPTracking.dirpath()
        DIRHOME = os.path.expanduser("~")
        return gpt.GPTracking("./gp-tracking.template", "Remove", DIRHOME)

    def load_plugin(self):
        gpt = self.gpt()
        gpt.load_plugin()
        gpt.gptparse_args()
        return gpt

    def cli_params_list(self, parse_defaults):
        gpt = self.load_plugin()
        gpt.parse.set_defaults(**parse_defaults)
        gpt.cli()
        id, idErr  = self.get_id_stdout()
        assert idErr == None, idErr
    
    def cli_params_set(self,parse_defaults):
        gpt = self.load_plugin()
        gpt.parse.set_defaults(**parse_defaults)
        gpt.cli()
        success, successErr = self.set_success_stdout()
        assert successErr == None, successErr


    def get_id_stdout(self):
        data  , err = None, None
        with open("tests/stdout.txt", 'r') as f:
            lines = f.readlines()
            line_split = str(lines[1]).split("|")
            if len(line_split)>1:
                data  = line_split[1].strip()
            else:
                err = "Not found Id"
            f.close()
        return data, err 

    def set_success_stdout(self):
        data, err= False, None
        with open("tests/stdout.txt", 'r') as f:
            lines = f.readlines()
            line = str(lines[0])
            if re.match(r'^.*succes.*$', line):
                data  = True
            else: 
                err = line
            f.close()
        return data, err