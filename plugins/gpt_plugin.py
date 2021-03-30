# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import requests

class GPTPlugin(object):

    name = None
    session = {}

    def __init__(self, gpt):
        self.gpt = gpt
        self.setup()

    # Management setup
    def setup(self):
        """
        Checks params required for provider connect.
        params:
            None
        return:
            None
        """
        raise NotImplementedError

    def auth(self) -> bool:
        """
        Check if auth was successful
        """
        raise NotImplementedError

    # Management Time Entry
    def add_time_entry(self, **kwargs):
        """
        Params:
            description,str: Description activity
            start,str:       Datetime in UTC format %Y-%m-%dT%H:%M:%SZ
            ends,str:        Datetime in UTC format %Y-%m-%dT%H:%M:%SZ
            minutes,float:   Elapsed
        return:
            id,int:
        Exception:
            fail to add
        """
        raise NotImplementedError

    def rm_time_entry(self, **kwargs) -> bool:
        """
        Remove time entry in Time Tracking Software
        Params:
            id,int: time entry | required
        Return:
            success,bool:
        Exption:
            fail to remove
        """
        raise NotImplementedError

    # Management CLI
    def add_parse_args(self, kind):
        """
        Add optional arguments in command terminal
        params:
            None
        return:
            None
        e.g
        self.gptracking.parse.add_argument('--clockify-workspaces',
            action='store_const',
            dest='clockify_workspaces',
            help='List clockify workspaces',
            const=True,
        )
        """
        raise NotImplementedError

    def cli(self):
        """
        Interprets command line arguments
        params:
            None
        return:
            None

        e.g
        params = self.gptracking.gptparse_params()
        if params.clockify_workspaces:
            pass
        """
        raise NotImplementedError

    def status(self):
        """
        Print the current state of the Pomodoro ( gp-tracking --status )
        params:
            None
        return:
            None

        e.g

        _name = self.gptracking.gptconfig_get(self.GTP_CONFIG, "clockify_name")
        self.gptracking.print_cli([{'name': _name }])

        """
        raise NotImplementedError

    # Management Request
    def http_call(self, method, url, **kwargs):
        # url = urljoin(self.url, url)
        response = requests.request(method, url, **kwargs)
        if response.ok:
            return response.json()
        text = response.text
        raise Exception(text)
