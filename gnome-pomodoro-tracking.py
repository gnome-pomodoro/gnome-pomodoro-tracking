#! /usr/bin/python3
import os 
from gp_tracking import GPTracking

DIRHOME = os.path.expanduser("~")
GPT_CONF = "{}/.gnome-pomodoro-tracking.conf".format(DIRHOME)

if __name__ == "__main__":
    if not os.path.exists(GPT_CONF):
        print( "The file {} not exists. Try re-install" .format(GPT_CONF))
    else:
        gpt = GPTracking(GPT_CONF, "", DIRHOME)
        gpt.load_plugin()
        gpt.add_parse_args()
        gpt.cli()

