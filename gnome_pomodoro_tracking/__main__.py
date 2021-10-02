# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import os
from gnome_pomodoro_tracking.tracking import Tracking

def main():
    config = "%s/.local/share/gnome-pomodoro/tracking.config" % os.path.expanduser("~")
    gpt = Tracking(config)
    gpt.load_plugin()
    gpt.add_parse_args()
    gpt.cli()

if __name__ == "__main__":
    main()
    

