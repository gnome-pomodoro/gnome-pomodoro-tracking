#! /usr/bin/python3
import os 
from gp_tracking import GPTracking

DIRHOME = os.path.expanduser("~")
GPT_CONF = "{}/.gp-tracking.conf".format(DIRHOME)

if __name__ == "__main__":
    if not os.path.exists(GPT_CONF):
        print( "The file {} not exists. Try re-install" .format(GPT_CONF))
    else:
        gpt = GPTracking(GPT_CONF, "", DIRHOME)
        gpt.load_plugin()
        gpt.gptparse_args()
        gpt.cli()

